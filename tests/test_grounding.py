import json

import pytest

from nu_chat import generation


def test_audit_uses_cited_text_and_rejects_malformed_verdict(monkeypatch):
    calls = []

    def reply(messages, **kwargs):
        calls.append(messages)
        return '{"unsupported_claims": "not a list"}'

    monkeypatch.setattr(generation, "call_model", reply)
    source = {"citation": 1, "title": "Contact", "text": "Sheikh Zayed, Giza"}
    with pytest.raises(ValueError, match="Invalid evidence audit"):
        generation.verify_grounding("Where?", "Mansoura [1]", [source])
    evidence = json.loads(calls[0][-1]["content"])["evidence"]
    assert evidence == [{"id": 1, "title": "Contact", "text": "Sheikh Zayed, Giza"}]


@pytest.mark.parametrize("repair_succeeds", [True, False])
def test_unsupported_draft_is_repaired_or_withheld(monkeypatch, repair_succeeds):
    answers = iter(["Mansoura [1]", "Sheikh Zayed [1]"])
    verdicts = iter([["Mansoura is not in the source"], [] if repair_succeeds else ["Still wrong"]])
    messages = []

    def reply(history, **kwargs):
        messages.append(list(history))
        return json.dumps({"answer": next(answers), "supported": True, "citations": [1]})

    monkeypatch.setattr(generation, "call_model", reply)
    monkeypatch.setattr(generation, "verify_grounding", lambda *a: next(verdicts))
    source = {
        "citation": 1,
        "title": "Contact",
        "url": "https://nu.edu.eg/contact-us",
        "text": "Sheikh Zayed, Giza",
    }
    if repair_succeeds:
        answer, mode = generation.generate_answer("Where is NU?", "en", [], [source], True)
        assert answer == "Sheikh Zayed [1]" and mode == "generated"
    else:
        with pytest.raises(generation.GenerationError, match="verify its answer"):
            generation.generate_answer("Where is NU?", "en", [], [source], True)
    assert len(messages) == 2
    assert "Mansoura is not in the source" in messages[1][-1]["content"]
