"""A small FIFO queue for one local GPU, with bounded waiting and guaranteed release."""

import threading
import time
from collections import deque
from contextlib import contextmanager

from fastapi import HTTPException


class RequestQueue:
    def __init__(self, capacity=8, timeout=120):
        self.capacity = capacity
        self.timeout = timeout
        self.condition = threading.Condition()
        self.waiting = deque()
        self.active = False

    @contextmanager
    def slot(self):
        ticket = object()
        started = time.monotonic()
        with self.condition:
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
                    if remaining <= 0:
                        raise HTTPException(
                            503, "The model is taking longer than expected. Please retry."
                        )
                    self.condition.wait(timeout=remaining)
                self.waiting.popleft()
                self.active = True
            except BaseException:
                self.waiting.remove(ticket)
                self.condition.notify_all()
                raise
        try:
            yield round(time.monotonic() - started, 2)
        finally:
            with self.condition:
                self.active = False
                self.condition.notify_all()
