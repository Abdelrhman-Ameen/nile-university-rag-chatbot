# Output smoke review of the optimized 100-scenario run

Reviewed all 100 cases / 116 request results in
[the recorded run](runs/optimized-100.json). This review checks answer behavior,
obvious factual contradictions, the known fee/address fixtures, follow-ups, and
connection outcomes. It is not a fresh independent audit of every external fact
or a replacement for the earlier detailed [Gemma review](GEMMA_REVIEW.md).

The mechanical checker passed every case, and no request failed unexpectedly.
The following response problems still prevent treating that score as factual accuracy:

| Case | Observed issue |
| --- | --- |
| S011 | Assumes feminine gender in an otherwise appropriate empathy response. |
| S017 | Adds unsolicited NU/service branding and a long preamble to a joking request. |
| S030 | Asked for HTML escaping, but gives case-sensitive script-tag removal. The later suggestion to use `html` does not correct the supplied function. |
| S038 | Calls a 170-minute schedule a three-hour block. |
| S041–S043, S085, S088, S090, S095 | Correct Sheikh Zayed address, but sometimes adds a redundant library address or implies it is a separate campus. |
| S059–S060 | Clearly caveat the historical GPA chart, but the link label wrongly appends 2026/2027 from text explaining that it is not confirmed current policy. S059 also volunteers high-school merit information. |
| S061 | Gives only the forum's claimed eleven-year history instead of explaining what UGRF is. |
| S062 | Correct submission formats, then incorrectly says registration is open until June 7 despite the September 14 test date. S064 handles the explicit past-deadline question correctly. |
| S065 | Describes UGRF's frequency without explaining its difference from a graduation project. |
| S081 | Historical GPA caveat is present, but the reply still opens with a source-preface style the user asked to avoid. |
| S096 | Refuses to fabricate guaranteed admission, but generalizes a specific scholarship's extracurricular/research requirements to all admissions. |

Server logs also showed false-positive grounding repairs for UGRF: one audit called
the core claim supported while still returning it in `unsupported_claims`. These
unnecessary repairs add latency and can leave an incomplete final answer. The audit
was retained for this connection/performance change; suppressing it would conceal
errors instead of addressing the remaining answer-quality problem.

Coverage of the remaining outputs, grouped for readability:

| Cases | Review observations |
| --- | --- |
| S001–S004 | NU Egypt identity and independent student-project role, in the expected language. |
| S005–S010 | Short greetings, acknowledgments and thanks without the specialization footer. |
| S012–S016, S018–S020 | Handle emotion/social intent without unrelated admissions retrieval; S017 noted above. |
| S021–S029 | General NLP, math and science explanations with the substantive-general-information footer. Franco input receives Arabic. |
| S031–S035 | Basic code, precision/recall arithmetic, cosine formula and encoder/Franco explanations are useful; code stays intact. |
| S036–S040 | Creative writing and translation use no general-information footer; S038's duration mismatch noted above. Humor quality is subjective. |
| S044–S046 | Online application steps with official links and no blanket abstention. |
| S047–S048 | Four ITCS majors listed without substituting individual course titles. |
| S049–S058 | Known fee fixtures match the reviewed tables: ITCS 193,680 EGP base / 116,208 at 40%; Business 152,640 base; Biotech 91,980 at 50%; international ITCS 185 USD/credit; Egyptian EMBA 3,500 EGP/credit; general international postgraduate 200 USD/credit; exclusions and 60% combined-scholarship cap preserved. |
| S063–S064 | UGRF event date/location and explicitly past June 7 deadline handled correctly. |
| S066–S068 | ConstructX purpose, 150,000 EGP advertised prize pool, and BioTalent secondary-student eligibility answered with sources. |
| S069–S075 | CIS, WINC, NISC, SESC, IPTTO, OSP and NilePreneurs have relevant descriptions. Some marketing language is repeated as fact; no independent reputation assessment was performed. |
| S076–S078 | FACT is identified as FESTO training rather than an invented faculty; SCE and library contact questions get relevant answers. |
| S079–S080 | Rural-residency requirement and no guarantee from a Sawiris nomination are preserved. |
| S082–S090 | Identity clarification, topic switches, acknowledgments, tuition-to-50% follow-up and mixed NU/Python answers complete. S087 yields 96,840 EGP with a dated link. Python `[1, 2, 3]` remains code, not citations. Address verbosity and S081's source preface noted above. |
| S091–S094 | Empty/oversized question, forged system history role and invalid language correctly return 422. |
| S095–S096 | XML-like input does not break the UI; instruction to fabricate guaranteed admission is rejected, with the evidence-scope issue noted above. |
| S097–S100 | Concurrent and immediately consecutive requests complete. Identity bypass works during another job. No stale-busy error. |

Browser follow-ups separately confirmed a correctly linked ITCS base fee and
96,840 EGP at 50%, but the 50% answer unnecessarily included other schools. These
observed content defects are retained explicitly; they were not counted as
connection failures, and they were not treated as fixed by the performance work.
