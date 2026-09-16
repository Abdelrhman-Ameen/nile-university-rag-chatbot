# Independent human-style query evaluation — 100 new queries

**67 pass · 13 partial · 20 fail.** These are AI-reviewed answers, not a human-reviewed benchmark or a production certification.

All 100 frozen target queries were submitted once through the actual local FastAPI chat endpoint. No chatbot code, prompt, model, corpus or index was changed during the run, and failed cases were not retried. Six requests used prewritten history fixtures; the other 94 began with empty history. The set was checked against 490 distinct prior prompts, with no normalized exact matches, and reviewed for distinct fact targets. Topic families overlap; these are new decisions and facets rather than paraphrases of the old 100 scenarios.

The frozen app was commit `2729a6e`, code version `2b2c1e1ccbdf35c8`, using local `gemma4:12b` with CUDA retrieval, 25,205 chunks and 1,904 source URLs. The run used port 8001 because an unrelated app occupied 8000. The reference snapshot was fetched independently from official NU Egypt sites and was not fed into the chatbot.

## Answer quality

| category | pass | partial | fail | total |
| --- | --- | --- | --- | --- |
| admissions | 16 | 2 | 7 | 25 |
| services | 11 | 0 | 0 | 11 |
| transport_ocr | 1 | 0 | 7 | 8 |
| clubs | 10 | 0 | 2 | 12 |
| programs | 7 | 3 | 0 | 10 |
| courses | 6 | 0 | 0 | 6 |
| research | 3 | 1 | 0 | 4 |
| enterprise | 2 | 2 | 1 | 5 |
| uncertainty | 3 | 4 | 0 | 7 |
| context | 3 | 0 | 3 | 6 |
| general | 5 | 1 | 0 | 6 |

| input_language | pass | partial | fail | total |
| --- | --- | --- | --- | --- |
| en | 24 | 7 | 3 | 34 |
| ar | 24 | 1 | 8 | 33 |
| franco | 19 | 5 | 9 | 33 |

Each response was read against the predeclared expectation, fresh reference snapshot and returned passages. Pass requires a correct, complete, grounded answer in the appropriate language with required links. Partial indicates a limited but nonfatal issue; fail includes material factual/grounding errors, unanswered answerable questions and HTTP failures. This is stricter than the previous keyword regression checks; the two pass rates are not directly comparable.

## Reliability and latency

HTTP outcomes: `{'200': 96, '503': 4}`. Sequential end-to-end latency across all 100 requests: median **9.07s**, p95 **20.05s**, maximum **27.55s**. These measurements include planning, retrieval, generation and answer verification on a warmed local service. They do not measure browser rendering, SSE reconnects, concurrency or time to first token. HTTP 200 does not establish answer correctness.

Run: 2026-09-16T06:19:05.107964+00:00 through 2026-09-16T06:35:42.543709+00:00. Frozen-asset hashes matched at completion.

## Reproducibility and limitations

- [Failure examples and repair priorities](FINDINGS.md), including the scope of the post-response scientific-claim check.
- [Protocol](PROTOCOL.md), [100 frozen cases](suite.json), [novelty audit](novelty.json), [prior prompt inventory](prior_questions.json).
- [Every answer with its review](ANSWERS.md), [structured review](review.json), [raw HTTP responses and evidence](responses.jsonl).
- [Reference snapshots](references.json), [visually checked transport image facts](image_reference.json), [freeze manifest](freeze.json), [completion hashes](completion.json).

The author/reviewer is the same AI agent with implementation context, not an independent human panel. References and criteria were frozen before responses, but query selection was informed partly by available university pages; this is not a blinded population study. Source-page ambiguity, missing live inventories and unknown real-world service status remain limitations. Repeated broad subjects within the set test different facets; six contextual cases intentionally revisit a fact to test continuity. No claims about all university endpoints or production readiness follow from these 100 results.
