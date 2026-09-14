# Chatbot evaluation — recorded baseline

All 100 scenarios (116 requests) were executed against the actual `/api/chat` endpoint on September 14, 2026. Every response was then read against its review rubric. This run uses Qwen 3 14B, the English MS MARCO reranker, and the queue/connection fixes. Later fixes and model comparisons are separate runs; they must not overwrite these results.

Mechanical checks: **88/100 scenarios**. HTTP outcomes: `{200: 110, 503: 2, 422: 4}`.
Manual outcomes: `{'pass': 52, 'partial': 17, 'fail': 28, 'gap': 3}`. A mechanical pass is not a manual pass.

For successful non-identity requests, median latency was **7.06 s**, nearest-rank p95 **24.29 s**, and maximum **105.21 s**. This is a development-machine run with OCR/collection work and some browser checks occurring concurrently, not an isolated deployment load test.

Concurrency cases S097–S100 passed: concurrent calculations, identity during generation, immediate consecutive follow-ups, and simultaneous languages. No busy-model rejection occurred in those cases. Unit checks also cover release after exceptions and queue-wait timeout. The queue is bounded and can still reject overload; disconnecting a client does not cancel inference already running.

Important failures include incorrect/incomplete retrieval for some ITCS questions, wrong university routing for named initiatives, poor Franco output, Arabic translation failures, incorrect general explanations, and mixed-request grounding errors. This baseline does **not** meet a production release standard.

The per-case environment records capture the index version. The index changed after the initial general-conversation cases, before university cases began; general messages did not use retrieval. Full answers and cited source metadata are checked in at `runs/qwen14-baseline.json`; the original retrieval excerpts and timings remain in the local `data/scenarios-100-qwen14.json` log. The compact review is checked in as `evaluation/review_qwen14_baseline.json`.

## Manual review

| Scenario | Outcome | Finding |
| --- | --- | --- |
| S001 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S002 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S003 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S004 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S005 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S006 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S007 | partial | Understandable acknowledgment, but awkward Egyptian wording. |
| S008 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S009 | partial | Answers an acknowledgment with a new greeting. |
| S010 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S011 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S012 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S013 | fail | Franco changes the emotion into not wanting something. |
| S014 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S015 | partial | Unnatural wording about seeing the user’s happiness. |
| S016 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S017 | fail | Refuses/does not joke and mixes dialects. |
| S018 | partial | Offers an unsolicited factual anecdote instead of a creative response. |
| S019 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S020 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S021 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S022 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S023 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S024 | partial | Overstates RAG as ensuring accuracy rather than improving grounding. |
| S025 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S026 | partial | Correct basic explanation, but formal Arabic rather than conversational Egyptian. |
| S027 | fail | Awkward mixed-language phrasing and a weak overfitting example. |
| S028 | fail | Answers in English despite Franco being selected. |
| S029 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S030 | fail | Exact lowercase script-tag replacement is presented as general HTML execution protection. |
| S031 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S032 | fail | The example calls a basket ten apples while including two oranges. |
| S033 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S034 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S035 | fail | Confuses Franco with French in an added paragraph. |
| S036 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S037 | partial | Understandable encouragement, with awkward wording and repetition. |
| S038 | fail | Unwanted specialization note; labels a 30-minute slot a 15-minute break. |
| S039 | fail | Incorrect Arabic translation and unnecessary specialization note. |
| S040 | fail | Repetitive, incoherent joke and non-Egyptian dialect. |
| S041 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S042 | partial | Location facts preserved, but nearly all place names remain English. |
| S043 | fail | Franco location wording is not meaningful. |
| S044 | partial | Correct application sequence followed by unrequested transfer rules. |
| S045 | fail | Arabic translation fails and falls back to English; about 60 seconds. |
| S046 | fail | Franco translation fails and falls back to English; about 59 seconds. |
| S047 | fail | Omits Cybersecurity despite the retrieved FAQ listing it. |
| S048 | fail | Retrieves course pages, lists only two programs, and translation fails. |
| S049 | fail | Correct numeric range, but unnatural Arabic and missing clear first-year qualification. |
| S050 | fail | Fails to retrieve the requested ITCS fee despite its presence in the index. |
| S051 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S052 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S053 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S054 | fail | Uses the postgraduate USD 200 rate for an unqualified ITCS undergraduate context. |
| S055 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S056 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S057 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S058 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S059 | gap | No current GPA discount table in this index snapshot; does not invent a discount. |
| S060 | gap | No confirmed current continuing-student GPA mapping; historical image was found later. |
| S061 | fail | Routes a NU UGRF question to general knowledge. |
| S062 | partial | Supports the listed project formats; does not incorporate the external competition guide. |
| S063 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S064 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S065 | partial | Broad comparison is useful, but generalizes an industrial-engineering capstone rule to all graduation projects. |
| S066 | fail | General route invents expansions of IECC and EDECS. |
| S067 | fail | General route invents generic ConstructX prize types. |
| S068 | partial | Omits the secondary-school limitation and STEM category. |
| S069 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S070 | partial | Adds specific research topics without attaching the passage supporting those topics. |
| S071 | fail | Routes a named NU research center to general knowledge. |
| S072 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S073 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S074 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S075 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S076 | partial | Training description is supported; extra internship details need tighter citations. |
| S077 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S078 | gap | Library contact data unavailable in this index; live library TLS failed. |
| S079 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S080 | partial | Correct final answer, but generation/retry latency exceeds 100 seconds. |
| S081 | fail | Repeats poor tuition wording and lacks the requested current GPA mapping. |
| S082 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S083 | fail | Emotion follow-up works, but the initial Arabic application instructions contain mistranslations. |
| S084 | partial | Follow-up location is resolved correctly; application answer adds an unrequested international branch. |
| S085 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S086 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S087 | partial | Correct arithmetic and prices; omits the first-year restriction. |
| S088 | fail | Franco location is malformed and application translation falls back to English. |
| S089 | fail | Fails the initial complete-program-list question. |
| S090 | fail | Mixed university/general question returns HTTP 503. |
| S091 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S092 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S093 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S094 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S095 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S096 | fail | Grounding challenge returns HTTP 503 rather than a useful refusal to assert an unsupported fact. |
| S097 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S098 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S099 | pass | Meets the scenario’s requested behavior in this recorded response. |
| S100 | pass | Meets the scenario’s requested behavior in this recorded response. |

## Retesting

Pending fixes are evaluated in separate result files. Required release checks include correct source-backed numeric answers, complete program lists, readable Arabic/Franco, general answers without fabricated university facts, no unexpected 5xx responses, and acceptable response time under an isolated concurrency run.
