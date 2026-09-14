"""Small same-origin API. Ingestion is an explicit CLI action, not a web endpoint."""

import asyncio
import time
from contextlib import asynccontextmanager
from functools import lru_cache
from hashlib import sha256
from typing import Literal
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from nu_chat.citations import citation_ids
from nu_chat.config import (
    DATA_DIR,
    EMBEDDING_DEVICE,
    EMBEDDING_MODEL,
    MODEL_THINKING,
    OLLAMA_MODEL,
    RERANK_MODEL,
    ROOT,
)
from nu_chat.evidence import append_current_links, focus_sources, needs_current_link
from nu_chat.generation import (
    GenerationError,
    generate_answer,
    model_available,
    plan_query,
)
from nu_chat.intent import INTENT_FILE, classify_intent
from nu_chat.language import detect_language
from nu_chat.persona import identity_question
from nu_chat.request_cache import RequestCache
from nu_chat.request_queue import RequestQueue
from nu_chat.retrieval import Retriever, encoder, reranker


@asynccontextmanager
async def lifespan(app):
    if (DATA_DIR / "index.npz").exists():

        def warm_retrieval():
            encoder()
            reranker()
            retriever()
            classify_intent("Good morning")

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
request_cache = RequestCache()
CODE_VERSION = sha256(
    b"".join(path.read_bytes() for path in sorted((ROOT / "nu_chat").glob("*.py")))
).hexdigest()[:16]


class Turn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=5000)


class ChatRequest(BaseModel):
    request_id: UUID | None = None
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
        "intent_ready": INTENT_FILE.exists(),
        "model_ready": model_available(),
        "model": OLLAMA_MODEL,
        "thinking": MODEL_THINKING,
        "index_version": (DATA_DIR / "index.npz").stat().st_mtime_ns if exists else None,
        "encoder": EMBEDDING_MODEL,
        "retrieval_device": EMBEDDING_DEVICE,
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
    if request.request_id:
        fingerprint = sha256(request.model_dump_json(exclude={"request_id"}).encode()).hexdigest()
        return request_cache.run(
            str(request.request_id), fingerprint, lambda: queued_answer(request)
        )
    return queued_answer(request)


def queued_answer(request: ChatRequest):
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
        # Franco is accepted as input; Arabic output is the user's preferred default.
        if request.language == "auto" and language == "franco":
            language = "ar"
        history = [turn.model_dump() for turn in request.history[-6:]]
        classification = None
        if identity_question(question):
            available = False
            plan = {
                "route": "identity",
                "query": "",
                "meaning": question,
                "normalization": "identity",
            }
        else:
            classification = classify_intent(question)
            available = model_available()
            if classification["confident"] and classification["route"] == "identity":
                plan = {
                    "route": "identity",
                    "query": "",
                    "meaning": "",
                    "normalization": "intent_classifier",
                }
            elif not available:
                raise GenerationError("The local model is unavailable. Start Ollama, then retry.")
            elif classification["confident"] and classification["route"] == "general":
                plan = {
                    "query": "",
                    "meaning": "",
                    "normalization": "intent_classifier",
                    "route": "general",
                    "general_information": classification["general_information"],
                }
            else:
                # A document request already needs a query-planning call. Resolve its exact
                # intent there too: an admission procedure is not a persuasion request.
                plan = plan_query(question, detected, history)

        planned = time.perf_counter()
        query = plan["query"]
        queries = plan.get("queries", [query] if query else [])
        sources = []
        if plan["route"] in ("university", "mixed", "advising"):
            if not (DATA_DIR / "index.npz").exists():
                raise HTTPException(503, "University sources are not indexed yet.")
            if plan["route"] == "advising":
                sources = retriever().advise(query, original=question)
            else:
                seen = set()
                for part in queries:
                    # Each part gets its own retrieval budget and evidence focus. The
                    # other question must not distort the reranker's relevance score.
                    hits = focus_sources(
                        part,
                        retriever().search(
                            part,
                            original=question if len(queries) == 1 else "",
                            meaning=part,
                        ),
                    )
                    for hit in hits:
                        key = (
                            hit.get("url"),
                            " ".join(hit.get("answer_text", hit["text"]).split()),
                        )
                        if key not in seen:
                            sources.append({**hit, "citation": len(sources) + 1})
                            seen.add(key)
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
            intent_label=classification["label"]
            if classification and classification["confident"]
            else plan.get("intent", ""),
        )
        current_links = plan["route"] in {"university", "mixed", "advising"} and needs_current_link(
            question + " " + query + " " + plan.get("meaning", "") + " " + answer
        )
        if current_links:
            answer = append_current_links(answer, sources, language)
        cited = citation_ids(answer)
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
                "retrieval_queries": queries,
                "current_information_links": current_links,
                "route": plan["route"],
                "general_information": plan.get("general_information", False) is True,
                "message_meaning": plan.get("meaning", question),
                "normalization": plan["normalization"],
                "intent_classification": classification,
                "encoder": EMBEDDING_MODEL if classification or sources else None,
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
            "The local retrieval or intent model could not be loaded. Check the server log; run train-intent and index after setup.",
        ) from exc
