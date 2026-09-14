"""Reconnect-safe jobs. Only the ASGI event loop accesses this bounded cache."""

import asyncio
import time
from dataclasses import dataclass

from fastapi import HTTPException


@dataclass
class Entry:
    fingerprint: str
    task: asyncio.Task | None = None
    completed_at: float = 0
    stage: str = "queued"


class RequestCache:
    def __init__(self, capacity=128, ttl=300):
        self.capacity, self.ttl = capacity, ttl
        self.entries = {}

    def start(self, key: str, fingerprint: str, generate):
        now = time.monotonic()
        self.entries = {
            k: e
            for k, e in self.entries.items()
            if not e.task.done() or now - e.completed_at < self.ttl
        }
        entry = self.entries.get(key)
        if entry:
            if entry.fingerprint != fingerprint:
                raise HTTPException(
                    409, "This request ID was already used for a different message."
                )
            return entry
        if len(self.entries) >= self.capacity:
            completed = [k for k, e in self.entries.items() if e.task.done()]
            if not completed:
                raise HTTPException(429, "Too many active requests. Please retry shortly.")
            del self.entries[completed[0]]
        entry = self.entries[key] = Entry(fingerprint)
        entry.task = asyncio.create_task(generate(entry))

        def completed(task):
            entry.completed_at = time.monotonic()
            # Consume orphaned exceptions; result() still replays them after a reconnect.
            if not task.cancelled():
                task.exception()

        entry.task.add_done_callback(completed)
        return entry

    async def run(self, key: str, fingerprint: str, generate):
        return await asyncio.shield(self.start(key, fingerprint, generate).task)

    async def drain(self):
        await asyncio.gather(*(e.task for e in self.entries.values()), return_exceptions=True)
