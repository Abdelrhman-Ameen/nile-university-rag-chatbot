"""Token-aware chunks, normalized SBERT vectors, and a small hybrid retriever.

NumPy is sufficient for a university corpus: cosine search is a matrix multiply.
An atomic NPZ file contains both chunks and vectors, with no pickle loading.
"""

import json
import re
import threading
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

import numpy as np
from rank_bm25 import BM25Okapi

from nu_chat.config import DATA_DIR, EMBEDDING_DEVICE, EMBEDDING_MODEL, MIN_SIMILARITY, TOP_K
from nu_chat.language import tokens

STOP_WORDS = set(
    "a an the of to in at for is are do does how what can i me my we you your with and or nile university nu".split()
)


# Authority hints point to dedicated university service pages, not canned answers.
TOPIC_PAGES = {
    r"\b(apply|application|admission)\b": ("/how-to-apply", "/admission-requirement-and-documents"),
    r"\b(fees?|tuition|cost)\b": ("/fees-and-financials",),
    r"\b(where|location|located|address)\b": ("/contact-us-Departments",),
    r"\b(programs?|majors?|speciali[sz]ations?|departments?)\b": (
        "/faqs",
        "/undergraduate-programs",
    ),
    r"\bscholarships?\b": ("/scholarship/undergraduate-scholarship",),
}


def search_terms(text: str) -> list[str]:
    return [word for word in tokens(text) if word not in STOP_WORDS]


@lru_cache(maxsize=1)
def encoder():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL, device=EMBEDDING_DEVICE)


def chunk_document(
    document: dict, tokenizer, max_tokens: int = 92, overlap: int = 18
) -> list[dict]:
    if not 0 <= overlap < max_tokens:
        raise ValueError("Overlap must be smaller than chunk size")
    text = document["text"]
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
    model = encoder()
    chunks = [chunk for doc in documents for chunk in chunk_document(doc, model.tokenizer)]
    if not chunks:
        raise RuntimeError("The corpus has no usable text")
    # Reserve token space for the source title, so text is not silently truncated.
    texts = [
        model.tokenizer.decode(model.tokenizer.encode(c["title"], add_special_tokens=False)[:28])
        + "\n"
        + c["text"]
        for c in chunks
    ]
    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=True, batch_size=32)
    metadata = {"model": EMBEDDING_MODEL, "chunks": chunks}
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp = DATA_DIR / "index.tmp"
    with temp.open("wb") as stream:
        np.savez_compressed(
            stream,
            vectors=vectors.astype("float32"),
            metadata=json.dumps(metadata, ensure_ascii=False),
        )
    temp.replace(DATA_DIR / "index.npz")
    return {
        "chunks": len(chunks),
        "documents": len(documents),
        "dimensions": vectors.shape[1],
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

    def search(self, query: str, original: str = "", k: int = TOP_K) -> list[dict]:
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
        preferred_paths = {
            path
            for pattern, paths in TOPIC_PAGES.items()
            if re.search(pattern, query, re.IGNORECASE)
            for path in paths
        }
        authority = np.array(
            [float(urlsplit(c["url"]).path in preferred_paths) for c in self.chunks]
        )
        # Prefer dedicated service pages when they contain a match. This prevents
        # incidental mentions (such as exchange fees) from confusing the generator.
        direct = (authority > 0) & (dense >= 0.28)
        use_direct = bool(direct.any()) and not re.search(
            r"\b(master|phd|postgraduate|graduate|exchange)\b", query, re.IGNORECASE
        )
        scores = 0.65 * dense + 0.2 * lexical + 0.1 * title_match + 0.15 * authority
        chosen, per_source, contexts = [], {}, set()
        for idx in np.argsort(scores)[::-1]:
            if use_direct and not direct[idx]:
                continue
            if dense[idx] < MIN_SIMILARITY and not (dense[idx] >= 0.28 and authority[idx] > 0):
                continue
            chunk = self.chunks[int(idx)]
            context_key = (chunk["url"], chunk.get("context", chunk["text"]))
            if context_key in contexts:
                continue
            contexts.add(context_key)
            # Preserve useful adjacent evidence, while avoiding a single-page monopoly.
            if per_source.get(chunk["url"], 0) >= 2:
                continue
            per_source[chunk["url"]] = per_source.get(chunk["url"], 0) + 1
            chosen.append(
                {
                    **chunk,
                    "text": chunk.get("context", chunk["text"]),
                    "similarity": round(float(dense[idx]), 4),
                    "score": round(float(scores[idx]), 4),
                    "citation": len(chosen) + 1,
                }
            )
            if len(chosen) == k:
                break
        return chosen
