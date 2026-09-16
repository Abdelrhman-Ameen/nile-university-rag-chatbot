# NU Chat

NU Chat is a local RAG chatbot for **Nile University in Egypt**. It searches a collected snapshot of public NU websites and documents, retrieves relevant passages, and uses a local language model to answer with citations.

This is an independent NLP/LLM course project. It is not an official Nile University service and it cannot access private student records or live university systems.

## Features

- English and Arabic chat with automatic language detection
- Multilingual Sentence-BERT embeddings
- Hybrid vector, keyword, title, and cross-encoder retrieval
- Public HTML, PDF, DOCX, XLSX, and reviewed image-text collection
- Grounded NU answers with source citations and official links for changing information
- General chat without unrelated university retrieval
- FastAPI backend and a lightweight responsive web interface
- Local inference through Ollama; no cloud API key or hosted vector database
- Request queue, reconnect support, response caching, and timing diagnostics

The tested default generator is `gemma4:12b`. Another Ollama model, including Qwen, can be selected in `.env`, but it should be evaluated again before use.

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

The repository keeps full evaluation answers and failure analysis under [`evaluation/`](evaluation/). Automated and AI-reviewed results are regression evidence, not a claim of production certification.

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
