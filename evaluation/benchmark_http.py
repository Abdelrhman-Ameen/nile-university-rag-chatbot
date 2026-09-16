"""Repeatable real HTTP latency probe; preserves answers for quality review."""

import argparse
import json
import statistics
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from uuid import uuid4

import httpx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()
    report = {"requests": [], "health": []}
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    stopped = threading.Event()
    with httpx.Client(base_url=args.base_url, timeout=360, trust_env=False) as client:
        report["server"] = client.get("/api/health").json()

        def health_probe():
            while not stopped.is_set():
                started = time.perf_counter()
                try:
                    response = client.get("/api/health", timeout=5)
                    row = {"status": response.status_code}
                except httpx.HTTPError as exc:
                    row = {"error": repr(exc)}
                report["health"].append({**row, "seconds": time.perf_counter() - started})
                stopped.wait(0.5)

        def ask(label, question, request_id=None):
            started = time.perf_counter()
            try:
                response = client.post(
                    "/api/chat",
                    json={
                        "request_id": request_id or str(uuid4()),
                        "question": question,
                    },
                )
                row = {
                    "label": label,
                    "question": question,
                    "status": response.status_code,
                    "result": response.json(),
                }
            except httpx.HTTPError as exc:
                row = {"label": label, "question": question, "error": repr(exc)}
            row["seconds"] = round(time.perf_counter() - started, 3)
            report["requests"].append(row)
            print(label, row.get("status", "error"), row["seconds"], flush=True)

        probe = threading.Thread(target=health_probe)
        probe.start()
        try:
            for label, question in [
                ("identity", "انت مين؟"),
                ("general", "Explain recursion in one short paragraph."),
                ("fees", "مصروفات حاسبات ومعلومات كام قبل الخصم؟"),
                ("location", "Where is Nile University in Egypt?"),
                ("advice", "هل الجامعة كويسة لدراسة حاسبات؟"),
                ("bus-live", "How many NU bus seats are left right now?"),
                ("library-live", "How many NU library copies are available this minute?"),
                ("fees-repeat", "مصروفات حاسبات ومعلومات كام قبل الخصم؟"),
            ]:
                ask(label, question)
            request_id = str(uuid4())
            with ThreadPoolExecutor(max_workers=3) as pool:
                jobs = [
                    pool.submit(ask, "overlap-one", "What is UGRF?", request_id),
                    pool.submit(ask, "overlap-retry", "What is UGRF?", request_id),
                    pool.submit(ask, "overlap-next", "Say hello in Arabic"),
                ]
                for job in jobs:
                    job.result()
        finally:
            stopped.set()
            probe.join()
            health_times = sorted(row["seconds"] for row in report["health"])
            report["health_summary"] = {
                "count": len(health_times),
                "median": statistics.median(health_times),
                "p95": health_times[int(0.95 * (len(health_times) - 1))],
                "errors": sum(row.get("status") != 200 for row in report["health"]),
            }
            target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            print(report["health_summary"], flush=True)


if __name__ == "__main__":
    main()
