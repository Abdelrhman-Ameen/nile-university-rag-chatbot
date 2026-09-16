"""Run each stage independently: python -m nu_chat --help."""

import argparse
import json


def main():
    parser = argparse.ArgumentParser(description="Nile Guide: collect, embed, retrieve, generate")
    parser.add_argument(
        "command",
        choices=["collect", "ocr", "index", "ingest", "serve", "evaluate", "train-intent"],
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="Maximum new URL requests; 0 drains the public frontier",
    )
    parser.add_argument(
        "--no-sitemaps", action="store_true", help="Use seeds and discovered links only"
    )
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--refresh", action="store_true", help="Refetch cached pages")
    parser.add_argument(
        "--document-images-only",
        action="store_true",
        help="Limit OCR to images identified as documents; default checks all content images",
    )
    parser.add_argument(
        "--max-images", type=int, default=0, help="Image OCR limit; 0 processes all selected images"
    )
    parser.add_argument(
        "--reviewed-only",
        action="store_true",
        help="Refresh only content-hash-checked reviewed images; skip automatic OCR and PDFs",
    )
    parser.add_argument(
        "--with-llm", action="store_true", help="Use local model normalization during evaluation"
    )
    args = parser.parse_args()
    if args.max_pages < 0:
        parser.error("--max-pages cannot be negative")
    if args.command in {"train-intent", "ingest"}:
        from nu_chat.intent import train_intent

        print(json.dumps(train_intent(), indent=2))
    if args.command in {"collect", "ingest"}:
        from nu_chat.collect import collect

        report = collect(args.max_pages, not args.no_sitemaps, refresh=args.refresh)
        print(json.dumps({k: v for k, v in report.items() if k != "skipped"}, indent=2))
    if args.command in {"ocr", "ingest"}:
        from nu_chat.ocr import extract_images

        result = extract_images(
            not args.document_images_only,
            args.max_images,
            refresh=args.refresh,
            reviewed_only=args.reviewed_only,
        )
        print(json.dumps({k: v for k, v in result.items() if k != "results"}, indent=2))
    if args.command in {"index", "ingest"}:
        from nu_chat.retrieval import build_index

        print(json.dumps(build_index(), indent=2))
    if args.command == "serve":
        import os

        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
        import uvicorn

        # One process owns the GPU and reconnect cache. Additional workers would
        # duplicate model memory and route retries to unrelated caches.
        uvicorn.run(
            "nu_chat.api:app",
            host="127.0.0.1",
            port=args.port,
            timeout_keep_alive=30,
            timeout_graceful_shutdown=240,
        )
    if args.command == "evaluate":
        from nu_chat.evaluate import evaluate

        print(json.dumps(evaluate(args.with_llm), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
