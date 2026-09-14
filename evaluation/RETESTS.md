# Retests and browser checks — September 14, 2026

These are development retests of known failures, not a held-out benchmark. The complete 100-scenario baseline is in [CHAT_REVIEW.md](CHAT_REVIEW.md). Original runs are preserved; their old mechanical scores have not been recomputed with the newer language-output checks.

| Run | Scenarios | Manual findings |
| --- | ---: | --- |
| [qwen14-retest](runs/qwen14-retest.json) | 17 | 7 fail, 3 partial, 6 pass, 1 gap |
| [qwen35-9b-comparison](runs/qwen35-9b-comparison.json) | 8 | 3 partial, 3 fail, 2 pass |
| [coverage-retest](runs/coverage-retest.json) | 12 | 3 partial, 9 pass |

Qwen comparisons confirmed that system instructions reach the model, but multilingual and factual errors remained. The runtime now uses local Gemma 4 12B after comparison; this changes the generator, not the Sentence-BERT encoder. Two complete Gemma runs were manually reviewed; see [GEMMA_REVIEW.md](GEMMA_REVIEW.md). Explicit Franco output remains unreliable; automatic Franco input receives Egyptian Arabic.

## Browser checks

- Desktop table rendering: two data rows and three columns display cleanly in the NU theme.
- Fee citations: expanding Sources exposes the original image link and the extracted table text.
- Immediate follow-up: compose the next message while the first is running; submit as soon as Send re-enables. Answers 42 and then 50 arrive without a busy rejection.
- Failure while drafting: stop only the verified local chat-server process during a request. The failed prompt remains visible, the next draft is preserved exactly, and Send re-enables. The local server is restarted after this check.
- Earlier checks cover new-chat navigation, identity, acknowledgments without branding footers, and the 390-pixel mobile layout.

## Ingestion checks

- The resumed crawl initially had 2,147 extracted document records from 1,897 unique URLs. Re-extraction of cached HTML changed the deduplicated record count; current counts are in the collection report. Eight hosts returned access challenges; 13,332 frontier URLs remain pending. Those URLs are not counted as collected.
- All 436 pages across 19 cached PDFs have completed an OCR pass. The full discovered image inventory has completed its four-worker pass: 4,531 successful assets and 69 errors, with 3,172 retained OCR document records. Each worker owns its OCR engines, and one coordinator checkpoints the corpus. Automatic OCR is not equivalent to reviewed text.
- Nine fee/policy images have visually checked, content-hash-bound transcriptions. One is a historical ITCS GPA chart; it is not proof of current eligibility.
- Visual inspection of the FACT training catalogue caught interleaved facing pages. The corrected reading order keeps the PLC 131 and PLC 232 descriptions separate; page 19 was checked against its rendered image.
- Footer contact details were initially removed with navigation. Re-extraction preserves the published NU hotline and address while retaining original download dates.
- DOCX paragraph/table order and XLSX saved values/number formats are covered by an extraction test. Legacy formats and embedded Office images remain unsupported.

Current deterministic verification: 99 pytest tests pass; Ruff and JavaScript syntax checks pass. This does not make the chatbot production-ready.


## Current fixes and verification boundaries

- Separate queries preserve each part of multi-question messages, including Franco application-plus-tuition questions. Retrieved evidence is merged with distinct citation IDs.
- Reviewed general tuition tables take priority for base-rate questions. Certificate-specific, historical GPA and foreign-student policies remain separate; the original full passage stays inspectable in Sources.
- Current-information answers append visible official page links, derived from retrieved NU Egypt/NilePreneurs URLs rather than generated URLs. A link is not a claim that the page was checked live on each message.
- A substantive non-NU question is required before a mixed question receives the specialization notice. The model cannot retain an exact copy of an old app-owned notice on a new non-general turn.
- Windows intermittently rejected local socket creation with WinError 10013 during test-client startup and one browser/API connection. A subsequent ten-socket probe succeeded, and rerunning the deterministic suite passed. No firewall or security settings were changed; the intermittent host issue is not claimed fixed.

The 100-case second full run caught fee-category generalization, certificate-document confusion, an erroneous 50% scholarship audit rejection, and unwanted recruitment pitches. These failures are retained in the report. Subsequent focused runs are separate development retests, not a new production-quality score.


The first link retest exposed an extra application-fee query in a tuition follow-up ([record](runs/links-initial.json)). The next run exposed incorrect mixed classification of two university questions ([record](runs/links-mixed-routing-failure.json)). A later run fixed the notice but still broadened one tuition follow-up ([record](runs/links-before-scope-guard.json)). These mechanically passing answers were rejected during manual review; the subsequent query-scope guard removes unrequested application-charge searches when tuition is being asked.

Reconnect handling now uses a client-generated request UUID and a bounded five-minute in-memory result cache. Duplicate in-flight requests wait for the same generation; a reused UUID with a different validated payload returns 409. The UI retries network failures twice with the same payload/UUID, while retaining a single overall timeout. Model errors are not blindly retried. This improves recovery without claiming to resolve the Windows socket-permission issue.


## Final focused review sequence

| Recorded run | Mechanical checks | Manual review |
| --- | ---: | --- |
| [30 affected scenarios before alias fix](runs/affected-before-alias-fix.json) | 28/30 | 19 pass, 6 partial, 5 fail; exposed admission-step/cost aliases and two transient model failures |
| [11 alias/GPA follow-up retests](runs/aliases-reviewed.json) | 11/11 | 9 pass, 1 partial, 1 fail; the failure caught code being mistaken for grouped citations |
| [8 screenshot scenarios](runs/screenshots-reviewed.json) | 8/8 | 3 pass, 5 partial; fees and application are now retrieved together, but advice remains wordy and dates need consistent presentation |

The final parser patch leaves inline and fenced code untouched when normalizing/counting citations. Reviewed academic-year labels now appear on fee links, even if the generator omits the year in its prose. The old runs above retain their original code/checker versions and failures.

The real HTTP [request-ID replay check](runs/request-replay.json) returned 200 for original and replay (identical body), and 409 for the same UUID with changed input. Unit tests separately verify overlapping callers execute only one generation and that cache capacity cannot evict an active request.

Remaining quality limitations include overly broad advising language, occasional weak historical-policy wording, and an unqualified deadline answer that gives the day without a year or past-date explanation. Current GPA eligibility is not established by the historical image. The host also showed a model-read timeout and intermittent local socket-permission errors. Later successful retries do not erase those failures.


Final checks on the delivered code: [the exact tuition/application screenshot conversations](runs/delivery.json) passed both mechanical and manual review (two scenarios, four turns). Both parts are answered; follow-up stays on tuition; the official fee link shows 2026/2027; ITCS base 193680 EGP and conditional 50% amount 96840 EGP are correct. [The mixed coding scenario](runs/code-final.json) now preserves valid `my_list = [1, 2, 3]` code and omits the notice on the acknowledgment. These three targeted scenarios are not a new full-100 accuracy score.
