"""Short-lived idempotency for reconnects, including requests still being generated."""

import threading
import time
from dataclasses import dataclass, field

from fastapi import HTTPException


@dataclass
class Entry:
    fingerprint: str
    done: threading.Event = field(default_factory=threading.Event)
    completed_at: float = 0
    result: dict | None = None
    error: tuple | None = None


class RequestCache:
    def __init__(self, capacity=128, ttl=300, wait_timeout=360):
        self.capacity, self.ttl, self.wait_timeout = capacity, ttl, wait_timeout
        self.entries = {}
        self.lock = threading.Lock()

    def run(self, key: str, fingerprint: str, generate):
        with self.lock:
            now = time.monotonic()
            self.entries = {
                k: e
                for k, e in self.entries.items()
                if not e.done.is_set() or now - e.completed_at < self.ttl
            }
            entry = self.entries.get(key)
            owner = entry is None
            if entry and entry.fingerprint != fingerprint:
                raise HTTPException(
                    409, "This request ID was already used for a different message."
                )
            if owner:
                if len(self.entries) >= self.capacity:
                    completed = [k for k, e in self.entries.items() if e.done.is_set()]
                    if not completed:
                        raise HTTPException(429, "Too many active requests. Please retry shortly.")
                    del self.entries[completed[0]]
                entry = self.entries[key] = Entry(fingerprint)
        if owner:
            try:
                entry.result = generate()
            except Exception as exc:
                entry.error = (
                    (exc.status_code, exc.detail, exc.headers)
                    if isinstance(exc, HTTPException)
                    else (500, "The request could not be completed. Please retry.", None)
                )
                raise
            finally:
                entry.completed_at = time.monotonic()
                entry.done.set()
        elif not entry.done.wait(self.wait_timeout):
            raise HTTPException(503, "The original request is still running. Please retry shortly.")
        if entry.error:
            raise HTTPException(*entry.error)
        return entry.result
