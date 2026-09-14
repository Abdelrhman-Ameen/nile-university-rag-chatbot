"""A small supervised intent head on frozen Sentence-BERT embeddings.

Training examples and development validation examples are kept separate. This does not train
the generator or teach the encoder university facts; it learns conversation routing.
"""

import json
from functools import lru_cache
from hashlib import sha256

import numpy as np

from nu_chat.config import DATA_DIR, EMBEDDING_MODEL, ROOT
from nu_chat.language import FRANCO_HINTS, tokens
from nu_chat.retrieval import encoder

INTENT_FILE = DATA_DIR / "intent_classifier.npz"
POLICIES = {
    "identity": ("identity", False),
    "social": ("general", False),
    "emotion": ("general", False),
    "opinion": ("general", False),
    "university_advice": ("advising", False),
    "general_information": ("general", True),
    "creative": ("general", False),
    "university": ("university", False),
    "mixed": ("mixed", True),
    "followup": (None, None),
}


def decision(probabilities, classes) -> dict:
    grouped = {}
    for label, probability in zip(classes, probabilities):
        policy = POLICIES[label]
        grouped[policy] = grouped.get(policy, 0) + float(probability)
    ordered = sorted(grouped.items(), key=lambda item: item[1], reverse=True)
    policy, score = ordered[0]
    margin = score - ordered[1][1]
    eligible = [
        (label, float(p)) for label, p in zip(classes, probabilities) if POLICIES[label] == policy
    ]
    label, intent_score = max(eligible, key=lambda item: item[1])
    return {
        "label": label,
        "intent_score": round(intent_score, 4),
        "score": round(score, 4),
        "margin": round(margin, 4),
        "confident": score >= (0.9 if policy[0] == "advising" else 0.65)
        and margin >= 0.2
        and policy[0] is not None,
        "route": policy[0],
        "general_information": policy[1],
    }


def classifier_text(text: str) -> str:
    hints = list(dict.fromkeys(FRANCO_HINTS[w] for w in tokens(text) if w in FRANCO_HINTS))
    return text.strip() + ("\nMeaning hints: " + "; ".join(hints) if hints else "")


def features(texts: list[str]) -> np.ndarray:
    from sklearn.feature_extraction.text import HashingVectorizer

    prepared = [classifier_text(text) for text in texts]
    semantic = encoder().encode(
        prepared, normalize_embeddings=True, batch_size=32, show_progress_bar=False
    )
    # Short spellings and Arabic/Franco verbs carry intent as well as semantic meaning.
    lexical = HashingVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        n_features=8192,
        alternate_sign=False,
        dtype=np.float32,
    ).transform(prepared)
    return np.concatenate([semantic, lexical.toarray()], axis=1)


def train_intent() -> dict:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import classification_report, confusion_matrix

    examples_path = ROOT / "evaluation" / "intent_examples.json"
    raw = examples_path.read_bytes()
    examples = json.loads(raw)
    train = [(text, label) for label, texts in examples["train"].items() for text in texts]
    test = [(text, label) for label, texts in examples["validation"].items() for text in texts]
    normalized_train = {" ".join(tokens(text)) for text, _ in train}
    assert not normalized_train & {" ".join(tokens(text)) for text, _ in test}
    for suite in ("scenarios_100.json", "screenshot_regressions.json"):
        cases = json.loads((ROOT / "evaluation" / suite).read_text(encoding="utf-8"))
        prompts = {" ".join(tokens(step["question"])) for case in cases for step in case["steps"]}
        assert not normalized_train & prompts, "Training overlaps the chat regression suite"
    vectors = features([text for text, _ in train + test])
    head = LogisticRegression(C=15, class_weight="balanced", max_iter=2000)
    head.fit(vectors[: len(train)], [label for _, label in train])
    probabilities = head.predict_proba(vectors[len(train) :])
    predicted = head.classes_[probabilities.argmax(axis=1)]
    rows = []
    for (text, expected), actual, probs in zip(test, predicted, probabilities):
        ordered = np.sort(probs)
        rows.append(
            {
                "text": text,
                "expected": expected,
                "predicted": str(actual),
                "score": round(float(ordered[-1]), 4),
                "margin": round(float(ordered[-1] - ordered[-2]), 4),
                "correct": expected == actual,
                "decision": decision(probs, head.classes_),
                "policy_correct": (
                    decision(probs, head.classes_)["route"],
                    decision(probs, head.classes_)["general_information"],
                )
                == POLICIES[expected],
            }
        )
    metadata = {
        "model": EMBEDDING_MODEL,
        "classes": head.classes_.tolist(),
        "examples_sha256": sha256(raw).hexdigest(),
        "version": 2,
        "train_count": len(train),
        "validation_count": len(test),
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temporary = INTENT_FILE.with_suffix(".tmp")
    with temporary.open("wb") as output:
        np.savez_compressed(
            output,
            weights=head.coef_.astype(np.float32),
            intercept=head.intercept_.astype(np.float32),
            metadata=json.dumps(metadata),
        )
    temporary.replace(INTENT_FILE)
    report = {
        **metadata,
        "classification": classification_report(
            [y for _, y in test], predicted, output_dict=True, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(
            [y for _, y in test], predicted, labels=head.classes_
        ).tolist(),
        "cases": rows,
        "note": "Authored development validation set used for tuning, not a blind production test. Scores are not calibrated probabilities of correctness.",
    }
    (DATA_DIR / "intent_evaluation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {
        "train_count": len(train),
        "validation_count": len(test),
        "accuracy": report["classification"]["accuracy"],
    }


@lru_cache(maxsize=1)
def _load_head(modified: int):
    with np.load(INTENT_FILE, allow_pickle=False) as data:
        weights, intercept = data["weights"].copy(), data["intercept"].copy()
        metadata = json.loads(str(data["metadata"]))
    if metadata["model"] != EMBEDDING_MODEL or metadata["version"] != 2:
        raise ValueError("Intent encoder changed. Run: python -m nu_chat train-intent")
    return weights, intercept, metadata


def classify_intent(question: str) -> dict:
    weights, intercept, metadata = _load_head(INTENT_FILE.stat().st_mtime_ns)
    vector = features([question])[0]
    scores = weights @ vector + intercept
    probabilities = np.exp(scores - scores.max())
    probabilities /= probabilities.sum()
    return {
        **decision(probabilities, metadata["classes"]),
        "model": EMBEDDING_MODEL,
        "head_version": metadata["examples_sha256"][:16],
    }
