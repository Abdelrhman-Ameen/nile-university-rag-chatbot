"""Reuse one ASGI event loop; unit tests never load models at startup."""

from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient

from nu_chat.api import app


@asynccontextmanager
async def unit_lifespan(app):
    yield


@pytest.fixture(scope="session")
def client():
    original = app.router.lifespan_context
    app.router.lifespan_context = unit_lifespan
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.router.lifespan_context = original
