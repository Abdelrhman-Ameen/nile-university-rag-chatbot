# NU Chat

A local RAG chatbot for **Nile University in Egypt**, built as an independent NLP/LLM course project. Ask university questions, have a conversation, or ask general questions in English, Arabic, Egyptian Franco, or mixed language. It is not an official university service.

The interface is plain HTML/CSS/JavaScript with NU colors, Arabic layout, chat history, code blocks, tables, and expandable citations. Model diagnostics stay in the API rather than the conversation UI.

## Run on Windows

Requires Python 3.12 and [Ollama](https://ollama.com/download/windows). The default generator, [Gemma 4 12B](https://ollama.com/library/gemma4:12b), downloads about 7.6 GB. This workspace uses a 16 GB NVIDIA GPU for Ollama. Embedding and reranking support either CPU or CUDA; OCR runs on CPU; CPU-only generation is possible but substantially slower.

```powershell
.\setup.ps1
.\run.ps1
```

Open [the chatbot](http://127.0.0.1:8000/). Setup installs pinned dependencies, trains the intent classifier, crawls public sources, extracts image text, and builds the index. The first collection can take a long time. Successful downloads, OCR, and unchanged embeddings are cached. The launch script starts Ollama if necessary, downloads the configured generator, and starts FastAPI. The UI is available while models warm in the background. An existing portable runtime under `.runtime/ollama/` is also supported.

For GPU retrieval on a compatible NVIDIA driver, use `./setup.ps1 -Gpu` and set
`EMBEDDING_DEVICE=cuda` in `.env` before running the app. This installs the CUDA 13.0
build of the same pinned PyTorch version from its official package index. The workspace
verified it on the RTX 3080 Laptop GPU; the CPU-only installation remains the portable default.

For manual setup:

```bash
python -m venv .venv
# Activate .venv using your shell's activation command.
python -m pip install -r requirements.txt
ollama pull gemma4:12b
# Keep Ollama running (ollama serve if the service is not running).
python -m nu_chat ingest
python -m nu_chat serve
```

Copy `.env.example` to `.env` to override models or paths. The requirements were resolved on Windows/Python 3.12; other platforms can resolve `requirements.in` if a pinned wheel is unavailable. A smaller model can be configured, but its response quality must be evaluated separately.

## Pipeline

1. **Collect public sources.** `sources.json` defines seeds and allowed domains: NU Egypt and its subdomains, plus the publicly linked NilePreneurs affiliate `np.eg`. The crawler discovers sitemaps, links, embedded documents, and content images. It extracts HTML, PDF, DOCX paragraphs/tables, and XLSX saved cell values with number formats; it does not recalculate formulas. It preserves raw snapshots, source URLs, dates, PDF pages, failures, and the pending frontier in SQLite/JSON. Parser fixes can be applied to cached HTML without downloading it again. Contact details in page footers are retained. A blocked host is paused; private portals and access challenges are not bypassed.
2. **Extract text from images.** RapidOCR processes content images in English and Arabic with four independent OCR workers; PDFium renders every cached PDF page for OCR, including pages with both selectable text and images. Facing pages with a clear text gutter are read separately. Only extracted text is embedded. The nine manually checked fee/policy images in `sources/reviewed_images.json` have content hashes and structured table rows. Their transcriptions apply only when downloaded image bytes match those hashes. Other OCR remains explicitly unreviewed. A historical GPA chart is explicitly marked as historical; its presence does not establish current eligibility. Reviewed public webpage snapshots live in `sources/reviewed_documents.json` with provenance.
3. **Embed and search.** Multilingual Sentence-BERT produces 384-dimensional vectors. Token-aware chunks contain 92 tokens with 18-token overlap and adjacent context. NumPy cosine search, BM25, and title matching form a candidate union. An English MS MARCO cross-encoder reranks using the normalized English question; unreviewed image titles cannot stand in for their actual OCR text, and degree-list requests downrank pages with an explicit Course ID field; repeated passages and low-relevance candidates are removed. This English reranker is a limitation for Arabic-only source text. Unchanged chunks reuse their vectors during index refresh.
4. **Classify before retrieval.** A small supervised logistic-regression head uses frozen Sentence-BERT embeddings plus hashed character features. It separates identity, social chat, emotion, general opinion, university choice/advising, factual university questions, general information, creative work, mixed requests and follow-ups. Confident ordinary chat decisions skip retrieval planning. Document requests already require an English search rewrite, so that same local-model call resolves their exact intent using conversation history and official acronym meanings; it prevents an application procedure from turning into a persuasion response. Ambiguous messages also use that planner. This trains an intent head, not the encoder or generator. English/Arabic/Franco/mixed detection is separate; Franco input gets Egyptian Arabic by default. `evaluation/intent_examples.json` contains 256 training and 79 development-validation examples. The validation set was used for tuning and is not a blind benchmark. Rebuild the head with `python -m nu_chat train-intent`.
5. **Answer.** General chat uses the local model without unrelated university passages. Identity is application-owned. A short NU-specialization note is added only to substantive general information. University answers use retrieved evidence and quiet citations. The advising route searches several concrete topics, including student research and entrepreneurship, to discuss why NU may fit a student and address objections without inventing advantages. It prioritizes text and reviewed image transcriptions for those broad recommendations; detailed factual retrieval still includes all OCR. Answers are generated directly in the requested language. Citation-ID checks are followed by a separate local-model evidence audit and at most one repair. The audit can still miss errors or reject a correct answer; it is not proof of truth.
6. **Handle requests.** FastAPI accepts chat requests asynchronously. One local GPU serves one pipeline at a time; up to eight others wait in a FIFO queue without occupying worker threads. Identity questions do not need the GPU. The browser receives live progress and a heartbeat at least every ten seconds through `/api/chat/stream`; only the final checked answer is displayed. Network reconnects retry the same request UUID at most twice. An in-memory cache joins the original task even after a client disconnects, or replays its result for five minutes (128 entries maximum). Reusing an ID with a changed payload returns 409. The queue releases before the final response, allowing an immediate follow-up. `/api/chat` remains available for JSON clients.
7. **Bound repeated work and memory.** Exact query plans (including language and conversation history) and retrievals use independent 128-entry caches; rebuilding the index discards its retrieval cache. Returned passages are copied before per-answer citation edits. Health replies use a background snapshot, refreshed every 30 seconds, instead of probing Ollama on each request. Model calls use a pooled client with separate connect/read/pool timeouts and expose token counts and inference timings. `MODEL_KEEP_ALIVE=-1` keeps the model resident; set `30m` to allow idle unloading. The launch script starts one Ollama model/slot, disables the llama.cpp backend's 8 GiB retired-prompt RAM cache, and limits context checkpoints to two. Those backend limits apply when this script starts Ollama; restart an existing server to change its process environment. No model quantization or grounding check was removed. See [measured performance and connection tests](evaluation/PERFORMANCE.md).

## Collect, refresh, and test

```bash
python -m nu_chat train-intent
python -m nu_chat collect
python -m nu_chat ocr
python -m nu_chat index
# Refetch cached pages and images explicitly:
python -m nu_chat ingest --refresh
# Optional bounded exploration; zero is the default unbounded frontier:
python -m nu_chat collect --max-pages 200
python -m nu_chat ocr --document-images-only
python -m pytest -q
node --test tests/chat-transport.test.cjs
python -m ruff check nu_chat tests evaluation/check_chat.py evaluation/run_scenarios.py
# With the app and Ollama running:
python evaluation/run_scenarios.py
python evaluation/run_scenarios.py --resume
python evaluation/run_scenarios.py --ids S097,S098,S099,S100 --output data/concurrency-check.json
python evaluation/benchmark_http.py --output data/performance.json
python evaluation/check_connections.py --output data/connections.json
```

`ingest` trains the intent head, then runs collection, OCR, and indexing in order. `--max-pages` limits new network requests; cached results do not consume that allowance. `--max-images` optionally limits selected images. Public URLs on a newly approved domain must be added to `sources.json` deliberately.

The 100-scenario suite includes 116 messages across identity, greetings, emotions, coding, NLP, fees, GPA, admissions, research, competitions, source grounding, follow-ups, invalid input, and concurrent requests. It uses the actual `/api/chat` endpoint and preserves full responses, cited passages, and timings in `data/scenarios-100.json`. Each scenario includes a manual-review rubric. Mechanical passes are regression signals, not factual-quality scores or production certification. See [evaluation notes](evaluation/RESULTS.md).

A separate [100-query challenge evaluation on September 16, 2026](evaluation/independent_2026_09_16/REPORT.md) produced **67 pass, 13 partial and 20 fail**, including four HTTP 503 responses. It used new fact targets checked against 490 earlier prompts, frozen references and an unchanged local app. Every answer was reviewed by an AI agent; this was not a recruited human panel. The [full answers](evaluation/independent_2026_09_16/ANSWERS.md) and [failure analysis](evaluation/independent_2026_09_16/FINDINGS.md) document missing image-based transport information, lost Franco negation, retrieval gaps and citation errors. The interface refinement was made after that run; it does not fix those answer-quality failures.

Coverage artifacts:

- `evaluation/coverage-2026-09-14.json`: checked-in summary of completed extraction and remaining gaps.
- `data/collection_report.json`: downloaded documents, errors, blocked hosts, and pending URLs.
- `data/source_inventory.json`: per-URL outcomes.
- `data/crawl/assets.json`: discovered image URLs and page context.
- `data/crawl/external_links.json`: external links requiring scope review.
- `data/ocr_report.json`: OCR success/failure and manual-review status.
- `data/documents.jsonl` and `data/ocr_documents.jsonl`: text corpora used by the index.

## Code map

| File | Responsibility |
| --- | --- |
| `nu_chat/collect.py`, `crawl.py` | Scope, robots rules, extraction, durable crawl frontier |
| `nu_chat/ocr.py` | Image and PDF text extraction |
| `nu_chat/language.py`, `persona.py` | Language hints and NU identity |
| `nu_chat/intent.py` | Frozen-encoder features, supervised head, confidence fallback |
| `nu_chat/retrieval.py` | Chunking, embeddings, indexing, hybrid search |
| `nu_chat/generation.py` | Local model planning and grounded answers |
| `nu_chat/evidence.py`, `citations.py` | Applicable fee evidence, official update links and code-safe citations |
| `nu_chat/request_queue.py`, `request_cache.py`, `api.py` | Bounded queue, reconnect deduplication, validation, API |
| `static/` | Chat interface with no frontend build step |
| `evaluation/`, `tests/` | Live scenarios, review rubrics, deterministic checks |

API: `GET /api/health`, `GET /api/sources`, `POST /api/chat`, `POST /api/chat/stream`; interactive schema at `/docs`. Both chat endpoints accept the same JSON and optional `request_id` UUID. Stream events are `status` (`stage`), `result` (the normal response), or `error` (`status`, `detail`); validation and conflicting IDs fail before streaming starts. A disconnected stream can reconnect using the identical body. Health distinguishes startup from readiness and reports active/waiting jobs; its model status reflects the last background residency check. Conversation history stays in browser memory and resets on reload. There is no cloud API dependency or hosted vector database.

## Known limits

Multi-part questions receive separate retrieval queries. For tuition, reviewed general tables supply the applicable base rate; scholarship and certificate conditions are kept separate. Answers involving changing NU information include explicit official links. These links supplement the answer and do not mean a page was checked live on every message.

The corpus is a snapshot, not live web search. A drained frontier would still not prove every university document was discoverable; currently some sites return access challenges and some old domains fail. Check the reports before claiming coverage. JavaScript-only content, external document hosts, legacy Office formats and images embedded in Office documents can remain missing.

Automatic replies to Franco input use Egyptian Arabic. Explicit Franco output and some Arabic wording remain unreliable. Conflicting historical policies, unreviewed OCR, and model hallucinations require manual evidence review. A historical GPA-to-discount chart must not be presented as confirmed current eligibility. Neither this model nor the small evaluation set establishes production readiness.

The server binds to loopback and uses one Uvicorn process, which owns the GPU queue and reconnect cache. Multiple web workers would require shared task storage and a separate inference worker. Public deployment needs authentication, per-user limits, monitoring, a deployment load test, and a model-hosting plan. Disconnecting a client preserves its generation for reconnection; inference timeouts bound it. Restarting the server loses in-memory jobs and cached responses. Runtime files, downloaded sources, and model weights are excluded from Git. See [logo attribution](docs/ASSETS.md).

## References

- [Nile University, Egypt](https://nu.edu.eg/)
- [Sentence-BERT paper](https://aclanthology.org/D19-1410/)
- [Multilingual MiniLM encoder](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- [MS MARCO cross-encoder](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2)
- [Ollama chat API](https://docs.ollama.com/api/chat)
- [RapidOCR](https://github.com/RapidAI/RapidOCR)
