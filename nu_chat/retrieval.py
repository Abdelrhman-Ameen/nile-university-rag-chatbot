"""Token-aware chunks, normalized SBERT vectors, and a small hybrid retriever.

NumPy is sufficient for a university corpus: cosine search is a matrix multiply.
An atomic NPZ file contains both chunks and vectors, with no pickle loading.
"""

import json
import re
import threading
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

from nu_chat.config import (
    DATA_DIR,
    EMBEDDING_DEVICE,
    EMBEDDING_MODEL,
    MIN_SIMILARITY,
    RERANK_BATCH_SIZE,
    RERANK_MODEL,
    RETRIEVAL_THREADS,
    ROOT,
    TOP_K,
)
from nu_chat.evidence import general_tuition
from nu_chat.language import tokens

STOP_WORDS = set(
    "a an the of to in at for is are do does how what can i me my we you your with and or nile university nu".split()
)
ABBREVIATIONS = {
    "ITCS": "School of Information Technology and Computer Science",
    "EAS": "School of Engineering and Applied Sciences",
    "UGRF": "Undergraduate Research Forum",
    "WINC": "Wireless Intelligent Networks Center",
    "NISC": "Nanoelectronics Integrated Systems Center",
    "SESC": "Smart Engineering Systems Research Center",
    "CIS": "Center for Informatics Science",
    "IPTTO": "Intellectual Property and Technology Transfer Office",
    "OSP": "Office of Sponsored Programs",
    "FACT": "FESTO Authorized and Certified Training Centre",
    "SCE": "School of Continuing Education",
    "IECC": "Innovation Entrepreneurship and Competitiveness Centre",
}


def expand_abbreviations(text: str) -> str:
    # Rewrites often already contain "Full school name (ITCS)". Expanding both
    # copies overwhelms the topic and can rank individual courses above degree lists.
    for abbreviation, full_name in ABBREVIATIONS.items():
        if full_name.lower() in text.lower():
            text = re.sub(r"\(?\b" + abbreviation + r"\b\)?", "", text, flags=re.I)
    return re.sub(
        r"\b(" + "|".join(ABBREVIATIONS) + r")\b",
        lambda match: ABBREVIATIONS[match[0].upper()],
        text,
        flags=re.I,
    )


@lru_cache(maxsize=1)
def reranker():
    from sentence_transformers import CrossEncoder
    from torch.nn import Sigmoid

    if not RERANK_MODEL:
        return None
    configure_cpu_threads()
    return CrossEncoder(
        RERANK_MODEL, device=EMBEDDING_DEVICE, activation_fn=Sigmoid(), max_length=384
    )


def search_terms(text: str) -> list[str]:
    aliases = {
        "application": "apply",
        "applications": "apply",
        "applying": "apply",
        "admissions": "admission",
        "requirements": "requirement",
        "programs": "program",
        "major": "program",
        "majors": "program",
        "degree": "program",
        "degrees": "program",
        "scholarships": "scholarship",
        "discounts": "discount",
        "financials": "fees",
        "cost": "fees",
        "costs": "fees",
        "tuition": "fees",
        "students": "student",
        "steps": "step",
        "researchers": "researcher",
    }
    return [aliases.get(word, word) for word in tokens(text) if word not in STOP_WORDS]


@lru_cache(maxsize=1)
def configure_cpu_threads():
    import torch

    # Small inference batches get slower when competing with OCR for every CPU core.
    if EMBEDDING_DEVICE == "cpu":
        torch.set_num_threads(max(1, RETRIEVAL_THREADS))


@lru_cache(maxsize=1)
def encoder():
    from sentence_transformers import SentenceTransformer

    configure_cpu_threads()
    return SentenceTransformer(EMBEDDING_MODEL, device=EMBEDDING_DEVICE)


def chunk_document(
    document: dict, tokenizer, max_tokens: int = 92, overlap: int = 18
) -> list[dict]:
    if not 0 <= overlap < max_tokens:
        raise ValueError("Overlap must be smaller than chunk size")
    text = document["text"]
    # Split long pages on meaningful sections so a FAQ answer cannot borrow the
    # neighboring question's transfer/scholarship rules. Short pages stay whole.
    if len(text) > 1800 and "\n## " in text:
        sections = re.split(r"(?m)^##\s+", text)
        output = []
        for number, section in enumerate(sections):
            if not section.strip():
                continue
            heading, _, body = section.partition("\n")
            if not body.strip():
                continue
            output.extend(
                chunk_document(
                    {
                        **document,
                        "id": f"{document['id']}-s{number}",
                        "title": heading.strip() + " — " + document["title"],
                        "text": heading + "\n" + body.strip(),
                    },
                    tokenizer,
                    max_tokens,
                    overlap,
                )
            )
        if output:
            return output
    offsets = tokenizer(
        text, add_special_tokens=False, return_offsets_mapping=True, truncation=False, verbose=False
    )["offset_mapping"]
    chunks = []
    for start in range(0, len(offsets), max_tokens - overlap):
        end = min(start + max_tokens, len(offsets))
        excerpt = text[offsets[start][0] : offsets[end - 1][1]].strip()
        if excerpt:
            context_start = max(0, start - max_tokens)
            context_end = min(len(offsets), end + max_tokens)
            context = text[offsets[context_start][0] : offsets[context_end - 1][1]].strip()
            chunks.append(
                {**document, "id": f"{document['id']}-{start}", "text": excerpt, "context": context}
            )
        if end == len(offsets):
            break
    return chunks


def build_index() -> dict:
    corpus = DATA_DIR / "documents.jsonl"
    if not corpus.exists():
        raise RuntimeError("Collect sources first: python -m nu_chat collect")
    documents = [
        json.loads(line) for line in corpus.read_text(encoding="utf-8").splitlines() if line
    ]
    reviewed_path = ROOT / "sources" / "reviewed_documents.json"
    if reviewed_path.exists():
        documents.extend(json.loads(reviewed_path.read_text(encoding="utf-8")))
    ocr_corpus = DATA_DIR / "ocr_documents.jsonl"
    if ocr_corpus.exists():
        documents.extend(
            json.loads(line) for line in ocr_corpus.read_text(encoding="utf-8").splitlines() if line
        )
    model = encoder()
    chunks = [chunk for doc in documents for chunk in chunk_document(doc, model.tokenizer)]
    if not chunks:
        raise RuntimeError("The corpus has no usable text")
    # Reserve token space for the source title, so text is not silently truncated.
    texts = [
        model.tokenizer.decode(
            model.tokenizer.encode(
                c["title"], add_special_tokens=False, truncation=True, max_length=28
            )
        )
        + "\n"
        + c["text"]
        for c in chunks
    ]
    cached = {}
    index_path = DATA_DIR / "index.npz"
    if index_path.exists():
        with np.load(index_path, allow_pickle=False) as previous:
            old = json.loads(str(previous["metadata"]))
            if old["model"] == EMBEDDING_MODEL and old.get("encoding_version") == 1:
                cached = {
                    (c["title"], c["text"]): v.copy()
                    for c, v in zip(old["chunks"], previous["vectors"])
                }
    missing = [i for i, c in enumerate(chunks) if (c["title"], c["text"]) not in cached]
    if missing:
        encoded = model.encode(
            [texts[i] for i in missing],
            normalize_embeddings=True,
            show_progress_bar=True,
            batch_size=32,
        )
        cached.update(
            ((chunks[i]["title"], chunks[i]["text"]), v) for i, v in zip(missing, encoded)
        )
    vectors = np.array([cached[(c["title"], c["text"])] for c in chunks])
    metadata = {"model": EMBEDDING_MODEL, "encoding_version": 1, "chunks": chunks}
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp = DATA_DIR / "index.tmp"
    with temp.open("wb") as stream:
        np.savez_compressed(
            stream,
            vectors=vectors.astype("float32"),
            metadata=json.dumps(metadata, ensure_ascii=False),
        )
    temp.replace(DATA_DIR / "index.npz")
    # Download the reranker during setup rather than on the first user's question.
    reranker()
    return {
        "chunks": len(chunks),
        "documents": len(documents),
        "dimensions": vectors.shape[1],
        "new_embeddings": len(missing),
        "model": EMBEDDING_MODEL,
    }


class Retriever:
    def __init__(self, path: Path = DATA_DIR / "index.npz"):
        with np.load(path, allow_pickle=False) as data:
            self.vectors = data["vectors"].copy()
            metadata = json.loads(str(data["metadata"]))
        if metadata["model"] != EMBEDDING_MODEL:
            raise ValueError("Embedding model changed. Rebuild with: python -m nu_chat index")
        self.chunks = metadata["chunks"]
        self.bm25 = BM25Okapi([search_terms(c["title"] + " " + c["text"]) for c in self.chunks])
        self.title_terms = [set(search_terms(c["title"])) for c in self.chunks]
        self.lock = threading.Lock()
        # A new index creates a new Retriever and therefore an empty cache. Keep
        # every retrieval option in the key; callers receive independent dictionaries.
        self.cached_search = lru_cache(maxsize=128)(self._search)

    def search(
        self,
        query: str,
        original: str = "",
        k: int = TOP_K,
        meaning: str = "",
        prefer_text: bool = False,
    ) -> list[dict]:
        return deepcopy(self.cached_search(query, original, k, meaning, prefer_text))

    def _search(
        self,
        query: str,
        original: str = "",
        k: int = TOP_K,
        meaning: str = "",
        prefer_text: bool = False,
    ) -> list[dict]:
        query = expand_abbreviations(query)
        meaning = expand_abbreviations(meaning)
        program_list = bool(
            re.search(r"\b(programs?|majors?|degrees?)\b", query, re.I)
            and re.search(r"\b(undergraduate|bachelor|available|list|offered)\b", query, re.I)
            and not re.search(r"\b(courses?|modules?|curriculum)\b", query, re.I)
        )
        if re.search(
            r"\b(?:location|address|located)\b|\bwhere is (?:the )?(?:nile university|nu|university|campus)\b",
            query,
            re.I,
        ):
            query += " campus location address contact"
            meaning = query
        # This is a single-university corpus: the institution name can drown out the actual topic.
        focused = re.sub(
            r"\b(?:nile university|nu|in egypt)\b|جامعة النيل", "", query, flags=re.IGNORECASE
        )
        focused = re.sub(r"\s+", " ", focused).strip()
        if not search_terms(focused):
            focused = query
        with self.lock:
            vector = encoder().encode(focused, normalize_embeddings=True)
        dense = self.vectors @ vector
        words = set(search_terms(query + " " + original))
        lexical = np.maximum(self.bm25.get_scores(list(words)), 0)
        if lexical.max() > 0:
            lexical = lexical / lexical.max()
        title_match = np.array(
            [len(words & title) / max(len(words), 1) for title in self.title_terms]
        )
        title_precision = np.array(
            [len(words & title) / max(len(title), 1) for title in self.title_terms]
        )
        scores = 0.65 * dense + 0.25 * lexical + 0.1 * title_match
        # Retrieve broadly, then compare the actual question against each passage.
        # No topic can restrict retrieval to a handpicked set of pages.
        # Union, rather than one blended top-24, protects exact names and rare
        # details which the multilingual encoder may rank much lower.
        candidate_ids = set(map(int, np.argsort(dense)[-40:]))
        candidate_ids.update(int(i) for i in np.argsort(lexical)[-40:] if lexical[i] > 0)
        candidate_ids.update(int(i) for i in np.argsort(title_match)[-24:] if title_match[i] > 0)
        candidate_ids.update(
            int(i) for i in np.argsort(title_precision)[-24:] if title_precision[i] > 0
        )
        tuition_tables = set()
        if general_tuition(query):
            years = re.findall(r"\b20\d{2}\b", query)
            tuition_tables = {
                i
                for i, chunk in enumerate(self.chunks)
                if chunk.get("ocr_reviewed")
                and "Tuition fees by discount category" in chunk.get("context", chunk["text"])
                and all(year in chunk.get("context", chunk["text"]) for year in years)
            }
            candidate_ids.update(tuition_tables)
        candidates = sorted(
            (
                i
                for i in candidate_ids
                if (dense[i] >= 0.28 or lexical[i] > 0)
                and not (
                    prefer_text
                    and self.chunks[i].get("kind") in {"image", "pdf-ocr"}
                    and not self.chunks[i].get("ocr_reviewed")
                )
            ),
            key=lambda i: scores[i],
            reverse=True,
        )
        if not candidates:
            return []
        with self.lock:
            ranker = reranker()
            if ranker is not None:
                pairs = [
                    (
                        re.sub(
                            r"\b(?:Nile University(?: in Egypt)?|NU)\b",
                            "the university",
                            meaning or query,
                            flags=re.I,
                        ),
                        (
                            self.chunks[i]["title"]
                            if self.chunks[i].get("kind") != "image"
                            or self.chunks[i].get("ocr_reviewed")
                            else ""
                        )
                        + "\n"
                        + self.chunks[i].get("context", self.chunks[i]["text"]),
                    )
                    for i in candidates
                ]
                relevance = ranker.predict(
                    pairs, batch_size=RERANK_BATCH_SIZE, show_progress_bar=False
                )
                reranked = dict(zip(candidates, map(float, relevance)))
                # The ranker is a relevance signal, not a truth probability.
                # Retain exact title/topic matching as a small independent signal.
                candidates.sort(
                    key=lambda i: (
                        0.75 * reranked[i]
                        + 0.15 * title_match[i]
                        + 0.1 * scores[i]
                        # Reviewed general tables take priority over certificate-specific
                        # or old GPA tables for a question about undergraduate tuition.
                        + (0.35 if i in tuition_tables else 0)
                        # Course pages carry an explicit Course ID field. A matching course
                        # title is weaker evidence for a degree catalogue than a program list.
                        - (
                            0.3
                            if program_list
                            and re.search(
                                r"\bCourse ID\b",
                                self.chunks[i].get("context", self.chunks[i]["text"]),
                                re.I,
                            )
                            else 0
                        )
                    ),
                    reverse=True,
                )
        chosen, per_source, contexts = [], {}, set()
        for idx in candidates:
            if ranker is not None and reranked[idx] < 0.05:
                continue
            if ranker is None and dense[idx] < MIN_SIMILARITY:
                continue
            chunk = self.chunks[int(idx)]
            context_key = re.sub(r"\s+", " ", chunk.get("context", chunk["text"])).strip()
            if context_key in contexts:
                continue
            contexts.add(context_key)
            # Preserve useful adjacent evidence, while avoiding a single-page monopoly.
            if per_source.get(chunk["url"], 0) >= (5 if tuition_tables else 2):
                continue
            per_source[chunk["url"]] = per_source.get(chunk["url"], 0) + 1
            chosen.append(
                {
                    **chunk,
                    "text": chunk.get("context", chunk["text"]),
                    "similarity": round(float(dense[idx]), 4),
                    "score": round(float(scores[idx]), 4),
                    "rerank_score": round(reranked[idx], 4) if ranker is not None else None,
                    "citation": len(chosen) + 1,
                }
            )
            if len(chosen) == k:
                break
        return chosen

    def advise(self, query: str, original: str = "") -> list[dict]:
        """A vague 'why enroll?' needs distinct evidence topics, not a similarity to 'good'."""
        topics = [
            query,
            "Undergraduate Research Forum student projects and participation",
            "IECC Entrepreneurship Program Undergrad Track student startups",
            "undergraduate student exchange programs",
        ]
        chosen, seen = [], set()
        for topic in topics:
            for hit in self.search(
                topic,
                original=original if topic == query else "",
                meaning=topic,
                k=2 if topic == query else 1,
                prefer_text=True,
            ):
                if hit["id"] not in seen:
                    # A generic exchange-page statement is not evidence of a named
                    # program's accreditation. Don't turn it into an unsolicited sales claim.
                    if not re.search(r"accredit|certif|اعتماد|معتمد", query + " " + original, re.I):
                        hit = {
                            **hit,
                            "answer_text": "\n".join(
                                line
                                for line in hit["text"].splitlines()
                                if not re.search(r"accredit|certified internationally", line, re.I)
                            ),
                        }
                    chosen.append({**hit, "citation": len(chosen) + 1})
                    seen.add(hit["id"])
        return chosen
