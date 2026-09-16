# Independent human-style query evaluation — frozen protocol

This is a new, agent-authored test set and an AI-reviewed evaluation. No recruited human participants or independent human reviewers took part. The reviewer also has implementation context, so this is independent of the existing development cases, not an organizationally independent or blinded audit.

## Scope fixed before execution

100 target queries, each submitted exactly once to the real FastAPI `/api/chat` endpoint with automatic language selection. Six queries have explicitly authored history fixtures; those fixtures are not extra chatbot requests. English, Egyptian Arabic and Egyptian Franco are included. Egyptian Arabic is acceptable for Franco input, as requested by the owner. The deployment is entirely local; the current configured generator is Gemma 4 12B, not Qwen.

The test intentionally samples previously untested fact targets and decisions: certificate-specific cases, campus services, clubs, individual courses, research projects, corporate services, image-only transport policies, unavailable real-time information, contextual corrections and general questions. It is a challenge set, not a random sample of real users. Broad domains inevitably overlap the development set; the questions are not paraphrases of its existing questions. The novelty audit retains the closest old prompt for inspection.

Freeze the questions, expectations, contexts, source snapshots, reviewer rules and runner before the first target request. Record SHA-256 hashes, Git revision, effective app health, local model digest, corpus/index/classifier hashes, runtime configuration, and run timestamps. Do not modify the app, index, model, prompt templates, query set or thresholds during this run. No retries or replacements of failed test cases. No model-generated grading and no keyword checks counted as factual passes.

## Reference method

Reference pages are freshly fetched from official Egyptian NU sites into a separate evaluation folder. These are not ingested into the app. Their URLs, fetch times, status, text and content hashes are preserved. The transport image is independently visually read and the relevant facts are transcribed with its URL and hash. Expectations use those public references, not the chatbot's retrieved passages. For unavailable information, lack of evidence is not proof of nonexistence: the expectation is a calibrated answer and a useful confirmation route.

## Predeclared review rubric

Review every full answer against its case expectation, reference snapshot, and returned supporting passages. Mark these dimensions separately:

- Correctness: 2 = all substantive claims correct or uncertainty justified; 1 = minor ambiguity/inaccuracy; 0 = material error, fabricated fact, invalid inference or unsupported certainty.
- Completeness: 2 = addresses every requested part and applies the scenario correctly; 1 = useful but incomplete; 0 = evasion, irrelevant response, or abstention despite a clearly answerable reference.
- Grounding: 2 = substantive NU claims supported by returned evidence/context, or appropriate abstention/general response; 1 = some correct NU claims unsupported by the supplied passages; 0 = citation misrepresentation or unsupported material NU claim.
- Language: 1 = readable requested language (Arabic for Franco accepted); 0 = wrong language or unusable prose.
- Links: 1 = official link supplied for time-sensitive rules, charges, office holders, hours, booking or live confirmation; 0 = needed link missing/misleading; N/A for stable descriptions/general questions. Numbered citations count only when the API includes their actual official URL, matching the UI source links; a raw invented URL never counts.

Pass requires correctness/completeness/grounding all 2, language 1, and links 1 or N/A. Fail if any of the first three dimensions is 0, or HTTP failure/empty answer. Partial is every remaining case. A blanket refusal is not a pass when a verified answer is available. Extra incorrect claims can fail an otherwise correct answer. An accurate short answer is sufficient; exact wording is not required.

Retrieval diagnostics describe whether the returned sources contain the needed evidence (present / partial / absent / not-needed). This measures the passages returned by the whole pipeline, not the encoder alone. It does not prove where a failure originated; classification, retrieval, evidence filtering and generation can all contribute. Record concise reasons and a failure category for each case. Do not present successful HTTP responses as successful answers.

## Reporting

Publish all 100 raw responses, per-case review, source/novelty audit and frozen manifest. Report pass/partial/fail, counts by category/language, HTTP outcomes, median/p95/max latency, representative failures and limitations. Latency is warmed local sequential API end-to-end latency, not time to first token or a concurrency/SSE/browser benchmark. No production-readiness claim follows from a 100-case challenge set. Freeze discrepancies or unexpected interruptions must be disclosed.
