"""Local image/scan OCR, with content-hash-checked reviewed table transcriptions.

OCR is an ingestion stage, never an extra model call during chat. Raw word boxes
and confidence scores stay in the cache for inspection. A score is not a claim
that the transcription or its interpretation is correct.
"""

import io
import json
import re
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from uuid import uuid4

import numpy as np

from nu_chat.collect import Collector, canonical_url
from nu_chat.config import DATA_DIR, ROOT
from nu_chat.crawl import atomic_json, replace_file


def readable_rows(boxes, texts) -> str:
    """Keep cells on the same horizontal row together, in their visual order."""
    rows = []
    for box, text in sorted(zip(boxes, texts), key=lambda item: float(np.mean(item[0][:, 1]))):
        y = float(np.mean(box[:, 1]))
        height = float(np.max(box[:, 1]) - np.min(box[:, 1]))
        if rows and abs(rows[-1][0] - y) <= max(4, height * 0.45):
            rows[-1][1].append((float(np.min(box[:, 0])), text))
        else:
            rows.append((y, [(float(np.min(box[:, 0])), text)]))
    return "\n".join(" | ".join(t for _, t in sorted(cells)) for _, cells in rows)


def pdf_reading_order(record: dict, width: int, height: int) -> str:
    """Separate facing pages with a clear gutter and substantial prose on both sides."""
    text = "\n".join(s["text"] for s in record["sections"])
    boxes = np.asarray(record.get("boxes", []))
    if width < height * 1.3 or len(boxes) < 8:
        return text
    left = np.max(boxes[:, :, 0], axis=1) < width * 0.49
    right = np.min(boxes[:, :, 0], axis=1) > width * 0.51
    # Tables generally have short cells; do not turn their columns into separate lists.
    prose = np.ptp(boxes[:, :, 0], axis=1) > width * 0.2
    if not np.all(left | right) or min(sum(left & prose), sum(right & prose)) < 4:
        return text
    texts = np.asarray(record["texts"])
    return "\n\n".join(
        f"## {label}\n" + readable_rows(boxes[mask], texts[mask])
        for label, mask in (("Left page", left), ("Right page", right))
    )


def extract_images(
    all_images: bool = True,
    max_images: int = 0,
    refresh: bool = False,
    reviewed_only: bool = False,
) -> dict:
    from rapidocr import LangRec, ModelType, OCRVersion, RapidOCR

    config = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    collector = Collector(config["allowed_domains"])
    cache_dir = DATA_DIR / "crawl"
    ocr_dir = cache_dir / "ocr"
    ocr_dir.mkdir(parents=True, exist_ok=True)
    reviewed_path = ROOT / "sources" / "reviewed_images.json"
    reviewed = (
        json.loads(reviewed_path.read_text(encoding="utf-8")) if reviewed_path.exists() else []
    )
    verified = {row["sha256"]: row for row in reviewed}
    assets = json.loads((cache_dir / "assets.json").read_text(encoding="utf-8"))
    assets.extend(
        {
            "url": r["asset_url"],
            "source_url": r["source_url"],
            "source_title": r["source_title"],
            "section": r["section"],
            "ocr_candidate": True,
            "alt": r["section"],
        }
        for r in reviewed
    )
    # Process likely documents before photographs; all public images are still eligible.
    reviewed_urls = {r["asset_url"] for r in reviewed}
    assets.sort(key=lambda a: (a["url"] not in reviewed_urls, not a.get("ocr_candidate", False)))
    documents, statuses, seen = {}, [], set()
    output = DATA_DIR / "ocr_documents.jsonl"
    if output.exists():
        documents = {
            d["id"]: d
            for line in output.read_text(encoding="utf-8").splitlines()
            if line and (d := json.loads(line))
        }
    engines = threading.local()

    def recognize(body):
        digest = sha256(body).hexdigest()
        cache = ocr_dir / (digest + ".en-ar-v1.json")
        if digest in verified:
            return digest, {"sections": verified[digest]["sections"], "reviewed": True}
        if cache.exists():
            return digest, json.loads(cache.read_text(encoding="utf-8"))
        engine = getattr(engines, "english", None)
        if engine is None:
            engine = RapidOCR(
                params={
                    "EngineConfig.onnxruntime.intra_op_num_threads": 2,
                    "EngineConfig.onnxruntime.inter_op_num_threads": 1,
                }
            )
            engines.english = engine
        result = engine(body)
        arabic_engine = getattr(engines, "arabic", None)
        if arabic_engine is None:
            arabic_engine = RapidOCR(
                params={
                    "Rec.lang_type": LangRec.ARABIC,
                    "Rec.ocr_version": OCRVersion.PPOCRV5,
                    "Rec.model_type": ModelType.MOBILE,
                    "EngineConfig.onnxruntime.intra_op_num_threads": 2,
                    "EngineConfig.onnxruntime.inter_op_num_threads": 1,
                }
            )
            engines.arabic = arabic_engine
        arabic = arabic_engine(body)
        items = [
            (box, text, score)
            for box, text, score in zip(
                result.boxes if result.boxes is not None else [],
                result.txts or [],
                result.scores or [],
            )
            if score >= 0.7 and not re.search(r"[\u4e00-\u9fff]", text)
        ]
        for box, text, score in zip(
            arabic.boxes if arabic.boxes is not None else [], arabic.txts or [], arabic.scores or []
        ):
            if score < 0.7 or len(re.findall(r"[\u0600-\u06ff]", text)) < 3:
                continue
            center = np.mean(box, axis=0)
            items = [
                item for item in items if np.linalg.norm(np.mean(item[0], axis=0) - center) > 12
            ]
            items.append((box, text, score))
        boxes = np.array([item[0] for item in items])
        texts = [item[1] for item in items]
        text = readable_rows(boxes, texts)
        record = {
            "sections": [{"title": "Image text", "text": text}],
            "reviewed": False,
            "boxes": boxes.tolist(),
            "texts": list(texts),
            "scores": [item[2] for item in items],
            "engines": ["PP-OCRv6", "PP-OCRv5 Arabic"],
        }
        atomic_json(cache, record)
        return digest, record

    def save():
        temporary = output.with_suffix(".tmp")
        temporary.write_text(
            "\n".join(json.dumps(d, ensure_ascii=False) for d in documents.values()),
            encoding="utf-8",
        )
        replace_file(temporary, output)
        report = {
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "documents": len(documents),
            "reviewed_documents": sum(d.get("ocr_reviewed", False) for d in documents.values()),
            "processed": len(statuses),
            "results": statuses,
            "scope": "Public crawl images and every page of cached PDFs, including images inside pages with a text layer. Automatic OCR is not manually verified.",
        }
        atomic_json(DATA_DIR / "ocr_report.json", report)
        return report

    def pdf_pages():
        """Read every cached PDF page so mixed text/image documents are covered too."""
        import pypdfium2 as pdfium

        database_path = cache_dir / "cache.sqlite3"
        if not database_path.exists():
            return
        with sqlite3.connect(database_path) as database:
            sources = [json.loads(row[0]) for row in database.execute("SELECT result FROM pages")]
        visited = set()
        for source in sources:
            raw = source.get("raw_path")
            if not raw or not Path(raw).exists():
                continue
            with Path(raw).open("rb") as stream:
                if stream.read(5) != b"%PDF-":
                    continue
            url = source.get("final_url") or source["url"]
            if url in visited:
                continue
            visited.add(url)
            try:
                with pdfium.PdfDocument(raw) as pdf:
                    for number in range(len(pdf)):
                        job = {"url": url, "page": number + 1, "kind": "pdf-ocr"}
                        try:
                            page = pdf[number]
                            bitmap = page.render(scale=2)
                            buffer = io.BytesIO()
                            rendered = bitmap.to_pil()
                            width, height = rendered.size
                            rendered.save(buffer, format="PNG")
                            bitmap.close()
                            page.close()
                            digest, record = recognize(buffer.getvalue())
                            text = pdf_reading_order(record, width, height)
                            identifier = sha256(f"{url}#scan{number + 1}".encode()).hexdigest()[:16]
                            documents.pop(identifier, None)
                            if len(text.strip()) >= 60:
                                documents[identifier] = {
                                    "id": identifier,
                                    "url": url,
                                    "title": Path(url).name,
                                    "text": text,
                                    "page": number + 1,
                                    "kind": "pdf-ocr",
                                    "fetched_at": source["fetched_at"],
                                    "extracted_at": datetime.now(timezone.utc).isoformat(),
                                    "archived": "oldwebsite." in url,
                                    "content_sha256": digest,
                                    "ocr_reviewed": False,
                                }
                            statuses.append({**job, "status": "ok"})
                        except Exception as exc:
                            statuses.append({**job, "status": "error", "reason": str(exc)})
                        print(
                            f"PDF OCR [{len(statuses)}]: {statuses[-1]['status']} {url} page {number + 1}",
                            flush=True,
                        )
                        if len(statuses) % 20 == 0:
                            save()
            except Exception as exc:
                statuses.append(
                    {"url": url, "kind": "pdf-ocr", "status": "error", "reason": str(exc)}
                )

    def read_image(asset):
        safe = asset["url"]
        try:
            raw_path = ocr_dir / (sha256(safe.encode()).hexdigest() + ".image")
            if raw_path.exists() and not refresh:
                body = raw_path.read_bytes()
            else:
                _, body, _ = collector.fetch(safe, assets=True)
                temporary = raw_path.with_suffix(f".{uuid4().hex}.tmp")
                temporary.write_bytes(body)
                replace_file(temporary, raw_path)
            fetched_at = datetime.fromtimestamp(raw_path.stat().st_mtime, timezone.utc).isoformat()
            digest, record = recognize(body)
            if record["reviewed"]:
                asset = {**asset, **verified[digest]}
            return {
                "asset": asset,
                "url": safe,
                "status": "ok",
                "record": record,
                "digest": digest,
                "fetched_at": fetched_at,
            }
        except Exception as exc:
            return {"url": safe, "status": "error", "reason": str(exc)}

    def accept_image(result):
        nonlocal documents
        safe = result["url"]
        if result["status"] == "ok":
            asset, record = result["asset"], result["record"]
            documents = {key: d for key, d in documents.items() if d.get("asset_url") != safe}
            for index, section in enumerate(record["sections"]):
                # A short phone number, date or fee can be the whole useful image.
                if not section["text"].strip():
                    continue
                identifier = sha256(f"{safe}#{index}".encode()).hexdigest()[:16]
                documents[identifier] = {
                    "id": identifier,
                    "url": asset["source_url"],
                    "asset_url": safe,
                    "title": asset["source_title"]
                    + " — "
                    + asset["section"]
                    + " — "
                    + section["title"],
                    "text": section["text"],
                    "page": None,
                    "kind": "image",
                    "fetched_at": result["fetched_at"],
                    "extracted_at": datetime.now(timezone.utc).isoformat(),
                    "archived": asset.get("archived", False),
                    "content_sha256": result["digest"],
                    "ocr_reviewed": record["reviewed"],
                }
            statuses.append({"url": safe, "status": "ok", "reviewed": record["reviewed"]})
        else:
            statuses.append(result)
        print(f"OCR [{len(statuses)}]: {result['status']} {safe}", flush=True)
        if len(statuses) % 20 == 0:
            save()

    try:
        selected = []
        for asset in assets:
            if reviewed_only and asset["url"] not in reviewed_urls:
                continue
            if not all_images and not asset.get("ocr_candidate"):
                continue
            safe = canonical_url(asset["url"], config["allowed_domains"], assets=True)
            if not safe or safe in seen:
                continue
            if max_images and len(seen) >= max_images:
                break
            seen.add(safe)
            selected.append({**asset, "url": safe})
        for asset in selected:
            if asset["url"] in reviewed_urls:
                accept_image(read_image(asset))
        if not reviewed_only:
            pdf_pages()
        # Each worker owns its OCR engines. Only this coordinator updates the corpus.
        remaining = [asset for asset in selected if asset["url"] not in reviewed_urls]
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(read_image, asset) for asset in remaining]
            for future in as_completed(futures):
                accept_image(future.result())
        return save()
    finally:
        save()
        collector.client.close()
