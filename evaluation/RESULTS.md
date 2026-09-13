# Development evaluation — September 14, 2026

Corpus: **148 public NU Egypt URLs**, including **2 PDFs**, producing **1,058 chunks**. The crawl attempted 160 URLs; 158 extracted page/text records were retained. PDF pages count separately from source URLs. Many additional sitemap URLs remain outside the bounded collection.

Models: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` and `qwen3:4b-instruct` through local Ollama.

| Metric | Encoder + glossary | Encoder + Qwen normalization |
| --- | ---: | ---: |
| Language routing | 15/15 | 15/15 |
| Relevant URL in top 5 | 11/13 | 13/13 |
| MRR@5 | 0.846 | 1.000 |
| Unrelated questions rejected | 2/2 | 2/2 |

These are **development results**, not a held-out benchmark. Routing rules and prompts were adjusted using this set. The small sample and URL-level labels cannot establish general accuracy, citation entailment, Franco fluency, or performance on new questions. Full per-question data is in `results-baseline.json` and `results-qwen.json`.

Manual end-to-end checks confirmed a generated answer for the campus location in Sheikh Zayed, Giza, Egypt; application steps; Arabic ITCS program questions; and a Franco application question. Replies can mix English into Franco, and translated academic program names should be checked against the English source labels. A tuition-cost question abstained because numerical fee tables are images, which the text-only collector does not OCR. A FIFA question correctly abstained.

33 deterministic tests pass, including URL scope, robots policies, redirects, language routing, chunk overlap, retrieval rejection, citation validation, structured abstention, truncated output rejection, and API validation. Browser checks covered the desktop and 390-pixel mobile layouts, mobile navigation, source-library filtering, and a generated answer with a working citation URL.

Reproduce with `python -m nu_chat evaluate --with-llm`; results can change when sources or model revisions change. Add a separate, manually labeled held-out dataset for the course's final accuracy claims.
