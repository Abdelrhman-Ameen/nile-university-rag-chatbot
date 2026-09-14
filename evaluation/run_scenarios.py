"""Run 100 real HTTP scenarios, preserving complete conversations and timings.

Mechanical checks are regression signals. Each scenario also supplies an explicit
manual-review rubric; passing keywords is not a factual-quality certification.
"""

import argparse
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

import httpx

CHECKER_VERSION = sha256(Path(__file__).read_bytes()).hexdigest()[:16]


def check(step, status, result):
    errors = []
    expected_status = step.get("status", 200)
    if status != expected_status:
        return [f"HTTP {status}; expected {expected_status}: {result.get('detail', '')}"]
    if expected_status != 200:
        return errors
    answer = result.get("answer", "")
    pipeline = result.get("pipeline", {})
    if not answer.strip():
        errors.append("empty answer")
    if step.get("route") and pipeline.get("route") != step["route"]:
        errors.append("wrong route")
    if step.get("language") and pipeline.get("reply_language") != step["language"]:
        errors.append("wrong language")
    if (
        "general_information" in step
        and pipeline.get("general_information") != step["general_information"]
    ):
        errors.append("wrong specialization-note decision")
    normalized = answer.lower().replace(",", "")
    for phrase in step.get("required", []):
        if phrase.lower().replace(",", "") not in normalized:
            errors.append("missing: " + phrase)
    if step.get("any_of") and not any(p.lower() in answer.lower() for p in step["any_of"]):
        errors.append("missing expected content")
    for phrase in step.get("forbidden", []):
        if phrase.lower() in answer.lower():
            errors.append("unwanted: " + phrase)
    sources = result.get("sources", [])
    citations = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
    if not citations <= {s["citation"] for s in sources}:
        errors.append("invalid citation")
    if pipeline.get("route") in {"general", "identity"} and sources:
        errors.append("unnecessary university retrieval")
    if result.get("mode") == "generated" and not citations:
        errors.append("uncited university answer")
    if pipeline.get("reply_language") == "franco" and re.search(
        r"\b(bghit|shno|daba|wach)\b", answer, re.I
    ):
        errors.append("non-Egyptian Franco")
    # Check actual prose, not just the model's declared language or the app's footer.
    prose = re.split(
        r"\n\n(?:I'm built specifically|أنا معمول مخصوص|Ana ma3mool makhsoos)", answer
    )[0]
    prose = re.sub(r"```[\s\S]*?```|`[^`]*`", "", prose)
    arabic = len(re.findall(r"[\u0621-\u064a]", prose))
    latin = len(re.findall(r"[A-Za-z]", prose))
    language = pipeline.get("reply_language")
    if language == "ar" and latin + arabic > 40 and arabic / (latin + arabic) < 0.3:
        errors.append("Arabic reply is mostly Latin-script prose")
    if language == "franco":
        if arabic > 15:
            errors.append("Franco reply contains Arabic-script prose")
        hints = re.findall(
            r"\b(?:el|mesh|3ayez|eh|ezay|3ala|men|ya3ni|fi|le|w|enak)\b", prose, re.I
        )
        if len(prose.split()) > 20 and len(hints) < 2:
            errors.append("reply may be English rather than Franco; manual review required")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--output", default="data/scenarios-100.json")
    parser.add_argument("--ids", help="Comma-separated IDs to rerun")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    cases = json.loads(Path(__file__).with_name("scenarios_100.json").read_text(encoding="utf-8"))
    assert len(cases) == 100 and len({c["id"] for c in cases}) == 100
    if args.ids:
        cases = [c for c in cases if c["id"] in args.ids.split(",")]
    output = Path(args.output)
    previous = (
        json.loads(output.read_text(encoding="utf-8")) if args.resume and output.exists() else {}
    )
    rows = previous.get("cases", [])
    done = {c["id"] for c in rows}
    client = httpx.Client(timeout=360, transport=httpx.HTTPTransport(retries=2))
    health = client.get(args.url + "/api/health", timeout=60).json()

    def request(step, history):
        body = step.get(
            "payload",
            {
                "question": step["question"],
                "history": history,
                "language": step.get("reply_language", "auto"),
            },
        )
        started = time.perf_counter()
        try:
            response = client.post(args.url + "/api/chat", json=body)
            result = response.json()
            return {
                "question": body.get("question"),
                "status": response.status_code,
                "seconds": round(time.perf_counter() - started, 2),
                "result": result,
                "errors": check(step, response.status_code, result),
            }
        except (httpx.HTTPError, ValueError) as exc:
            return {
                "question": body.get("question"),
                "status": None,
                "seconds": round(time.perf_counter() - started, 2),
                "result": {},
                "errors": [str(exc)],
            }

    def save():
        report = {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "checker_version": CHECKER_VERSION,
            "health": health,
            "total": len(rows),
            "mechanical_passes": sum(not r["errors"] for r in rows),
            "manual_review_required": True,
            "cases": rows,
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_suffix(".tmp")
        temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        temporary.replace(output)

    for case in cases:
        if case["id"] in done:
            continue
        environment = client.get(args.url + "/api/health", timeout=60).json()
        history, turns = [], []
        if case.get("concurrent"):
            with ThreadPoolExecutor(max_workers=len(case["steps"])) as pool:
                futures = [pool.submit(request, step, []) for step in case["steps"]]
                turns = [future.result() for future in futures]
        else:
            for step in case["steps"]:
                turn = request(step, history)
                turns.append(turn)
                if turn["status"] == 200:
                    history.extend(
                        [
                            {"role": "user", "content": str(turn["question"])},
                            {"role": "assistant", "content": turn["result"]["answer"][:5000]},
                        ]
                    )
                    history = history[-12:]
        errors = [f"turn {i + 1}: {error}" for i, t in enumerate(turns) for error in t["errors"]]
        rows.append(
            {
                "id": case["id"],
                "environment": environment,
                "tags": case["tags"],
                "review": case["review"],
                "errors": errors,
                "turns": turns,
            }
        )
        save()
        print(
            case["id"],
            "FAIL" if errors else "PASS",
            "; ".join(errors),
            f"({sum(t['seconds'] for t in turns):.1f}s)",
            flush=True,
        )
    print(f"{len(rows)} scenarios recorded in {output}. Review full answers and cited passages.")
    client.close()


if __name__ == "__main__":
    main()
