"""Small same-origin API. Ingestion is an explicit CLI action, not a web endpoint."""

import asyncio
import json
import logging
import re
import threading
import time
from contextlib import asynccontextmanager
from functools import lru_cache
from hashlib import sha256
from typing import Literal
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
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
    model_client,
    needs_live_confirmation,
    plan_query,
    warm_model,
)
from nu_chat.intent import INTENT_FILE, classify_intent
from nu_chat.language import detect_language
from nu_chat.persona import identity_question
from nu_chat.request_cache import RequestCache
from nu_chat.request_queue import RequestQueue
from nu_chat.retrieval import Retriever, encoder, reranker
from nu_chat.routing import (
    direct_live_query,
    has_university_context,
    is_nu_fact_request,
    is_simple_named_nu_question,
    mentions_nu_entity,
)
from nu_chat.telemetry import model_timings, progress, stage

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    app.state.ready = False
    app.state.model_ready = False
    app.state.index_status = {}
    app.state.startup_error = None

    def warmup():
        if (DATA_DIR / "index.npz").exists():
            encoder()
            reranker()
            retriever()
            classify_intent("Good morning")
        try:
            warm_model()
        except Exception:
            log.exception("Local model warmup failed; requests can retry when Ollama recovers")

    async def initialize():
        try:
            await asyncio.to_thread(warmup)
            app.state.index_status = await asyncio.to_thread(index_status)
            app.state.model_ready = await asyncio.to_thread(model_available)
            app.state.ready = True
        except Exception:
            app.state.startup_error = (
                "Local retrieval models could not start. Check the server log."
            )
            log.exception("Retrieval startup failed")
            raise

    async def refresh_status():
        while True:
            app.state.model_ready = await asyncio.to_thread(model_available)
            if app.state.ready:
                app.state.index_status = await asyncio.to_thread(index_status)
            await asyncio.sleep(30)

    app.state.warmup = asyncio.create_task(initialize())
    monitor = asyncio.create_task(refresh_status())
    try:
        yield
    finally:
        monitor.cancel()
        await asyncio.gather(monitor, return_exceptions=True)
        await asyncio.gather(app.state.warmup, return_exceptions=True)
        await request_cache.drain()
        model_client.close()


app = FastAPI(
    title="NU Chat",
    description="Nile University Egypt multilingual chat",
    version="1.3.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
chat_queue = RequestQueue()
request_cache = RequestCache()
index_lock = threading.Lock()
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
    # lru_cache alone permits duplicate concurrent loads on a cold cache miss.
    with index_lock:
        return _load_retriever((DATA_DIR / "index.npz").stat().st_mtime_ns)


@app.get("/")
def home():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/api/health")
async def health():
    # Never probe Ollama, scan the corpus, or wait for inference on a health request.
    return {
        **getattr(app.state, "index_status", {}),
        "ready": getattr(app.state, "ready", False),
        "startup_error": getattr(app.state, "startup_error", None),
        "index_ready": getattr(app.state, "index_status", {}).get("index_ready", False),
        "intent_ready": INTENT_FILE.exists(),
        "model_ready": getattr(app.state, "model_ready", False),
        "model": OLLAMA_MODEL,
        "thinking": MODEL_THINKING,
        "encoder": EMBEDDING_MODEL,
        "retrieval_device": EMBEDDING_DEVICE,
        "reranker": RERANK_MODEL,
        "code_version": CODE_VERSION,
        "queue": {
            "active": chat_queue.active,
            "waiting": len(chat_queue.waiting),
            "capacity": chat_queue.capacity,
        },
    }


@lru_cache(maxsize=1)
def corpus_summary(version):
    index = retriever()
    unique = {}
    for c in index.chunks:
        unique.setdefault(
            c["url"], {k: c[k] for k in ("url", "title", "kind", "fetched_at", "archived")}
        )
    return {
        "index_ready": True,
        "index_version": version,
        "chunks": len(index.chunks),
        "sources": len(unique),
        "collected_at": max((c["fetched_at"] for c in index.chunks), default=None),
    }, sorted(unique.values(), key=lambda s: s["title"].lower())


def index_status():
    path = DATA_DIR / "index.npz"
    return corpus_summary(path.stat().st_mtime_ns)[0] if path.exists() else {"index_ready": False}


@app.get("/api/sources")
async def source_library():
    await wait_until_ready()
    return await asyncio.to_thread(read_sources)


def read_sources():
    path = DATA_DIR / "index.npz"
    return {"sources": corpus_summary(path.stat().st_mtime_ns)[1] if path.exists() else []}


async def wait_until_ready():
    warmup_task = getattr(app.state, "warmup", None)
    if warmup_task:
        try:
            await asyncio.shield(warmup_task)
        except Exception as exc:
            raise HTTPException(503, "Local models could not start. Check the server log.") from exc


def start_request(request):
    if not request.question.strip():
        raise HTTPException(422, "Write a question first.")
    fingerprint = sha256(request.model_dump_json(exclude={"request_id"}).encode()).hexdigest()
    return request_cache.start(
        str(request.request_id or uuid4()), fingerprint, lambda entry: queued_answer(request, entry)
    )


@app.post("/api/chat")
async def chat(request: ChatRequest):
    return await asyncio.shield(start_request(request).task)


@app.post("/api/chat/stream")
async def stream_chat(request: ChatRequest):
    entry = start_request(request)

    async def events():
        previous, last_sent = None, 0
        while not entry.task.done():
            now = time.monotonic()
            if entry.stage != previous or now - last_sent >= 10:
                yield "event: status\ndata: " + json.dumps({"stage": entry.stage}) + "\n\n"
                previous, last_sent = entry.stage, now
            # Waiting or disconnecting never cancels the shared inference job.
            await asyncio.wait({entry.task}, timeout=0.25)
        try:
            result = entry.task.result()
            yield "event: result\ndata: " + json.dumps(result, ensure_ascii=False) + "\n\n"
        except HTTPException as exc:
            yield (
                "event: error\ndata: "
                + json.dumps({"detail": exc.detail, "status": exc.status_code})
                + "\n\n"
            )
        except Exception:
            log.exception("Chat job failed")
            yield 'event: error\ndata: {"detail":"The request could not be completed. Please retry.","status":500}\n\n'

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-store", "X-Accel-Buffering": "no"},
    )


async def queued_answer(request: ChatRequest, entry):
    if identity_question(request.question):
        return answer_request(request)
    async with chat_queue.slot() as waited:
        entry.stage = "starting"
        await wait_until_ready()
        progress_token = progress.set(lambda name: setattr(entry, "stage", name))
        timings = []
        timing_token = model_timings.set(timings)
        try:
            # Only the active job occupies a worker; waiting clients remain asynchronous.
            result = await asyncio.to_thread(answer_request, request)
            result["pipeline"].update(queue_seconds=waited, model_calls=timings)
            return result
        finally:
            progress.reset(progress_token)
            model_timings.reset(timing_token)


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
            stage("understanding")
            classification = classify_intent(question)
            # A tags probe cannot predict whether inference will succeed. Let the actual
            # request reconnect or report its error, avoiding a redundant failure point.
            available = True
            live_request = needs_live_confirmation(question) and (
                has_university_context(question)
                or bool(
                    re.search(
                        r"\b(?:bus|transport|library|copies|meeting|reservation|booking)\b|"
                        r"أتوبيس|اتوبيس|مكتبة|اجتماع|حجز",
                        question,
                        re.I,
                    )
                )
            )
            if live_request and not history:
                query = direct_live_query(question)
                plan = {
                    "route": "university",
                    "query": query,
                    "queries": [query],
                    "meaning": question,
                    "normalization": "live_request",
                    "general_information": False,
                    "intent": "university",
                }
            elif classification["confident"] and classification["route"] == "identity":
                plan = {
                    "route": "identity",
                    "query": "",
                    "meaning": "",
                    "normalization": "intent_classifier",
                }
            elif (
                classification["confident"]
                and classification["route"] == "general"
                and not mentions_nu_entity(question)
            ):
                plan = {
                    "query": "",
                    "meaning": "",
                    "normalization": "intent_classifier",
                    "route": "general",
                    "general_information": classification["general_information"],
                }
            elif (
                not history
                and detected == "en"
                and classification.get("route") in {"university", "advising"}
                and (classification["confident"] or is_simple_named_nu_question(question))
            ):
                plan = {
                    "query": question,
                    "queries": [question],
                    "meaning": question,
                    "normalization": "direct_english",
                    "route": classification["route"],
                    "general_information": False,
                    "intent": classification["label"],
                }
            elif (
                not history
                and detected == "en"
                and classification.get("route") == "mixed"
                and is_simple_named_nu_question(question)
            ):
                plan = {
                    "query": question,
                    "queries": [question],
                    "meaning": question,
                    "normalization": "direct_english",
                    "route": "university",
                    "general_information": False,
                    "intent": "university",
                }
            elif (
                not history
                and detected != "franco"
                and classification.get("route") == "general"
                and classification.get("score", 0) >= 0.5
                and classification.get("margin", 0) >= 0.2
                and not has_university_context(question)
                and not is_nu_fact_request(question)
            ):
                plan = {
                    "query": "",
                    "queries": [],
                    "meaning": question if detected == "en" else "",
                    "normalization": "intent_classifier",
                    "route": "general",
                    "general_information": classification["general_information"],
                    "intent": classification["label"],
                }
            else:
                # A document request already needs a query-planning call. Resolve its exact
                # intent there too: an admission procedure is not a persuasion request.
                plan = plan_query(question, detected, history)
                if plan["route"] == "advising" and is_nu_fact_request(
                    question + " " + plan.get("meaning", "")
                ):
                    plan.update(route="university", intent="university", general_information=False)

        planned = time.perf_counter()
        query = plan["query"]
        queries = plan.get("queries", [query] if query else [])
        sources = []
        if plan["route"] in ("university", "mixed", "advising"):
            stage("searching")
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
                            # Original wording adds candidate terms; the reranker still
                            # judges each subquestion independently against its passage.
                            original=question,
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
        stage("answering")
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
