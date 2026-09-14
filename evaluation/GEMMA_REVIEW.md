# Manual review of 100 scenarios — Gemma second full run

Model: `gemma4:12b`. Code: `63cab9f6a5a80055`. Index: `1789358993852111800`.

All 100 scenarios were sent to the real local chat API. Full responses and source URL metadata are preserved in [the run](runs/gemma-second-full.json). Source passages remain in the local raw report.

**82 pass, 14 partial, 4 fail** after reading the answers; mechanical checks alone reported **97/100**. These are authored development scenarios, not a blind benchmark or production certification. This snapshot precedes the subsequent multipart/tuition/link fixes; targeted retests must not be presented as a new full-100 score.

| Scenario | Verdict | Review |
| --- | --- | --- |
| S001 | pass | Correct NU Egypt identity and student-choice role. |
| S002 | pass | Arabic identity is explicit and independent. |
| S003 | pass | Repeated identity remains correct. |
| S004 | pass | Franco identity input receives Arabic. |
| S005 | pass | Brief greeting; no disclaimer. |
| S006 | pass | Brief Arabic greeting; no extra services. |
| S007 | pass | Brief acknowledgment without coding offer or disclaimer. |
| S008 | pass | Natural thanks response. |
| S009 | pass | Natural acknowledgment. |
| S010 | pass | Natural English thanks response. |
| S011 | partial | Correct empathy without disclaimer, but unnecessarily assumes feminine address. |
| S012 | pass | Calm response to insult with no disclaimer or admissions diversion. |
| S013 | pass | Understands Franco frustration and invites explanation in Arabic. |
| S014 | pass | Acknowledges disappointment without inventing reasons. |
| S015 | pass | Celebrates good mood naturally. |
| S016 | pass | Congratulates exam success. |
| S017 | pass | Playful response without factual disclaimer. |
| S018 | pass | Short appropriate uplifting thought. |
| S019 | pass | Understands sadness in Franco; Arabic reply is understandable. |
| S020 | pass | Venting request receives listening invitation without footer. |
| S021 | partial | Core overfitting concept correct; overstates perfect training performance and inevitable severe failure. |
| S022 | pass | 17 times 23 = 391; correct general note. |
| S023 | pass | Correct basic list/tuple mutability distinction; shallow performance generalization. |
| S024 | pass | Correct RAG expansion and explanation. |
| S025 | pass | Useful basic embedding explanation. |
| S026 | pass | Clear Arabic ML explanation. |
| S027 | pass | Basic mixed-language overfitting explanation is understandable. |
| S028 | pass | Franco AI/ML question understood; Arabic reply correctly explains relationship. |
| S029 | pass | Basic Rayleigh scattering explanation is appropriate. |
| S030 | pass | Uses html.escape for HTML text escaping; avoids the prior exact-tag replacement bug. |
| S031 | pass | Working add function. |
| S032 | pass | Correct precision 7/8 and recall 7/10 example. |
| S033 | partial | Correct cosine formula/range; overstates that any two documents about AI will have high similarity. |
| S034 | pass | Correct encoder/generator distinction; no prior GAN/encoder mistake. |
| S035 | pass | Correct Latin letters/numerals description of Franco as a writing convention. |
| S036 | pass | Four-line poem; no factual footer. |
| S037 | pass | Supportive encouragement without unrelated branding. |
| S038 | pass | Useful 2.5-hour study schedule in the requested language. |
| S039 | pass | Correct requested translation. |
| S040 | pass | Short relevant joke; no factual university claim. |
| S041 | pass | Correct Sheikh Zayed/Giza campus address. |
| S042 | pass | Correct address, although five citations are excessive. |
| S043 | partial | Correct campus but adds a confusing unnecessary second library-address description. |
| S044 | fail | Basic application steps are correct, then repeats misleading certificate-stamping rules including Thanaweya/British Council. Source itself contains the faulty juxtaposition; basic answer should not include these branches. |
| S045 | pass | Correct Arabic application steps only. |
| S046 | partial | Correct steps, but adds unrequested international branch and charges. |
| S047 | pass | Complete ITCS degree list, not individual courses. |
| S048 | pass | All four ITCS degrees identified. |
| S049 | fail | Generalizes IGCSE score thresholds to all applicants and adds USD rates without asking category; base amount alone is correct. |
| S050 | partial | Correct base amount but assumes Thanaweya Amma and adds unrequested scholarship tiers. |
| S051 | pass | 40% discounted first-year amount 116208 EGP is correct. |
| S052 | pass | Business base annual tuition 152640 EGP is correct. |
| S053 | pass | Biotechnology 50% amount 91980 EGP is correct. |
| S054 | pass | Non-Egyptian ITCS 185 USD per credit is supported. |
| S055 | pass | EMBA 3500 EGP per credit is supported. |
| S056 | pass | Postgraduate 200 USD per credit is supported. |
| S057 | pass | Correct exclusion of non-curricular courses from annual tuition. |
| S058 | pass | Up to three partial scholarships, maximum combined 60%. |
| S059 | partial | Historical 40% rule caveat present, but opening is ambiguous and adds an unrequested old fee amount. |
| S060 | pass | Clearly leads with historical/current-unconfirmed status before explaining 3.8 to below 4 bracket. |
| S061 | partial | Repeats undated eleven-year marketing statement; needs event/date qualification. |
| S062 | pass | Submission formats supported. Cited 22nd UGRF passage explicitly includes undergraduate and graduate participants; no false open-deadline claim. |
| S063 | pass | August 19 2026 NU Campus matches indexed event page. |
| S064 | pass | June 7 deadline correctly treated as past. |
| S065 | pass | Useful distinction between forum presentation and a capstone project. |
| S066 | pass | ConstructX format and IECC/EDECS organizers supported. |
| S067 | pass | 150000 EGP total cash prizes and conditional pilot opportunities match event page. |
| S068 | pass | Secondary-school eligibility and biotechnology participation described accurately. |
| S069 | partial | Research areas supported, but repeats university marketing that CIS is a leader as an unqualified fact. |
| S070 | pass | WINC origin and wireless/optical systems research supported by cited passages. |
| S071 | pass | NISC purpose, masters and director/research group match cited pages; current roles should also receive explicit update links. |
| S072 | pass | SESC multidisciplinary engineering research fields supported. |
| S073 | pass | IPTTO faculty IP/commercialization support accurately scoped. |
| S074 | pass | OSP external funding, proposals and stewardship accurately scoped to faculty/staff. |
| S075 | pass | NilePreneurs CBE/NU connection, SME services and sectors supported. |
| S076 | pass | FACT correctly expanded as FESTO training; industrial automation/mechatronics and certificates supported. |
| S077 | pass | Continuing-education and lifelong-learning role supported. |
| S078 | pass | Library email, phone and hours match reviewed public source. |
| S079 | pass | Rural residence requirement answered directly. |
| S080 | partial | Correct no-guarantee answer, but incorrectly routes to advising and appends an unwanted recruitment pitch. |
| S081 | fail | Initial fee answer generalizes IGCSE tiers and volunteers USD. Follow-up historical GPA caveat exists but says entitled before clarifying current policy. |
| S082 | pass | Both repeated identity replies identify NU Egypt and independent project. |
| S083 | pass | Application response followed by empathy, no repeated admissions instructions. |
| S084 | partial | Location follow-up correct; initial application answer adds unrequested international branch and amounts. |
| S085 | pass | Switches from correct campus answer to working addition function with one general note. |
| S086 | partial | Thanks correctly has no note; overfitting explanation overstates that training performance must be perfect. |
| S087 | fail | Base amount correct; immediate 50% follow-up returns HTTP503 after an erroneous evidence-audit rejection. |
| S088 | partial | Franco understood and application steps correct; location response adds confusing unnecessary library location. |
| S089 | pass | Four ITCS majors correct; Biotechnology correctly placed in its own school. |
| S090 | pass | Both NU address and Python list answered; subsequent hmm is brief with no notice. |
| S091 | pass | Blank input rejected with 422. |
| S092 | pass | Oversized input rejected with 422. |
| S093 | pass | Client-supplied system role rejected with 422. |
| S094 | pass | Unsupported language rejected with 422. |
| S095 | pass | Markup treated as text and campus question answered correctly. |
| S096 | partial | Rejects universal admission guarantee correctly, but adds an unwanted recruitment pitch and wrong advising route. |
| S097 | pass | Concurrent arithmetic requests both succeed with correct answers. |
| S098 | pass | Identity bypasses queued explanation; both answers correct. |
| S099 | pass | Immediate hello, arithmetic and thanks all succeed; note only on substantive answer. |
| S100 | pass | Concurrent English/Arabic/identity requests remain independent and all succeed. |
