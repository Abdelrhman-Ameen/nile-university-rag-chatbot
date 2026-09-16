"""Replay the known failed/partial cases after repairs; this is not a new blind score."""

import argparse
import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent / "independent_2026_09_16" / "suite.json"
CASE_IDS = {
    "I002",
    "I006",
    "I010",
    "I011",
    "I014",
    "I018",
    "I020",
    "I024",
    "I025",
    "I038",
    "I039",
    "I042",
    "I051",
    "I054",
    "I057",
    "I060",
    "I070",
    "I073",
    "I074",
    "I075",
    "I077",
    "I078",
    "I079",
    "I080",
    "I081",
    "I082",
    "I084",
    "I085",
    "I088",
    "I090",
    "I092",
    "I094",
    "I097",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8001")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ids", help="Optional comma-separated subset of known regression IDs")
    args = parser.parse_args()
    selected_ids = set(args.ids.split(",")) if args.ids else CASE_IDS
    if not selected_ids <= CASE_IDS:
        raise RuntimeError(f"Unknown regression IDs: {sorted(selected_ids - CASE_IDS)}")
    cases = [
        case
        for case in json.loads(SUITE.read_text(encoding="utf-8"))
        if case["id"] in selected_ids
    ]
    if len(cases) != len(selected_ids):
        raise RuntimeError("Regression IDs do not match the frozen suite")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream, httpx.Client(
        timeout=360, trust_env=False
    ) as client:
        health = client.get(args.url + "/api/health", timeout=15).json()
        if not all(health.get(key) for key in ("ready", "model_ready", "index_ready")):
            raise RuntimeError(f"Service is not ready: {health}")
        for case in cases:
            body = {
                "question": case["question"],
                "history": case["history"],
                "language": "auto",
                "request_id": str(uuid.uuid4()),
            }
            started = time.perf_counter()
            response = client.post(args.url + "/api/chat", json=body)
            row = {
                "id": case["id"],
                "expectation": case["expectation"],
                "started_at": now(),
                "status": response.status_code,
                "seconds": round(time.perf_counter() - started, 3),
                "request": body,
                "result": response.json(),
            }
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            stream.flush()
            print(case["id"], response.status_code, row["seconds"], flush=True)


if __name__ == "__main__":
    main()
