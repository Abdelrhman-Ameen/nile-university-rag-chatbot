"""Exercise routing boundaries without loading a model or making network requests."""

import pytest

from nu_chat import api, generation
from nu_chat.intent import POLICIES, decision


@pytest.mark.parametrize("label", [label for label in POLICIES if label != "followup"])
def test_fallback_planner_uses_one_intent_to_derive_consistent_policy(monkeypatch, label):
    import json

    route, informational = POLICIES[label]
    monkeypatch.setattr(
        generation,
        "call_model",
        lambda *a, **k: json.dumps(
            {
                "intent": label,
                "meaning": "Current message",
                "queries": ["NU topic"],
                "general_question": "Explain a Python list" if label == "mixed" else "",
            }
        ),
    )
    plan = generation.plan_query("A message", "en", [])
    assert (plan["route"], plan["general_information"]) == (route, informational)
    assert bool(plan["query"]) == (route in {"advising", "university", "mixed"})


def test_uncertain_and_context_dependent_intents_defer_to_planner():
    assert not decision([0.52, 0.48], ["university", "opinion"])["confident"]
    assert not decision([0.95, 0.05], ["followup", "university"])["confident"]
    assert decision([0.85, 0.15], ["university_advice", "emotion"])["route"] == "advising"
    assert not decision([0.85, 0.15], ["university_advice", "university"])["confident"]


@pytest.mark.parametrize("route", ["general", "advising", "university", "mixed"])
def test_head_skips_planning_for_chat_but_document_planner_resolves_intent(
    monkeypatch, tmp_path, route, client
):
    classification = {
        "confident": True,
        "route": route,
        "label": "university_advice" if route == "advising" else route,
        "general_information": route == "mixed",
    }
    monkeypatch.setattr(api, "classify_intent", lambda _: classification)
    monkeypatch.setattr(api, "model_available", lambda: True)
    monkeypatch.setattr(api, "DATA_DIR", tmp_path)
    (tmp_path / "index.npz").touch()
    events = []

    def unexpected(*args):
        pytest.fail("Confident intent was needlessly reclassified by the generator")

    def rewrite(question, language, history):
        events.append("rewrite")
        assert history == [{"role": "user", "content": "I want to study computing"}]
        return {
            "meaning": "NU opportunities",
            "query": "undergraduate research",
            "normalization": "test",
            "route": route,
            "general_information": route == "mixed",
        }

    class Index:
        def search(self, query, **kwargs):
            events.append("search")
            return [{"citation": 1, "text": "NU holds a research forum"}]

        def advise(self, query, **kwargs):
            return self.search(query, **kwargs)

    def answer(question, language, history, sources, available, **kwargs):
        assert kwargs["route"] == route
        assert bool(sources) == (route != "general")
        return "Useful response [1]" if sources else "Hello", "generated" if sources else "general"

    monkeypatch.setattr(api, "plan_query", unexpected if route == "general" else rewrite)
    monkeypatch.setattr(api, "retriever", lambda: Index())
    monkeypatch.setattr(api, "generate_answer", answer)
    result = client.post(
        "/api/chat",
        json={
            "question": "Tell me more about choosing NU",
            "history": [{"role": "user", "content": "I want to study computing"}],
        },
    )
    assert result.status_code == 200
    assert events == ([] if route == "general" else ["rewrite", "search"])
    assert result.json()["pipeline"]["intent_classification"] == classification


def test_unconfident_head_passes_history_to_planner(monkeypatch, client):
    monkeypatch.setattr(api, "classify_intent", lambda _: {"confident": False})
    monkeypatch.setattr(api, "model_available", lambda: True)
    calls = []

    def plan(question, language, history):
        calls.append(history)
        return {"route": "general", "query": "", "normalization": "test"}

    monkeypatch.setattr(api, "plan_query", plan)
    monkeypatch.setattr(api, "generate_answer", lambda *a, **k: ("An explanation", "general"))
    history = [{"role": "user", "content": "Explain recursion"}]
    assert (
        client.post(
            "/api/chat", json={"question": "Make that simpler", "history": history}
        ).status_code
        == 200
    )
    assert calls == [history]
