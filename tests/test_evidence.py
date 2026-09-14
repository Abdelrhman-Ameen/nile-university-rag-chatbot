import json

from nu_chat import api, generation
from nu_chat.evidence import append_current_links, focus_sources, needs_current_link, scoped_queries


def test_bare_fees_use_reviewed_base_without_certificate_assumptions():
    sources = [
        {"citation": 1, "text": "IGCSE 95%: 50% discount", "ocr_reviewed": True},
        {
            "citation": 2,
            "ocr_reviewed": True,
            "text": (
                "First year 2026/2027. Tuition fees by discount category.\n"
                "Category 1: scholarship discount 50%; annual tuition fees 100 EGP.\n"
                "Category 4: scholarship discount 0%; annual tuition fees 200 EGP."
            ),
        },
    ]
    focused = focus_sources("ITCS undergraduate tuition 2026/2027", sources)
    assert len(focused) == 1
    assert "200 EGP" in focused[0]["answer_text"]
    assert "100 EGP" not in focused[0]["answer_text"]
    assert "100 EGP" in focused[0]["text"]  # Preserve provenance for source inspection.
    assert "answer_text" not in focus_sources("ITCS tuition with 50% scholarship", sources)[0]
    assert len(focus_sources("ITCS IGCSE tuition", sources)) == 2
    assert len(focus_sources("ITCS tuition 2025/2026", sources)) == 2
    assert (
        focus_sources("ITCS costs 2026/2027", sources)[0]["answer_text"]
        == focused[0]["answer_text"]
    )


def test_generic_admission_steps_exclude_international_branch_but_explicit_query_keeps_it():
    sources = [
        {
            "citation": 1,
            "text": "Apply Now: Create your account. International students use Study in Egypt.",
        },
        {"citation": 2, "text": "Apply Now: Create your account. Fill out data. Submit."},
    ]
    assert focus_sources("NU admission steps", sources) == [{**sources[1], "citation": 1}]
    assert len(focus_sources("International student admission steps", sources)) == 2


def test_tuition_query_cannot_silently_add_application_charges():
    queries = ["NU tuition fees", "NU application fees", "How to apply to NU"]
    assert scoped_queries(queries, "How do I apply and what is tuition?") == [
        queries[0],
        queries[2],
    ]
    assert scoped_queries(queries[:2], "What is tuition and the application fee?") == queries[:2]
    assert scoped_queries([queries[1]], "What is the application fee?") == [queries[1]]


def test_current_links_are_explicit_deduplicated_and_official():
    sources = [
        {
            "citation": 1,
            "url": "https://nu.edu.eg/fees",
            "title": "Fees",
            "ocr_reviewed": True,
            "text": "Undergraduate tuition 2026/2027. First year only.",
        },
        {"citation": 2, "url": "https://nu.edu.eg/fees", "title": "Fees again"},
        {"citation": 3, "url": "https://nu.edu.eg.evil.example/pay", "title": "Fake"},
    ]
    result = append_current_links("Cost [1] [2] [3]", sources, "ar")
    assert result.count("](https://nu.edu.eg/fees)") == 1
    assert "Fees — 2026/2027" in result
    assert "evil.example" not in result
    assert append_current_links(result, sources, "ar") == result
    assert needs_current_link("مصاريف حاسبات كام؟")
    assert needs_current_link("UGRF submission deadline")
    assert not needs_current_link("Thanks, that helped")
    assert "](https://nu.edu.eg/)" in append_current_links(
        "Current policy not confirmed.", [], "en"
    )


def test_gpa_evidence_cannot_be_replaced_by_freshman_certificate_tiers():
    sources = [
        {"citation": 1, "text": "Historical GPA discount table"},
        {"citation": 2, "text": "IGCSE: 95% certificate score, freshman discount"},
    ]
    assert focus_sources("Continuing student GPA 3.98 discount", sources) == sources[:1]
    queries = ["ITCS GPA discount", "ITCS tuition fees"]
    assert scoped_queries(queries, "What discount do I get with GPA 3.98?") == queries[:1]
    assert scoped_queries(queries, "What discount and tuition fee apply with GPA 3.98?") == queries


def test_multipart_request_retains_application_and_tuition_evidence(monkeypatch, tmp_path, client):
    monkeypatch.setattr(api, "classify_intent", lambda _: {"confident": False})
    monkeypatch.setattr(api, "model_available", lambda: True)
    monkeypatch.setattr(api, "DATA_DIR", tmp_path)
    (tmp_path / "index.npz").touch()
    queries = ["How to apply for undergraduate admission", "ITCS undergraduate tuition"]
    monkeypatch.setattr(
        api,
        "plan_query",
        lambda *a: {
            "route": "university",
            "queries": queries,
            "query": " | ".join(queries),
            "normalization": "test",
        },
    )
    searched = []

    class Index:
        def search(self, query, **kwargs):
            searched.append(query)
            assert kwargs["meaning"] == query
            return [
                {
                    "id": query,
                    "citation": 1,
                    "url": "https://nu.edu.eg/apply-now",
                    "title": query,
                    "text": "Apply Now: create your account"
                    if query == queries[0]
                    else "ITCS undergraduate tuition amount",
                }
            ]

    monkeypatch.setattr(api, "retriever", Index)

    def generate(*args, **kwargs):
        assert [s["citation"] for s in args[3]] == [1, 2]
        assert "create your account" in args[3][0]["text"]
        assert "tuition" in args[3][1]["text"]
        return "Application steps [1]. Tuition [2].", "generated"

    monkeypatch.setattr(api, "generate_answer", generate)
    response = client.post("/api/chat", json={"question": "How do I apply and what is tuition?"})
    assert response.status_code == 200
    assert searched == queries
    assert "](https://nu.edu.eg/apply-now)" in response.json()["answer"]


def test_planner_preserves_distinct_subquestions(monkeypatch):
    queries = ["NU undergraduate application steps", "NU undergraduate tuition"]
    monkeypatch.setattr(
        generation,
        "call_model",
        lambda *a, **k: json.dumps(
            {
                "intent": "university",
                "meaning": "How do I apply and how much is tuition?",
                "queries": queries,
            }
        ),
    )
    plan = generation.plan_query("How do I apply and how much is tuition?", "en", [])
    assert plan["queries"] == queries and plan["route"] == "university"


def test_multiple_nu_questions_without_general_part_do_not_get_general_notice(monkeypatch):
    monkeypatch.setattr(
        generation,
        "call_model",
        lambda *a, **k: json.dumps(
            {
                "intent": "mixed",
                "meaning": "How do I apply and what is tuition?",
                "queries": ["NU application steps", "NU tuition"],
                "general_question": "",
            }
        ),
    )
    plan = generation.plan_query("How do I apply and what is tuition?", "en", [])
    assert plan["route"] == "university" and not plan["general_information"]


def test_history_cannot_make_general_notice_repeat_on_thanks(monkeypatch):
    from nu_chat.persona import GENERAL_NOTE

    monkeypatch.setattr(
        generation, "call_model", lambda *a, **k: "You're welcome!\n\n" + GENERAL_NOTE["en"]
    )
    answer, _ = generation.generate_answer("Thanks", "en", [], [], True, route="general")
    assert answer == "You're welcome!"
