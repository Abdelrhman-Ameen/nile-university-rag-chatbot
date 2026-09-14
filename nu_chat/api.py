"""Small same-origin API. Ingestion is an explicit CLI action, not a web endpoint."""

import asyncio
import re
import time
from contextlib import asynccontextmanager
from functools import lru_cache
from hashlib import sha256
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from nu_chat.config import DATA_DIR, EMBEDDING_MODEL, OLLAMA_MODEL, RERANK_MODEL, ROOT
from nu_chat.generation import GenerationError, generate_answer, model_available, plan_query
from nu_chat.language import detect_language
from nu_chat.persona import identity_question
from nu_chat.request_queue import RequestQueue
from nu_chat.retrieval import Retriever, encoder, reranker


@asynccontextmanager
async def lifespan(app):
    if (DATA_DIR / "index.npz").exists():

        def warm_retrieval():
            encoder()
            reranker()
            retriever()

        await asyncio.to_thread(warm_retrieval)
    yield


app = FastAPI(
    title="NU Chat",
    description="Nile University Egypt multilingual chat",
    version="1.2.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
chat_queue = RequestQueue()
CODE_VERSION = sha256(
    b"".join(path.read_bytes() for path in sorted((ROOT / "nu_chat").glob("*.py")))
).hexdigest()[:16]


class Turn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=5000)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1500)
    history: list[Turn] = Field(default_factory=list, max_length=12)
    language: Literal["auto", "en", "ar", "franco", "mixed"] = "auto"


@lru_cache(maxsize=1)
def _load_retriever(index_modified: int):
    return Retriever()


def retriever():
    return _load_retriever((DATA_DIR / "index.npz").stat().st_mtime_ns)


@app.get("/")
def home():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/api/health")
def health():
    exists = (DATA_DIR / "index.npz").exists()
    index = retriever() if exists else None
    return {
        "index_ready": exists,
        "model_ready": model_available(),
        "model": OLLAMA_MODEL,
        "index_version": (DATA_DIR / "index.npz").stat().st_mtime_ns if exists else None,
        "encoder": EMBEDDING_MODEL,
        "reranker": RERANK_MODEL,
        "code_version": CODE_VERSION,
        "chunks": len(index.chunks) if index else 0,
        "sources": len({c["url"] for c in index.chunks}) if index else 0,
        "collected_at": max((c["fetched_at"] for c in index.chunks), default=None)
        if index
        else None,
    }


@app.get("/api/sources")
def source_library():
    if not (DATA_DIR / "index.npz").exists():
        return {"sources": []}
    unique = {}
    for c in retriever().chunks:
        unique.setdefault(
            c["url"], {k: c[k] for k in ("url", "title", "kind", "fetched_at", "archived")}
        )
    return {"sources": sorted(unique.values(), key=lambda s: s["title"].lower())}


@app.post("/api/chat")
def chat(request: ChatRequest):
    if identity_question(request.question):
        return answer_request(request)
    with chat_queue.slot() as waited:
        result = answer_request(request)
        result["pipeline"]["queue_seconds"] = waited
        return result


def answer_request(request: ChatRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(422, "Write a question first.")
    try:
        start = time.perf_counter()
        detected = detect_language(question)
        language = request.language if request.language != "auto" else detected
        history = [turn.model_dump() for turn in request.history[-6:]]
        if identity_question(question):
            available = False
            plan = {
                "route": "identity",
                "query": "",
                "meaning": question,
                "normalization": "identity",
            }
        else:
            available = model_available()
            if not available:
                raise GenerationError("Qwen is unavailable. Start Ollama, then retry.")
            plan = plan_query(question, detected, history)
        planned = time.perf_counter()
        query = plan["query"]
        sources = []
        if plan["route"] in ("university", "mixed"):
            if not (DATA_DIR / "index.npz").exists():
                raise HTTPException(503, "University sources are not indexed yet.")
            sources = retriever().search(
                query,
                original=question,
                meaning=query if plan["route"] == "mixed" else plan.get("meaning", query),
            )
        retrieved = time.perf_counter()
        answer, mode = generate_answer(
            question,
            language,
            history,
            sources,
            available,
            retrieval_query=query,
            route=plan["route"],
            meaning=plan.get("meaning", ""),
            general_information=plan.get("general_information", False) is True,
        )
        cited = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
        for source in sources:
            source["cited"] = source["citation"] in cited
        return {
            "answer": answer,
            "sources": sources,
            "mode": mode,
            "pipeline": {
                "detected_language": detected,
                "reply_language": language,
                "retrieval_query": query,
                "route": plan["route"],
                "general_information": plan.get("general_information", False) is True,
                "message_meaning": plan.get("meaning", question),
                "normalization": plan["normalization"],
                "encoder": EMBEDDING_MODEL if plan["route"] in ("university", "mixed") else None,
                "generator": None if mode == "identity" else OLLAMA_MODEL,
                "elapsed_seconds": round(time.perf_counter() - start, 2),
                "planning_seconds": round(planned - start, 2),
                "retrieval_seconds": round(retrieved - planned, 2),
                "generation_seconds": round(time.perf_counter() - retrieved, 2),
            },
        }
    except GenerationError as exc:
        raise HTTPException(503, str(exc)) from exc
    except (OSError, ValueError) as exc:
        raise HTTPException(
            503,
            "The retrieval index or embedding model could not be loaded. Check the server log and rebuild the index.",
        ) from exc
