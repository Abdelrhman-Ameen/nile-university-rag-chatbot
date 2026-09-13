"""Small, hand-authored development set; results are not a research benchmark."""

import json
from datetime import datetime, timezone

from nu_chat.config import DATA_DIR, ROOT
from nu_chat.generation import model_available, normalize_query
from nu_chat.language import detect_language
from nu_chat.retrieval import Retriever


def evaluate(with_llm: bool = False) -> dict:
    cases = json.loads((ROOT / "evaluation/questions.json").read_text(encoding="utf-8"))
    if with_llm and not model_available():
        raise RuntimeError("Qwen must be running for --with-llm evaluation")
    retriever = Retriever()
    rows = []
    for case in cases:
        language = detect_language(case["question"])
        query, route = normalize_query(case["question"], language, [], with_llm)
        hits = retriever.search(query, original=case["question"])
        rank = next(
            (
                i
                for i, hit in enumerate(hits, 1)
                if any(term in hit["url"].lower() for term in case["expected_url_terms"])
            ),
            0,
        )
        rows.append(
            {
                **case,
                "detected": language,
                "query": query,
                "normalization": route,
                "hit_at_5": bool(rank),
                "reciprocal_rank": 1 / rank if rank else 0,
                "rejected": not hits,
                "top_urls": [h["url"] for h in hits],
            }
        )
    answerable = [r for r in rows if not r.get("unanswerable")]
    unanswerable = [r for r in rows if r.get("unanswerable")]
    report = {
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "with_llm": with_llm,
        "note": "Development set: URL-level relevance labels, not full answer correctness or Franco fluency.",
        "classification_accuracy": sum(r["detected"] == r["language"] for r in rows) / len(rows),
        "hit_at_5": sum(r["hit_at_5"] for r in answerable) / len(answerable),
        "mrr_at_5": sum(r["reciprocal_rank"] for r in answerable) / len(answerable),
        "unanswerable_rejection_rate": sum(r["rejected"] for r in unanswerable) / len(unanswerable),
        "cases": rows,
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filename = "evaluation-qwen.json" if with_llm else "evaluation-baseline.json"
    (DATA_DIR / filename).write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {k: v for k, v in report.items() if k != "cases"}
