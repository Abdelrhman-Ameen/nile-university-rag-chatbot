"""Run tagged HTTP regressions against a real running app; inspect the saved answers too.

Usage: python evaluation/check_chat.py --output data/chat-check.json
These checks catch routing/citation regressions, not every hallucination or language error.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import httpx


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--output", default="data/chat-check.json")
    parser.add_argument("--tag", help="Run only cases with this tag")
    args = parser.parse_args()
    cases = json.loads(Path(__file__).with_name("chat_cases.json").read_text(encoding="utf-8"))
    rows = []
    with httpx.Client(timeout=240) as client:
        health = client.get(args.url + "/api/health").json()
        for case in cases:
            if args.tag and args.tag not in case["tags"]:
                continue
            errors, result = [], {}
            try:
                response = client.post(
                    args.url + "/api/chat",
                    json={
                        "question": case["question"],
                        "history": case.get("history", []),
                    },
                )
                response.raise_for_status()
                result = response.json()
                answer = result["answer"]
                if result["pipeline"]["route"] != case["route"]:
                    errors.append("wrong route")
                if result["pipeline"]["reply_language"] != case["language"]:
                    errors.append("wrong language routing")
                if not answer.strip():
                    errors.append("empty answer")
                if case.get("any_of") and not any(
                    x.lower() in answer.lower() for x in case["any_of"]
                ):
                    errors.append("missing expected content")
                if any(x.lower() not in answer.lower() for x in case.get("all_of", [])):
                    errors.append("missing requested topic")
                if any(x.lower() in answer.lower() for x in case.get("forbidden", [])):
                    errors.append("unwanted content")
                sources = result["sources"]
                if case["route"] == "general" and sources:
                    errors.append("general answer has university sources")
                if any(
                    not (
                        (urlsplit(s["url"]).hostname or "") == "nu.edu.eg"
                        or (urlsplit(s["url"]).hostname or "").endswith(".nu.edu.eg")
                    )
                    for s in sources
                ):
                    errors.append("non-Egypt source")
                if case["route"] != "general":
                    cited = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
                    if not cited <= {s["citation"] for s in sources}:
                        errors.append("invalid citations")
                    if result["mode"] == "generated" and not cited:
                        errors.append("missing citations")
            except (httpx.HTTPError, ValueError, KeyError) as exc:
                errors.append(str(exc))
            rows.append(
                {
                    "id": case["id"],
                    "tags": case["tags"],
                    "question": case["question"],
                    "errors": errors,
                    "result": result,
                }
            )
            print(f"{case['id']}: {'FAIL ' + ', '.join(errors) if errors else 'PASS'}", flush=True)
    if not rows:
        raise SystemExit("No cases matched")
    report = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "health": health,
        "passed": sum(not r["errors"] for r in rows),
        "total": len(rows),
        "cases": rows,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{report['passed']}/{len(rows)} checks passed. Inspect answers in {output}.")
    return 0 if report["passed"] == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
