# Findings and repair priorities

The result is **67 pass, 13 partial, 20 fail**. It does not support calling the chatbot production-ready. The strongest groups in this challenge set were campus services (11/11) and individual courses (6/6). Image-based transport questions were the weakest (1/8), followed by context cases (3/6).

## Failures that matter

| Cases | Observed behavior | Implication |
| --- | --- | --- |
| I038–039, I077–081, I092 | Misses fares, refund deductions, minimum rider count and booking conditions visible in the official transport image. Some answers link to unrelated scholarships, field trips or the homepage. | The current pipeline is not delivering the needed image text to generation. Inspect image discovery, OCR content, indexing and final passage selection separately. A larger encoder alone is not a demonstrated fix. |
| I006 | Franco negation in “ma3adetes TOK” is lost; the pipeline treats it as having TOK and answers yes under the stated IB requirements. | Normalization can change the decision itself. Preserve negation and check normalized text against the original question before applying admissions rules. |
| I011, I020, I042, I074 | Missing certificate-specific evidence, a published club email, or the venture-clienting time window despite the facts appearing in independent official references. | Measure coverage at the passage/section level. A large URL count does not prove that a specific fact is retrievable. |
| I051 | A question about GSP Simulatopedia goes through the general route and receives an unsupported explanation. | Entity and intent recognition need to preserve university context for informal names and Franco spelling. |
| I090 | Correct club comparison from history, but the FilmFish claim cites the Pixels page. | A relevant-looking official citation is insufficient: validate each claim against the specific cited passage. |
| I002, I018, I024, I025 | HTTP 503; the local model cannot verify its answer, so the user receives no answer. | Verification failures are service failures, even if other requests are fast. Preserve diagnostic traces and provide a useful, evidence-based fallback without inventing an answer. |
| I054, I057 | English-only replies to Franco input. | Language compliance is inconsistent even when factual content is correct; Arabic replies were explicitly acceptable. |
| I082, I084–085, I088 | No invented seat count, meeting room or inventory, but missing confirmation links, unhelpful one-line abstention, or overgeneralized housing evidence. | Unknown live/personal information needs a clear limit and the right confirmation route. It should not imply the information does not exist. |

Read [all 100 answers](ANSWERS.md) for the exact output, expectation and individual score. These examples are diagnostic observations, not isolated anecdotes substituted for the complete results.

## Repair order

1. Trace one known missing fact from the official page/image through extracted text, chunk storage, retrieval candidates, reranking, filtering and the final prompt. Fix the first point where it is lost; extend the trace to the other missing-fact cases.
2. Preserve negation, certificate names and entities during Franco normalization. Check university-specific routing and follow-up resolution using cases that are separate from this evaluation.
3. Tighten citation-to-claim alignment and stop substituting an unrelated page when evidence is missing. Keep time-sensitive answers tied to their exact official page or image and date.
4. Diagnose the four verification failures and evaluate a calibrated fallback. Then run a separate browser/SSE/concurrency test; this sequential API run does not test reconnection or the previous busy-lock issue.
5. Retest the failed cases as regressions after fixes, then use another unseen evaluation set for the next quality estimate. Do not report improved results on these now-known cases as a new independent score.

No application fixes were made during the evaluation. The requested UI refinement was started after the completed run and its successful frozen-file hash check; it does not change these results.

## Review qualifications

This is an AI-reviewed set of human-style questions, authored and reviewed by the same agent with implementation context. It is independent of the earlier test cases, not an independent human panel. Broad topics overlap older scenarios; the novelty audit records exact and closest textual matches and the protocol describes the distinct-fact-target scope. The score is not an estimate of all future users' success rate.

The source/expectation snapshot was frozen before execution. An extra scientific claim in I070 required a [supplemental post-response check](supplemental_checks.json) of the official full abstract. Its record is separate from the frozen reference snapshot, and no question or rubric was changed.

The results also contain occasional unnecessary promotional copy and university-specialization footers. The frozen rubric did not assign a separate brevity/style score, so this report does not silently introduce one after seeing the answers.
