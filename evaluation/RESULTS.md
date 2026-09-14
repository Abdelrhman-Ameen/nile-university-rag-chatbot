# Development evaluation — September 14, 2026

The most recent **complete 100-scenario review** used local `gemma4:12b`, GPU retrieval, and the expanded 1,904-URL corpus. It produced **82 pass, 14 partial, 4 fail** on manual review; the mechanical checker reported **97/100**. There were 116 HTTP requests. Successful non-identity responses had median 6.57 seconds, sampled p95 16.51 seconds and maximum 28.3 seconds. These are single-laptop development measurements, not deployment load-test results.

Read [every case and its verdict](GEMMA_REVIEW.md) and [the full answer log](runs/gemma-second-full.json). That snapshot precedes the multipart retrieval, tuition evidence focusing and explicit official-link fixes. Later focused reruns are reported in [RETESTS.md](RETESTS.md); their scores do not replace the full-run score.

Two complete Gemma runs were manually reviewed: the first yielded 71 pass / 14 partial / 15 fail, then the second 82 / 14 / 4. Known failures were used to tune subsequent changes, so neither run is a blind benchmark. Earlier Qwen runs remain in `runs/` rather than being overwritten. The university has not certified these reviews.

The intent classifier is a supervised logistic-regression head using frozen multilingual Sentence-BERT embeddings plus character features. It has 256 training and 79 development-validation examples; fine-label accuracy is 82.28%. Confidence selects whether to use the local model for contextual planning; classifier scores are not calibrated truth probabilities. See [validation details](intent_validation.json).

Current coverage: 25,205 chunks from 5,312 document records and 1,904 distinct source URLs. OCR processed 4,600 assets with 4,531 successes and 69 errors; only 33 sections from nine images have manually reviewed, content-hash-bound transcriptions. The crawl still has 13,332 pending URLs and eight hosts paused after access challenges. See [coverage report](coverage-2026-09-14.json). **This is not complete university coverage or production readiness.**

## Historical initial baseline


**Historical baseline below.** These initial URL-level scores did not catch the broken Arabic rewrites or repeated admissions replies to complaints. They are not evidence that the current chatbot works. The new `check_chat.py` suite tests real chat requests, including general conversation; rejecting every non-university question is no longer the desired behavior. See `CHAT_REVIEW.md` for the revised model's results.

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
