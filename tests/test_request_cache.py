import asyncio
import threading
from uuid import uuid4

import httpx
import pytest
from fastapi import HTTPException

from nu_chat import api
from nu_chat.request_cache import RequestCache
from nu_chat.request_queue import RequestQueue


def test_cancelled_client_rejoins_original_job_without_releasing_gpu():
    async def scenario():
        cache, queue = RequestCache(), RequestQueue()
        entered, release = asyncio.Event(), asyncio.Event()
        calls = []

        async def generate(entry):
            async with queue.slot():
                calls.append(1)
                entered.set()
                await release.wait()
                return {"answer": "One answer"}

        first = asyncio.create_task(cache.run("id", "body", generate))
        await entered.wait()
        first.cancel()
        with pytest.raises(asyncio.CancelledError):
            await first
        assert queue.active and not cache.entries["id"].task.cancelled()
        retry = asyncio.create_task(cache.run("id", "body", generate))
        release.set()
        assert await retry == {"answer": "One answer"}
        assert not queue.active and calls == [1]

    asyncio.run(scenario())


def test_failed_generation_is_replayed_without_starting_a_second_job():
    async def scenario():
        cache, calls = RequestCache(), []

        async def generate(entry):
            calls.append(1)
            raise HTTPException(503, "Model unavailable")

        for _ in range(2):
            with pytest.raises(HTTPException) as error:
                await cache.run("id", "body", generate)
            assert error.value.status_code == 503
        assert calls == [1]

    asyncio.run(scenario())


def test_cache_is_bounded_and_does_not_evict_an_active_request():
    async def scenario():
        cache = RequestCache(capacity=1)

        async def generate(entry):
            with pytest.raises(HTTPException) as error:
                cache.start("different", "body", generate)
            assert error.value.status_code == 429
            return {"answer": "done"}

        await cache.run("first", "body", generate)
        await cache.run("second", "body", generate)
        assert list(cache.entries) == ["second"]

    asyncio.run(scenario())


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


def test_fifty_reconnects_leave_health_responsive_and_run_one_inference(monkeypatch):
    async def scenario():
        monkeypatch.setattr(api, "request_cache", RequestCache())
        monkeypatch.setattr(api, "chat_queue", RequestQueue())
        entered, release = threading.Event(), threading.Event()
        calls = []

        def answer(request):
            calls.append(request.question)
            entered.set()
            assert release.wait(5)
            return {"answer": "Hello", "pipeline": {}}

        monkeypatch.setattr(api, "answer_request", answer)
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=api.app), base_url="http://test"
        ) as client:
            body = {"request_id": str(uuid4()), "question": "hello"}
            first = asyncio.create_task(client.post("/api/chat", json=body))
            assert await asyncio.to_thread(entered.wait, 2)
            retries = [asyncio.create_task(client.post("/api/chat", json=body)) for _ in range(50)]
            try:
                health = await asyncio.wait_for(client.get("/api/health"), 1)
                assert health.status_code == 200
                assert api.chat_queue.active and len(calls) == 1
                assert not api.chat_queue.waiting
            finally:
                release.set()
            results = await asyncio.gather(first, *retries)
            assert all(r.status_code == 200 and r.json() == results[0].json() for r in results)
            # Immediately following a completed response must not see a stale busy flag.
            assert (
                await client.post("/api/chat", json={"question": "next question"})
            ).status_code == 200
            assert calls == ["hello", "next question"] and not api.chat_queue.active

    asyncio.run(scenario())


def test_stream_result_replays_and_preserves_http_errors(monkeypatch, client):
    monkeypatch.setattr(api, "request_cache", RequestCache())
    calls = []

    def answer(request):
        calls.append(request.question)
        if request.question == "fail":
            raise HTTPException(503, "Model unavailable")
        return {"answer": "أهلا", "sources": [], "pipeline": {}}

    monkeypatch.setattr(api, "answer_request", answer)
    body = {"request_id": str(uuid4()), "question": "hello"}
    for _ in range(2):
        response = client.post("/api/chat/stream", json=body)
        assert response.headers["content-type"].startswith("text/event-stream")
        assert "event: result\n" in response.text and "أهلا" in response.text
    assert calls == ["hello"]
    assert client.post("/api/chat/stream", json={**body, "question": "changed"}).status_code == 409
    response = client.post("/api/chat/stream", json={"question": "fail"})
    assert "event: error\n" in response.text and '"status": 503' in response.text
    assert not api.chat_queue.active


def test_waiting_cancellation_and_overflow_preserve_queue_owner():
    async def scenario():
        queue = RequestQueue(capacity=1)

        async def wait():
            async with queue.slot():
                raise AssertionError("Cancelled waiter must never run")

        async with queue.slot():
            waiter = asyncio.create_task(wait())
            await asyncio.sleep(0)
            with pytest.raises(HTTPException) as error:
                async with queue.slot():
                    pass
            assert error.value.status_code == 429
            waiter.cancel()
            with pytest.raises(asyncio.CancelledError):
                await waiter
            assert queue.active and not queue.waiting
        assert not queue.active

    asyncio.run(scenario())
