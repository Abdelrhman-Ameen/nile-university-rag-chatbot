# Retests and browser checks — September 14, 2026

These are development retests of known failures, not a held-out benchmark. The complete 100-scenario baseline is in [CHAT_REVIEW.md](CHAT_REVIEW.md). Original runs are preserved; their old mechanical scores have not been recomputed with the newer language-output checks.

| Run | Scenarios | Manual findings |
| --- | ---: | --- |
| [qwen14-retest](runs/qwen14-retest.json) | 17 | 7 fail, 3 partial, 6 pass, 1 gap |
| [qwen35-9b-comparison](runs/qwen35-9b-comparison.json) | 8 | 3 partial, 3 fail, 2 pass |
| [coverage-retest](runs/coverage-retest.json) | 12 | 3 partial, 9 pass |

The runtime comparison confirms that system instructions reach the model; both the chat API and a direct chat-template probe can follow simple controls, but harder multilingual instructions are still unreliable. Qwen 3.5 9B is a comparison candidate, not an approved production upgrade. A larger local model is being evaluated separately.

## Browser checks

- Desktop table rendering: two data rows and three columns display cleanly in the NU theme.
- Fee citations: expanding Sources exposes the original image link and the extracted table text.
- Immediate follow-up: compose the next message while the first is running; submit as soon as Send re-enables. Answers 42 and then 50 arrive without a busy rejection.
- Failure while drafting: stop only the verified local chat-server process during a request. The failed prompt remains visible, the next draft is preserved exactly, and Send re-enables. The local server is restarted after this check.
- Earlier checks cover new-chat navigation, identity, acknowledgments without branding footers, and the 390-pixel mobile layout.

## Ingestion checks

- The resumed crawl has 2,147 extracted document records from 1,897 unique URLs. Eight hosts returned access challenges; 13,332 frontier URLs remain pending. Those URLs are not counted as collected.
- All 436 pages across 19 cached PDFs are eligible for OCR. The OCR run is still in progress, followed by the full image inventory.
- Nine fee/policy images have visually checked, content-hash-bound transcriptions. One is a historical ITCS GPA chart; it is not proof of current eligibility.
- Visual inspection of the FACT training catalogue caught interleaved facing pages. The corrected reading order keeps the PLC 131 and PLC 232 descriptions separate; page 19 was checked against its rendered image.
- DOCX paragraph/table order and XLSX saved values/number formats are covered by an extraction test. Legacy formats and embedded Office images remain unsupported.

Current deterministic verification: 58 pytest tests pass; Ruff and JavaScript syntax checks pass. This does not make the chatbot production-ready.
