"""Bounded FIFO admission for one GPU, without occupying waiting worker threads."""

import asyncio
import time
from collections import deque
from contextlib import asynccontextmanager

from fastapi import HTTPException


class RequestQueue:
    def __init__(self, capacity=8, timeout=120):
        self.capacity = capacity
        self.timeout = timeout
        self.condition = asyncio.Condition()
        self.waiting = deque()
        self.active = False

    @asynccontextmanager
    async def slot(self):
        ticket = object()
        started = time.monotonic()
        async with self.condition:
            if len(self.waiting) >= self.capacity:
                raise HTTPException(
                    429,
                    "The request queue is full. Please retry shortly.",
                    headers={"Retry-After": "5"},
                )
            self.waiting.append(ticket)
            try:
                while self.active or self.waiting[0] is not ticket:
                    remaining = self.timeout - (time.monotonic() - started)
                    try:
                        await asyncio.wait_for(self.condition.wait(), max(0, remaining))
                    except TimeoutError as exc:
                        raise HTTPException(
                            503, "The model is taking longer than expected. Please retry."
                        ) from exc
                self.waiting.popleft()
                self.active = True
            except BaseException:
                self.waiting.remove(ticket)
                self.condition.notify_all()
                raise
        try:
            yield round(time.monotonic() - started, 2)
        finally:
            async with self.condition:
                self.active = False
                self.condition.notify_all()
