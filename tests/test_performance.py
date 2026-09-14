import asyncio
import json

import httpx
import numpy as np

from nu_chat import api, generation, retrieval


def test_planning_cache_keeps_language_and_complete_followup_context(monkeypatch):
    calls = []

    def model(messages, **kwargs):
        calls.append(messages)
        return json.dumps(
            {
                "intent": "university",
                "queries": ["tuition fees"],
                "meaning": "Tuition fees",
                "general_question": "",
            }
        )

    monkeypatch.setattr(generation, "call_model", model)
    first = generation.plan_query("How much?", "en", [])
    first["queries"].append("caller mutation")
    assert "caller mutation" not in generation.plan_query("How much?", "en", [])["queries"]
    assert len(calls) == 1
    generation.plan_query("How much?", "ar", [])
    generation.plan_query("How much?", "en", [{"role": "user", "content": "ITCS"}])
    assert len(calls) == 3


def test_retrieval_cache_is_isolated_from_citation_mutations_and_new_indexes(tmp_path, monkeypatch):
    calls = []

    class Encoder:
        def encode(self, query, **kwargs):
            calls.append(query)
            return np.array([1.0, 0.0])

    chunk = {
        "id": "one",
        "url": "https://nu.edu.eg/apply",
        "title": "Admissions",
        "text": "Apply online",
    }
    path = tmp_path / "index.npz"
    np.savez(
        path,
        vectors=np.array([[1.0, 0.0]]),
        metadata=json.dumps(
            {
                "model": retrieval.EMBEDDING_MODEL,
                "chunks": [chunk],
            }
        ),
    )
    monkeypatch.setattr(retrieval, "encoder", lambda: Encoder())
    monkeypatch.setattr(retrieval, "reranker", lambda: None)
    index = retrieval.Retriever(path)
    first = index.search("admissions")
    first[0]["citation"] = 99
    first[0]["text"] = "corrupted"
    assert index.search("admissions")[0]["citation"] == 1
    assert index.search("admissions")[0]["text"] == "Apply online"
    assert len(calls) == 1
    index.search("admissions", prefer_text=True)
    assert len(calls) == 2
    retrieval.Retriever(path).search("admissions")
    assert len(calls) == 3


def test_health_never_probes_model_or_loads_index(monkeypatch, client):
    def forbidden():
        raise AssertionError("Health must only return the background snapshot")

    monkeypatch.setattr(api, "model_available", forbidden)
    monkeypatch.setattr(api, "retriever", forbidden)
    assert client.get("/api/health").status_code == 200


def test_keepalive_is_valid_json_and_connect_timeout_is_independent(monkeypatch):
    calls = []

    def post(url, **kwargs):
        calls.append(kwargs)
        return httpx.Response(200, request=httpx.Request("POST", url), json={})

    monkeypatch.setattr(generation.model_client, "post", post)
    generation.warm_model()
    keep_alive = calls[0]["json"]["keep_alive"]
    assert keep_alive != "-1"  # Ollama requires numeric -1 or a duration such as '-1m'.
    assert calls[0]["timeout"].connect == 2
    assert calls[0]["timeout"].read == 180


def test_source_library_waits_for_startup_without_blocking_health(monkeypatch):
    async def scenario():
        release = asyncio.Event()
        warmup = asyncio.create_task(release.wait())
        monkeypatch.setattr(api.app.state, "warmup", warmup, raising=False)
        calls = []

        def read_sources():
            calls.append(1)
            return {"sources": [{"title": "NU"}]}

        monkeypatch.setattr(api, "read_sources", read_sources)
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=api.app), base_url="http://test"
        ) as client:
            sources = asyncio.create_task(client.get("/api/sources"))
            await asyncio.sleep(0)
            assert not sources.done() and calls == []
            assert (await asyncio.wait_for(client.get("/api/health"), 1)).status_code == 200
            release.set()
            assert (await sources).json() == {"sources": [{"title": "NU"}]}
            assert calls == [1]

    asyncio.run(scenario())
