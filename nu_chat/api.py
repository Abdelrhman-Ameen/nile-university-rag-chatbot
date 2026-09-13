"""Small same-origin API. Ingestion is an explicit CLI action, not a web endpoint."""

import re
import threading
import time
from functools import lru_cache
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from nu_chat.config import DATA_DIR, EMBEDDING_MODEL, OLLAMA_MODEL, ROOT
from nu_chat.generation import generate_answer, model_available, normalize_query
from nu_chat.language import detect_language
from nu_chat.retrieval import Retriever

app = FastAPI(title="Nile Guide", description="Nile University multilingual RAG", version="1.0.0")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
chat_lock = threading.Lock()


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
        "encoder": EMBEDDING_MODEL,
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
    question = request.question.strip()
    if not question:
        raise HTTPException(422, "Write a question first.")
    if not (DATA_DIR / "index.npz").exists():
        raise HTTPException(503, "The source index is empty. Run: python -m nu_chat ingest")
    if not chat_lock.acquire(blocking=False):
        raise HTTPException(429, "Another answer is being prepared. Try again shortly.")
    try:
        start = time.perf_counter()
        detected = detect_language(question)
        language = request.language if request.language != "auto" else detected
        history = [turn.model_dump() for turn in request.history[-6:]]
        available = model_available()
        query, normalization = normalize_query(question, detected, history, available)
        sources = retriever().search(query, original=question)
        answer, mode = generate_answer(
            question, language, history, sources, available, retrieval_query=query
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
                "normalization": normalization,
                "encoder": EMBEDDING_MODEL,
                "generator": OLLAMA_MODEL if mode == "generated" else None,
                "elapsed_seconds": round(time.perf_counter() - start, 2),
            },
        }
    except (OSError, ValueError) as exc:
        raise HTTPException(
            503,
            "The retrieval index or embedding model could not be loaded. Check the server log and rebuild the index.",
        ) from exc
    finally:
        chat_lock.release()
