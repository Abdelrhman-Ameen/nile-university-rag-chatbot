import threading
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

import pytest
from fastapi import HTTPException

from nu_chat import api
from nu_chat.request_cache import RequestCache


def test_overlapping_retry_waits_for_the_same_generation():
    cache = RequestCache(wait_timeout=2)
    entered, release = threading.Event(), threading.Event()
    calls = []

    def generate():
        calls.append(1)
        entered.set()
        assert release.wait(2)
        return {"answer": "One answer"}

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(cache.run, "id", "body", generate)
        assert entered.wait(2)
        retry = pool.submit(cache.run, "id", "body", generate)
        release.set()
        assert first.result() == retry.result() == {"answer": "One answer"}
    assert calls == [1]


def test_failed_generation_is_replayed_without_starting_a_second_job():
    cache = RequestCache()
    calls = []

    def generate():
        calls.append(1)
        raise HTTPException(503, "Model unavailable")

    for _ in range(2):
        with pytest.raises(HTTPException) as error:
            cache.run("id", "body", generate)
        assert error.value.status_code == 503
    assert calls == [1]


def test_cache_is_bounded_and_does_not_evict_an_active_request():
    cache = RequestCache(capacity=1)

    def generate():
        with pytest.raises(HTTPException) as error:
            cache.run("different", "body", lambda: {})
        assert error.value.status_code == 429
        return {"answer": "done"}

    cache.run("first", "body", generate)
    cache.run("second", "body", lambda: {})
    assert list(cache.entries) == ["second"]


def test_api_replay_requires_identical_validated_payload(monkeypatch, client):
    monkeypatch.setattr(api, "request_cache", RequestCache())
    calls = []

    def answer(request):
        calls.append(request.question)
        return {"answer": "Hello", "pipeline": {}}

    monkeypatch.setattr(api, "answer_request", answer)
    body = {"request_id": str(uuid4()), "question": "hello"}
    one = client.post("/api/chat", json=body)
    two = client.post("/api/chat", json=body)
    assert one.status_code == two.status_code == 200
    assert one.json() == two.json() and calls == ["hello"]
    assert client.post("/api/chat", json={**body, "question": "different"}).status_code == 409
    assert calls == ["hello"]
