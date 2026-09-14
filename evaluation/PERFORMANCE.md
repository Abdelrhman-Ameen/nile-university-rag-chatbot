# Local performance and connection checks — 2026-09-14

This change keeps FastAPI and the same local Gemma 4 12B, CUDA SBERT, reranker,
25,205-chunk index, and evidence audit. It changes request scheduling, reconnects,
caches, and memory use. These are laptop measurements, not a production capacity claim.

## Findings and changes

- At the beginning of the investigation neither the app nor Ollama was running.
  `run.ps1` starts the local services; FastAPI now serves the UI during model warmup
  and distinguishes startup failure from an offline connection.
- Waiting requests and duplicate reconnects used to occupy synchronous web worker
  threads. Admission and shared task waiting are now asynchronous. Only the active
  inference job occupies a worker. The queue is still bounded to eight waiting jobs.
- A browser disconnect does not cancel the shared task. Reconnection uses the same
  UUID and full payload. The queue releases before the result is delivered.
- The UI receives progress and ten-second heartbeats over SSE, followed by the
  checked answer. Token fragments from an unaudited draft are not displayed.
- Health requests no longer scan 25,205 chunks or make an Ollama request. A background
  check supplies a snapshot every 30 seconds; source-library summaries are cached by
  index version. Actual inference no longer depends on a redundant preflight probe.
- HTTPX pool limits are applied to the actual transport, with independent two-second
  connection/pool timeouts. The pooled client closes after jobs drain at shutdown.
- Exact plans include language and history in their 128-entry cache key. Search
  caches include every retrieval option, and a new index creates a fresh cache.
  Responses receive deep copies so citations and evidence focusing cannot corrupt it.
- The Ollama 0.34 llama.cpp runner had a default **8,192 MiB retired-prompt RAM cache**.
  We observed its working set reach **8,379,949,056 bytes (7.80 GiB)** while the host
  had only about 1.38 GiB of free physical memory. `run.ps1` now sets
  `LLAMA_ARG_CACHE_RAM=0` and `LLAMA_ARG_CTX_CHECKPOINTS=2` when starting Ollama.
  After the comparison run the runner's working set was **1,480,531,968 bytes
  (1.38 GiB)**. These are working-set snapshots, not strict total-process memory bounds.
  The generator stays resident in VRAM; its model weights and precision are unchanged.

The backend's supported environment variables were checked against the installed
`llama-server.exe --help` and [llama.cpp's server documentation](https://github.com/ggml-org/llama.cpp/tree/master/tools/server).
Residency and single-model/slot settings follow [Ollama's documented controls](https://docs.ollama.com/faq).
The asynchronous request boundary keeps blocking inference in a worker, consistent
with [FastAPI's concurrency guidance](https://fastapi.tiangolo.com/async/).

## Before/after probe

`benchmark_http.py` issued the same questions with fresh IDs, one exact repeated
question, and an overlapping duplicate plus another question. It sampled health
every half second. Full responses and timings are preserved in
[before](runs/performance-before.json) and [after memory limits](runs/performance-bounded.json).

| Measurement | Before | After |
| --- | ---: | ---: |
| Health median | 8.80 ms | 2.18 ms |
| Health sampled p95 | 13.08 ms | 4.36 ms |
| Health errors | 0 / 137 | 0 / 138 |
| First Arabic tuition question | 7.98 s | 7.86 s |
| Franco application + all school fees | 16.34 s | 15.28 s |
| Campus location | 7.48 s | 7.09 s |
| NU choice advice | 13.23 s | 14.08 s |
| Exact repeated tuition question | 7.10 s | 4.89 s |
| UGRF response, including repair | 16.73 s | 19.28 s |
| Other question arriving with UGRF | 17.54 s | 20.04 s |

All nine HTTP chat requests completed in each probe. Duplicate IDs returned the same
result. The repeated tuition request skipped planning inference and retrieval work,
while generation and the evidence audit still ran. New questions are **not uniformly
faster**: variable answer length, repairs, thermal state and other laptop activity
still affect the 12B model. Queueing cannot remove single-GPU inference time.

The [intermediate probe](runs/performance-after.json) preceded the memory fix.
The [failed startup probe](runs/performance-startup-error.json) caught an invalid
string `"-1"` keep-alive value; it was corrected to numeric `-1` and covered by a test.
These failed/intermediate records are retained rather than replaced with successful runs.

## Connection verification

[Real socket test](runs/connections-optimized.json): closed the first SSE response
after receiving its first status, reconnected with the same UUID, obtained the answer,
replayed it through the JSON endpoint, then immediately submitted another question.

- First progress event: **23.8 ms**.
- Completed and checked tuition answer: **6.64 seconds**.
- Replay: **2.3 ms**, exactly the same result.
- Queue inactive immediately after result delivery.
- Immediate next question: **HTTP 200**, **0.54 seconds**.

107 Python tests and four JavaScript tests passed locally. Tests include 50 concurrent
reconnects with one inference, health responsiveness during that wait, cancellation
without releasing another job's slot, bounded overload, error replay, changed-payload
conflicts, fragmented Arabic UTF-8 events, interrupted-stream reconnection, and avoiding
automatic retries of model/HTTP errors.

The complete [100-scenario run](runs/optimized-100.json) issued **116 requests**:
**112 HTTP 200** and **four expected HTTP 422 validation responses**, with no connection
failures or HTTP 5xx responses. All 100 mechanical checks passed. The 104 successful
non-identity requests had median **6.17 s**, sampled p95 **9.84 s**, and maximum
**18.16 s**. After this extended run the runner working set was **1,466,159,104 bytes
(1.37 GiB)**. The old retired-prompt memory growth did not reappear in this run.

[Manual output review](OPTIMIZED_REVIEW.md) records factual, scope and wording defects
that the mechanical checker missed. The 100/100 result is not an answer-quality score.
That run used API code version `fe296684833c0197`; the final subsequent change makes
Sources wait for warmup and serializes concurrent cold index loads. It changes no
retrieval scoring or model prompts and is covered by startup/concurrency unit tests
and a final live startup/reconnect check.

The [final live reconnect check](runs/connections-final.json), on code version
`2b2c1e1ccbdf35c8`, again passed: first progress in **19.5 ms**, completion in
**6.63 s**, replay in **3.6 ms**, immediate next answer in **0.54 s**. The restarted
server reported ready and the source library returned all **1,904** indexed URLs.

Browser verification used the real UI: Franco application/tuition, immediate Arabic
ITCS tuition follow-up, then a 50% discount follow-up. All three completed, sources and
dated links rendered, Send re-enabled, and no browser console errors were recorded.
The last answer gave the correct 96,840 EGP ITCS amount but also volunteered other
schools' amounts; that existing response-scope limitation remains.

Prior intermittent Windows socket error 10013 is not proven fixed at the OS level.
No firewall or host security settings were changed. This probe observed no socket
errors and verified recovery from an intentionally interrupted connection.

## Reproduce

Start `run.ps1` and wait until `/api/health` reports `ready: true`. Use one load probe
at a time so competing tests do not distort GPU measurements:

```powershell
python evaluation/benchmark_http.py --output data/performance.json
python evaluation/check_connections.py --output data/connections.json
python evaluation/run_scenarios.py --output data/scenarios-100.json
python -m pytest -q
node --test tests/chat-transport.test.cjs
```

To change the retired-prompt cache or context-checkpoint limit, set the corresponding
`LLAMA_ARG_*` process environment variable before launching `run.ps1`; it preserves
explicit values. An already-running Ollama process must be restarted for those
settings to take effect. Other Ollama backends may not use these llama.cpp controls.
