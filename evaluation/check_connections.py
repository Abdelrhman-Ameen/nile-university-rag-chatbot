"""Real socket test: drop an SSE connection, reconnect, and immediately send again."""

import argparse
import json
import time
from pathlib import Path
from uuid import uuid4

import httpx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="evaluation/runs/connections-optimized.json")
    args = parser.parse_args()
    report = {"events": []}
    with httpx.Client(base_url="http://127.0.0.1:8000", timeout=240, trust_env=False) as client:
        report["server"] = client.get("/api/health").json()
        body = {
            "question": "What are the ITCS tuition fees before scholarships?",
            "request_id": str(uuid4()),
        }
        start = time.perf_counter()
        with client.stream("POST", "/api/chat/stream", json=body) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line.startswith("data: "):
                    event = json.loads(line[6:])
                    report["first_event_seconds"] = round(time.perf_counter() - start, 4)
                    report["events"].append(event)
                    assert "stage" in event, event
                    break  # Closing the response intentionally interrupts the socket.
        with client.stream("POST", "/api/chat/stream", json=body) as response:
            for line in response.iter_lines():
                if line.startswith("data: "):
                    event = json.loads(line[6:])
                    if "answer" in event:
                        report["result"] = event
                        break
                    report["events"].append(event)
        report["completion_seconds"] = round(time.perf_counter() - start, 3)
        assert "result" in report, report
        before = time.perf_counter()
        replay = client.post("/api/chat", json=body)
        report["replay_seconds"] = round(time.perf_counter() - before, 4)
        assert replay.status_code == 200 and replay.json() == report["result"]
        report["queue_after_result"] = client.get("/api/health").json()["queue"]
        assert not report["queue_after_result"]["active"]
        before = time.perf_counter()
        next_response = client.post(
            "/api/chat", json={"question": "شكرا", "request_id": str(uuid4())}
        )
        report["next_seconds"] = round(time.perf_counter() - before, 3)
        report["next_status"] = next_response.status_code
        report["next_result"] = next_response.json()
        assert next_response.status_code == 200
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in report.items() if k not in {"result", "next_result", "server"}},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
