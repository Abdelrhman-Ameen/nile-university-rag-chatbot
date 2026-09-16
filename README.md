# NU Chat

## Project snapshot

| Area | Checked-in result |
| --- | --- |
| Public source coverage | **1,904 unique URLs** across **17** NU and officially linked hosts |
| Knowledge base | **5,329 document records** indexed into **25,228 searchable chunks** |
| OCR coverage | **3,174 OCR-derived records**, including **36 reviewed sections from 10 hash-verified images** |
| Reviewed web evidence | **16 manually checked source records** for high-risk facts and policies |
| Supported input | English, Arabic, Egyptian Franco/Arabizi, and mixed Arabic-English |
| Local model stack | Multilingual Sentence-BERT + supervised intent head + MS MARCO reranker + `gemma4:12b` |
| Intent model | **256** training examples, **79** development-validation examples, **82.28%** fine-label accuracy |
| Full scenario review | **100 scenarios / 116 requests:** 82 pass, 14 partial, 4 fail; 97/100 mechanical checks |
| Independent challenge snapshot | **100 new queries:** 67 pass, 13 partial, 20 fail on the frozen pre-repair version |
| Current regression suite | **126 Python tests + 4 browser transport tests**, all passing |
| Focused latency benchmark | Median **3.74 s**, reduced from **6.90 s** (**45.8% faster**); live-status routes about **0.2 s** |
| Runtime | Fully local through Ollama and FastAPI; no cloud API key or hosted vector database |

The corpus includes public HTML pages, PDFs, DOCX files, XLSX tables, PDF OCR, and text extracted from content images. The current index contains 18,711 HTML chunks, 3,866 image-text chunks, 1,531 PDF-OCR chunks, 1,098 PDF text chunks, and 22 chunks from reviewed web evidence.

The evaluation figures are dated development snapshots. The complete 100-scenario review predates some later retrieval and grounding fixes, while the independent challenge was deliberately frozen before its failures were repaired. Results are kept for auditability and are not presented as a production certification.

## What it does

NU Chat is a local RAG chatbot for **Nile University in Egypt**. It collects public university material, extracts searchable text, finds evidence relevant to a question, reranks it, and asks a local language model to produce a concise answer with citations.

This is an independent NLP/LLM course project. It is not an official Nile University service and it cannot access private student records or live university systems.

## Features

- English and Arabic replies with automatic language detection
- Egyptian Franco/Arabizi input, answered in Egyptian Arabic by default
- Mixed Arabic-English questions with English technical terms preserved where useful
- Multilingual Sentence-BERT embeddings
- Hybrid vector, keyword, title, and cross-encoder retrieval
- Public HTML, PDF, DOCX, XLSX, and reviewed image-text collection
- Grounded NU answers with source citations and official links for changing information
- General chat without unrelated university retrieval
- FastAPI backend and a lightweight responsive web interface
- Local inference through Ollama; no cloud API key or hosted vector database
- Request queue, reconnect support, response caching, and timing diagnostics

The tested default generator is `gemma4:12b`. Another Ollama model, including Qwen, can be selected in `.env`, but it should be evaluated again before use.

## Languages and routing

| Input | Default reply behavior |
| --- | --- |
| English | English |
| Arabic | Natural Egyptian Arabic in Arabic script |
| Egyptian Franco / Arabizi | Egyptian Arabic in Arabic script |
| Mixed Arabic-English | Egyptian Arabic with useful English technical terms |

Language detection is separate from intent classification. The intent head routes identity, social chat, emotion, general information, creative tasks, NU facts, university-choice advice, mixed requests, and follow-ups. Clear general requests avoid retrieval. NU questions use retrieved evidence; ambiguous and contextual questions can use the local planner before retrieval.

## Quick start on Windows

Install Python 3.12 and [Ollama](https://ollama.com/download/windows), then run:

```powershell
./setup.ps1
./run.ps1
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

`setup.ps1` creates the environment, installs dependencies, trains the intent classifier, collects public data, runs OCR, and builds the search index. The first setup takes time because it downloads models and university content. Later runs reuse cached files and embeddings.

For an NVIDIA GPU, use:

```powershell
./setup.ps1 -Gpu
```

Then set `EMBEDDING_DEVICE=cuda` in `.env`.

## Manual setup

```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
ollama pull gemma4:12b
python -m nu_chat ingest
python -m nu_chat serve
```

Copy `.env.example` to `.env` to change the generator, embedding device, retrieval limits, or data directory.

## How it works

1. The collector follows approved public NU domains and stores source URLs and snapshots.
2. OCR extracts text from document images; manually reviewed transcriptions are tracked by file hash.
3. The index splits text into overlapping chunks and creates multilingual Sentence-BERT embeddings.
4. An intent classifier separates general chat, NU facts, advising, identity, and mixed requests.
5. Hybrid retrieval finds candidates and an MS MARCO cross-encoder reranks them.
6. The local generator answers from the retrieved evidence, then a separate grounding check audits factual NU claims.
7. FastAPI streams progress and serializes local GPU work through a bounded queue.

Clear English NU questions use their original wording directly, which avoids an unnecessary planning model call. Arabic factual questions keep the English query-planning step so the English reranker receives a reliable search query. Requests for live inventory or private records return a direct limitation and the relevant official route without asking the model to invent an answer.

## Refresh the data

```powershell
python -m nu_chat collect
python -m nu_chat ocr
python -m nu_chat index
```

To refetch previously cached pages and images:

```powershell
python -m nu_chat ingest --refresh
```

The crawler respects its configured scope and access restrictions. It does not bypass logins, private portals, robots rules, or access challenges.

## API

- `GET /api/health` — readiness, model, index, and queue status
- `GET /api/sources` — indexed source summary
- `POST /api/chat` — JSON chat endpoint
- `POST /api/chat/stream` — server-sent events with progress and final result
- `GET /docs` — interactive FastAPI schema

Both chat endpoints accept a question, optional conversation history, optional language override, and optional request UUID.

## Tests and evaluation

The most recent complete 100-scenario review used the local Gemma model and the expanded 1,904-URL corpus. A reviewer marked **82 scenarios as pass, 14 as partial, and 4 as fail**; the deterministic checker passed 97/100 scenarios. Those scenarios produced 116 real HTTP requests. See the [development results](evaluation/RESULTS.md) and [case-by-case review](evaluation/GEMMA_REVIEW.md).

A separate set of 100 previously unused questions produced **67 pass, 13 partial, and 20 fail** on a frozen earlier version. That harder run exposed transport-image, retrieval, language, citation, and error-handling gaps that motivated the later repairs. Its unchanged [report](evaluation/independent_2026_09_16/REPORT.md), [answers](evaluation/independent_2026_09_16/ANSWERS.md), and [failure analysis](evaluation/independent_2026_09_16/FINDINGS.md) remain in the repository.

The current focused performance artifact measures seven representative English, Arabic, general, factual, and live-status requests. Its median fell from **6.901 seconds to 3.740 seconds**, while the live bus and library routes completed in **0.233** and **0.218 seconds**. See the raw [before](evaluation/runs/performance-before-direct-routing.json) and [after](evaluation/runs/performance-final-direct-routing.json) responses, sources, and stage timings.

```powershell
python -m pytest -q
node --test tests/chat-transport.test.cjs
python -m ruff check nu_chat tests evaluation/check_chat.py evaluation/run_scenarios.py
```

Run the live scenario and connection checks while the app and Ollama are running:

```powershell
python evaluation/run_scenarios.py
python evaluation/benchmark_http.py --base-url http://127.0.0.1:8000 --output evaluation/runs/performance.json
python evaluation/check_connections.py --output evaluation/runs/connections.json
```

The repository keeps full evaluation answers and failure analysis under [`evaluation/`](evaluation/). Automated and AI-reviewed results are regression evidence, not a claim of production certification or an independent human benchmark.

## Main folders

| Path | Purpose |
| --- | --- |
| `nu_chat/` | Collection, OCR, retrieval, routing, generation, and FastAPI code |
| `static/` | Chat interface |
| `sources.json` | Crawl seeds and allowed domains |
| `sources/` | Reviewed public-source transcriptions and metadata |
| `evaluation/` | Scenarios, reports, and performance artifacts |
| `tests/` | Backend and browser-transport tests |

## Limits

The knowledge base is a dated public snapshot, not a live web search. Some pages can be blocked, changed, or absent from the crawl. OCR and language models can make mistakes, and the grounding audit reduces rather than eliminates hallucinations. Current fees, deadlines, availability, and personal records must be confirmed through the linked official university page or service.

The local server uses one inference slot by default. Public deployment would also need authentication, shared job storage, per-user rate limits, monitoring, and a separate load test.

## References

- [Nile University, Egypt](https://nu.edu.eg/)
- [Sentence-BERT](https://aclanthology.org/D19-1410/)
- [Multilingual MiniLM encoder](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
- [MS MARCO cross-encoder](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L6-v2)
- [Ollama API](https://docs.ollama.com/api/chat)
