"""Per-request progress and timings, carried into the inference worker by contextvars."""

from contextvars import ContextVar

progress = ContextVar("progress", default=None)
model_timings = ContextVar("model_timings", default=None)
current_stage = ContextVar("current_stage", default="understanding")


def stage(name):
    current_stage.set(name)
    callback = progress.get()
    if callback:
        callback(name)
