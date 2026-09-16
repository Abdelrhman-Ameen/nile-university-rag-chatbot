# All 100 answers and their reviews

AI-reviewed human-style challenge set. Scores and references were defined before execution. Every case is included, including failures. Full returned source passages and pipeline diagnostics are in `responses.jsonl`.

## I001 — PASS

**Question (en):** If I pay NU's application charge and then choose another university, can I get that charge back?

**Expected:** Application fee is non-refundable; distinguish application charge from tuition; link the admissions page.

**HTTP:** 200 · **Latency:** 5.743 seconds

**Answer:**

No, the application fee for Nile University is non-refundable [1].

Official pages for details and updates: [Introduction](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correctly states application fee non-refundable and supplies official page.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Introduction — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I002 — FAIL

**Question (ar):** أنا أمريكان ودرست عاشرة وحادية عشرة وتانية عشرة في ٣ مدارس مختلفة جوه مصر. ينفع شهادة آخر مدرسة بس للنيل؟

**Expected:** Separate stamped transcripts for each grade, not just final school; General Examinations Department stamps.

**HTTP:** 503 · **Latency:** 19.941 seconds

**Answer:**

{'detail': 'The local model could not verify its answer. Please retry.'}

**Review:** HTTP 503: local model could not verify its answer. Server log shows both verification attempts rejected; no answer delivered. Evidence not returned, so retrieval cannot be diagnosed.

**Scores:** correctness 0/2; completeness 0/2; grounding 0/2; language 0/1; links 0. Evidence: unavailable.

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I003 — PASS

**Question (franco):** ana IG w 3andy 8 O levels bas core mesh extended. yenfa3o lel NU?

**Expected:** Core does not meet the published extended-only requirement; no admission guarantee.

**HTTP:** 200 · **Latency:** 8.229 seconds

**Answer:**

عشان تتقبل في جامعة النيل (NU) بشهادة الـ IGCSE، لازم تقدم شهادات لـ 8 مواد في الـ O-Level بتقدير لا يقل عن "C" أو "4". بس لازم تكون المواد دي من نظام الـ extended مش الـ core [1] [4].

التفاصيل والتحديثات على الصفحات الرسمية: [IGCSE](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correctly excludes core O-levels, with relevant IGCSE evidence and Arabic reply to Franco.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [IGCSE — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [4] [IGCSE — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I004 — PASS

**Question (en):** My IGCSE subjects were completed five years before I plan to enroll at NU. Does the published time window cover me?

**Expected:** Published window is four years before enrollment; five years is outside it.

**HTTP:** 200 · **Latency:** 7.259 seconds

**Answer:**

No, the published time window does not cover your situation. Applicants must have completed their IGCSE subjects within the four years before university enrollment [1] [2].

Official pages for details and updates: [IGCSE](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Applies the four-year window correctly to a five-year-old certificate.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [IGCSE — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [2] [IGCSE — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I005 — PASS

**Question (ar):** للتقديم لهندسة النيل بالـIG، عندي المواد المطلوبة في O level ومعايا AS Math بدرجة D. لازم أجيب A level كمان؟

**Expected:** Published requirement permits one AS or AL Mathematics at minimum D; not both.

**HTTP:** 200 · **Latency:** 10.378 seconds

**Answer:**

عشان تقدمي في School of Engineering and Applied Sciences بالـ IG، المطلوب هو 8 مواد O-Level بتقدير لا يقل عن C، لازم يكون من ضمنهم (English, Maths, Physics, Chemistry). وبالنسبة لمادة الـ Math، مطلوب منك مادة واحدة بس تكون AS أو AL Math بتقدير لا يقل عن D [1] [2].

بناءً على المتطلبات، وجودك على AS Math بدرجة D كافي كبديل لـ AL Math في حالة تقديمك لـ Engineering & Applied Sciences، ومش لازم تاخدي A-level عشان متطلبات القبول الأساسية [1] [2].

التفاصيل والتحديثات على الصفحات الرسمية: [IGCSE](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correctly treats AS Math D as the stated alternative to AL, alongside O-level requirements.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [IGCSE — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [2] [IGCSE — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I006 — FAIL

**Question (franco):** ana IB 24 points bas ma3adetes TOK. el 24 keda kefaya lel Nile?

**Expected:** 24 points alone insufficient; must pass TOK and Extended Essay.

**HTTP:** 200 · **Latency:** 22.598 seconds

**Answer:**

أيوه، الـ 24 نقطة هي الحد الأدنى المقبول (minimum accepted point) لطلبة الـ IB في جامعة النيل [1]. لازم كمان تكوني مخلصة مواد الـ Extended Essay و Theory of Knowledge (TOK) [1]. 

جامعة النيل بتقدم فرص مميزة جداً ممكن تساعدك في مستقبلك، زي الـ Undergraduate Research Forum (UGRF) اللي بيتم فيه تقييم ونشر الأبحاث العلمية للطلبة في كل السنوات الدراسية [3]، ومركز الـ IECC اللي بيقدم دعم في ريادة الأعمال وتطوير المنتجات [4]. كمان فيه برامج تبادل طلابي (Exchange programs) في مجالات زي الهندسة، البيزنس، والـ IT في جامعات دولية في أمريكا، فرنسا، وأوروبا [5]. 

إيه هو التخصص اللي بتخططي تدخليه في الجامعة؟

التفاصيل والتحديثات على الصفحات الرسمية: [International Baccalaureate  IB](https://nu.edu.eg/admission-requirement-and-documents) · [Home page](https://ugrf.nu.edu.eg/) · [Innovation Entrepreneurship and competitiveness Centre  IECC , is Nile University’s leading center t](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/) · [Student Exchange Programs](https://nu.edu.eg/student-exchange).

**Review:** Answers yes to sufficiency despite failed TOK, then says subjects must be completed rather than passed. Pipeline normalizes 'ma3adetes TOK' to 'with TOK'; relevant pass requirement was retrieved. Irrelevant promotional material follows.

**Scores:** correctness 0/2; completeness 1/2; grounding 1/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [International Baccalaureate (IB) — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [3] [Home page | UGRF - Undergraduate Research Forum](https://ugrf.nu.edu.eg/)
- [4] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round - IECC](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/)
- [5] [Student Exchange Programs — Student Exchange | NU](https://nu.edu.eg/student-exchange)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I007 — PASS

**Question (en):** For an IB applicant to NU engineering, can Mathematics and Physics both be Standard Level?

**Expected:** Both Mathematics and Physics must be Higher Level for the stated schools.

**HTTP:** 200 · **Latency:** 6.684 seconds

**Answer:**

No, for the Engineering & Applied Sciences, Information Technology & Computer Science, and Energy and Environmental Engineering School majors, Math and Physics are required at a higher level [1].

Official pages for details and updates: [International Baccalaureate  IB](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correctly requires Higher Level Mathematics and Physics, not Standard Level.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [International Baccalaureate (IB) — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I008 — PASS

**Question (ar):** أنا IB وعايز بيوتكنولوجي في النيل؛ أنهي مادتين لازم يكونوا HL بالذات؟

**Expected:** Chemistry and Biology HL.

**HTTP:** 200 · **Latency:** 9.182 seconds

**Answer:**

لو أنت طالب IB وعايز تدخل تخصص Biotechnology في Nile University، لازم يكون عندك مادتين هما Chemistry و Biology في مستوى الـ higher level (HL) [1].

بشكل عام، عشان تقدم في الـ IB، لازم تكون مخلص الـ Baccalaureate diploma degree ومخلص الـ Extended Essay والـ Theory of Knowledge، ويكون عندك 6 مواد (3 منهم HL و 3 في مستوى الـ standard level) مع تحقيق حد أدنى 24 نقطة [1].

التفاصيل والتحديثات على الصفحات الرسمية: [International Baccalaureate  IB](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correctly identifies Chemistry and Biology HL; supporting IB checklist returned.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [International Baccalaureate (IB) — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I009 — PASS

**Question (franco):** law geebt scores 3alya fi AP, NU hat7sebholy credits automatic?

**Expected:** High AP scores may earn transfer credits; not automatic or guaranteed.

**HTTP:** 200 · **Latency:** 8.186 seconds

**Answer:**

بالنسبة لطلاب الـ American Diploma، جامعة النيل (NU) ممكن تمنحك تحويل ساعات معتمدة (transfer credits) لو كنت حاصل على درجات عالية في كورسات الـ Advanced Placement (AP) [3]. لكن مفيش ذكر إن التحويل ده بيتم بشكل تلقائي (automatic)؛ العملية بتعتمد على تقييم الدرجات والسياسات المتبعة [3].

التفاصيل والتحديثات على الصفحات الرسمية: [American Diploma](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Preserves discretionary AP credit wording and explicitly rejects automatic transfer.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [3] [American Diploma — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I010 — PARTIAL

**Question (en):** I hold a Nile Schools certificate. For NU engineering, is one Level 3 Mathematics subject an alternative to two Level 2 subjects?

**Expected:** Yes in the published track, alongside seven required L1 subjects; L3 Maths alternative, not a substitute for all requirements.

**HTTP:** 200 · **Latency:** 8.258 seconds

**Answer:**

For the School of Engineering & Applied Sciences, Information Technology & Computer Science, and Energy and Environmental Engineering, the requirement for students with a Nile Schools certificate is 2 L2 subjects, which can include math with one of the following: biology, physics, chemistry, or 1 L3 Math [1] [2].

Official pages for details and updates: [Nile Schools](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Repeats the source's awkward OR wording, presenting two L2 subjects as the requirement while listing one L3 within it. Does not clearly answer the alternative question or mention the accompanying L1 requirement. Source wording itself is ambiguous; not treated as a proven false policy.

**Scores:** correctness 1/2; completeness 1/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Nile Schools — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [2] [Nile Schools — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I011 — FAIL

**Question (ar):** معايا شهادة كندية وعايز بيوتكنولوجي النيل. Biology في grade 12 بس كفاية؟

**Expected:** Biology is required in both grades 11 and 12.

**HTTP:** 200 · **Latency:** 27.548 seconds

**Answer:**

بخصوص دراسة الـ Biotechnology في Nile University، الـ program بيقدم تخصصين هما Applied Biotechnology و Bioinformatics [1] [2]. بالنسبة لمتطلبات القبول، الـ requirements بتختلف حسب نوع الشهادة؛ لو الشهادة هي IGCSE، لازم تقدم 8 مواد بـ minimum grade "C" أو "4"، ولازم يكون من ضمنهم English و Maths و Physics و Chemistry و Biology [8]. لو الشهادة هي IB، لازم تكون خلصت الـ Baccalaureate diploma ومعاك 6 مواد (3 في مستوى أعلى و 3 في مستوى قياسي)، ولازم يكون Chemistry و Biology في مستوى أعلى (higher level) [6].

بما إنك معاك شهادة كندية، الـ information المتاحة مش بتحدد الـ equivalence بتاعها للـ IGCSE أو الـ IB، لكن الـ Biotechnology school بتطلب وجود مواد معينة زي Chemistry و Biology [6] [8]. الـ documents المطلوبة للـ undergraduate applicants بتشمل الـ online application، والـ transcript الموثق، وشهادة الميلاد المميكنة [9] [10].

التفاصيل والتحديثات على الصفحات الرسمية: [Biotechnology Program](https://nu.edu.eg/academics/undergraduate-programs/biotechnology) · [International Baccalaureate  IB](https://nu.edu.eg/admission-requirement-and-documents) · [What are the admission documents?](https://itcs.nu.edu.eg/apply-now).

**Review:** Does not answer grade 11 versus grade 12 for Canadian Biology. Gives IGCSE/IB requirements and an unhelpful equivalence discussion instead; Canadian section is absent from returned passages although present on the official page.

**Scores:** correctness 1/2; completeness 0/2; grounding 1/2; language 1/1; links 1. Evidence: absent.

**Returned citations:**

- [1] [Biotechnology Program | NU](https://nu.edu.eg/academics/undergraduate-programs/biotechnology)
- [2] [Biotechnology Program | NU](https://nu.edu.eg/academics/undergraduate-programs/biotechnology)
- [6] [International Baccalaureate (IB) — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [8] [IGCSE — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [9] [What are the admission documents? — Apply Now | Information Technology and Computer Science School](https://itcs.nu.edu.eg/apply-now)
- [10] [What are the admission documents? — Apply Now | Information Technology and Computer Science School](https://itcs.nu.edu.eg/apply-now)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I012 — PASS

**Question (franco):** ana masry thanaweya 3amma w ma3andish passport. da ye3attal wara2 el ta2deem lel NU?

**Expected:** Passport copy optional for Egyptians; mandatory for non-Egyptians; national ID still required.

**HTTP:** 200 · **Latency:** 17.883 seconds

**Answer:**

لا، عدم وجود جواز سفر مش هيعطل ورق التقديم بتاعك لأنك مصري. الأوراق المطلوبة للتقديم في جامعة النيل (NU) للطلاب المصريين بتشمل شهادة ميلاد كمبيوتر، و6 صور شخصية، ونسخة من الرقم القومي، بالإضافة لنموذج الجيش (2 و 7 أو 6) للذكور. جواز السفر مطلوب فقط للطلاب غير المصريين [2].

التفاصيل والتحديثات على الصفحات الرسمية: [Academic and Non-Academic Requirements:](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correctly says passport is optional for Egyptians and includes national ID. Most direct cited chunk is the Azhar checklist, but its nationality clause matches the fresh Thanawya checklist; avoid certificate mixing in future.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [2] [Academic and Non-Academic Requirements: — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I013 — PASS

**Question (en):** I'm applying to Nile as a non-Egyptian. Is submitting NU's own form enough, or is there a separate government nomination step?

**Expected:** Study in Egypt portal and nomination letter followed by completion with NU; link official page or portal.

**HTTP:** 200 · **Latency:** 10.589 seconds

**Answer:**

For non-Egyptian students, submitting the university's own application form is not the only step; a government nomination is required. You must first apply through the "Study in Egypt" portal (ادرس في مصر) to receive a nomination letter from the ministry of Higher Education and Scientific Research (Foreign Students Department) before completing the application process at Nile University [1] [6].

Official pages for details and updates: [Application Steps](https://nu.edu.eg/office-international-affairs) · [Non Egyptian Students](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correct sequence: Study in Egypt nomination before completing NU application, with official links.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Application Steps — The Office of International Affairs | NU](https://nu.edu.eg/office-international-affairs)
- [6] [Non Egyptian Students — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I014 — PARTIAL

**Question (ar):** عدد الصور الشخصية في تقديم بكالوريوس النيل هو نفسه عددها في تقديم الماجستير؟

**Expected:** Undergraduate six versus master's four passport-size photos.

**HTTP:** 200 · **Latency:** 7.592 seconds

**Answer:**

المعلومات المتاحة بخصوص عدد الصور الشخصية المطلوبة لتقديم البكالوريوس في جامعة النيل غير متوفرة حالياً، بينما يتطلب تقديم الماجستير 4 صور شخصية حديثة [1].

التفاصيل والتحديثات على الصفحات الرسمية: [Master Application Checklist](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correct master's four photos but does not provide undergraduate six; returned evidence contains only postgraduate photo counts. Useful half-answer, not full comparison.

**Scores:** correctness 2/2; completeness 1/2; grounding 2/2; language 1/1; links 1. Evidence: partial.

**Returned citations:**

- [1] [Master Application Checklist — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I015 — PASS

**Question (franco):** PhD NU: bachelor w master men gam3a 7okomeya barra masr. lazm equivalency lel etneen wala private bas?

**Expected:** PhD checklist equivalency for both degrees from private universities OR universities outside Egypt; public foreign degrees included.

**HTTP:** 200 · **Latency:** 9.336 seconds

**Answer:**

لو معاك شهادات البكالوريوس والماجستير من جامعة حكومية بره مصر، لازم تقدم شهادة معادلة (Equivalent Certificate) للشهادتين مع بعض (البكالوريوس والماجستير) لو كانوا من جامعات خاصة أو من بره مصر [5].

التفاصيل والتحديثات على الصفحات الرسمية: [Ph.D. Application Checklist](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correctly applies foreign-degree equivalency to both degrees even though the institution is public.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [5] [Ph.D. Application Checklist — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I016 — PASS

**Question (en):** I'm assembling my NU master's application. How many recommendation letters should I request?

**Expected:** Three recommendation letters.

**HTTP:** 200 · **Latency:** 6.408 seconds

**Answer:**

You should request three recommendation letters for your Master's application at Nile University [1].

Official pages for details and updates: [Master Application Checklist](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Three recommendation letters, directly supported.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Master Application Checklist — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I017 — PASS

**Question (ar):** MSc MOT في النيل: IELTS overall 6.5 وwriting 6.0، كده محقق شرط الإنجليزي؟

**Expected:** No; writing also minimum 6.5 for MSc MOT, not general master's threshold.

**HTTP:** 200 · **Latency:** 8.53 seconds

**Answer:**

لا، الـ score بتاعك مش كفاية لـ MSc MOT. عشان تحقق شرط الإنجليزي لبرنامج MSc MOT، لازم تجيب IELTS score 6.50 and above، بس لازم الـ writing يكون 6.50 and above [4]. الـ score اللي معاك في الـ writing (6.0) أقل من المطلوب [4].

**Review:** Correctly rejects writing 6.0 under MSc MOT's 6.5 writing threshold. Numbered citation resolves to the official admissions URL.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [4] [For English: — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I018 — FAIL

**Question (franco):** PhD MOT fel Nile: TOEFL iBT 95 w writing 26. el score da ykafy?

**Expected:** No; minimum overall 94 and writing 27 for PhD MOT.

**HTTP:** 503 · **Latency:** 17.781 seconds

**Answer:**

{'detail': 'The local model could not verify its answer. Please retry.'}

**Review:** HTTP 503 after answer verification; no answer delivered to the TOEFL writing-threshold scenario.

**Scores:** correctness 0/2; completeness 0/2; grounding 0/2; language 0/1; links 0. Evidence: unavailable.

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I019 — PASS

**Question (en):** For a regular NU master's application outside MOT, does the checklist accept AMIDEAST Institutional TOEFL, and at what score?

**Expected:** ITP administered by AMIDEAST at least 500; distinguish from iBT.

**HTTP:** 200 · **Latency:** 9.766 seconds

**Answer:**

For a regular Master's application at Nile University (excluding the MOT program), the university accepts the ITP (Institutional TOEFL) administered by AMIDEAST with a score of 500 or above [1] [6].

Official pages for details and updates: [Master Application Checklist](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correct AMIDEAST ITP minimum 500. One citation is only the checklist, but another and an uncited master's chunk supply the English threshold.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Master Application Checklist — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [6] [For English: — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I020 — FAIL

**Question (ar):** لو خلصت IG عند grade 11، النيل محتاجة إثبات معين إن التعليم بتاعي مكتمل؟

**Expected:** Proof of completing required education from Educational Administration stamped by General Examinations Department; no invented waiver.

**HTTP:** 200 · **Latency:** 11.704 seconds

**Answer:**

لو خلصت الـ IGCSE عند grade 11، الجامعة بتطلب تقديم شهادات لـ 8 مواد في الـ O-Level بحد أدنى تقدير "C" أو "4" (لازم يكونوا في الـ extended system مش الـ core) [1]. لازم تكون المواد دي خلصت في الأربع سنين اللي قبل التقديم للجامعة [1].

بالنسبة للـ admission documents، لو معاك IGCSE، لازم الشهادات تكون مختومة من الـ British Council، ووزارة الخارجية، وإدارة الامتحانات العامة لو المدرسة جوه مصر، أو الـ British Council ووزارة الخارجية لو المدرسة بره مصر [3].

التفاصيل والتحديثات على الصفحات الرسمية: [IGCSE](https://nu.edu.eg/admission-requirement-and-documents) · [What are the admission documents?](https://itcs.nu.edu.eg/apply-now).

**Review:** Gives general IGCSE subjects and stamps, omitting the specific grade-11 completion proof. Also changes enrollment window to application window. Relevant grade-11 clause not returned.

**Scores:** correctness 1/2; completeness 0/2; grounding 1/2; language 1/1; links 1. Evidence: absent.

**Returned citations:**

- [1] [IGCSE — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [3] [What are the admission documents? — Apply Now | Information Technology and Computer Science School](https://itcs.nu.edu.eg/apply-now)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I021 — PASS

**Question (franco):** French bac bta3y passable. el minimum grade el maktoob 3and NU eh?

**Expected:** Published minimum is passable; subject requirements and current admission rules still apply.

**HTTP:** 200 · **Latency:** 7.521 seconds

**Answer:**

جامعة النيل بتقبل المتقدمين اللي معاهم شهادة الـ French Baccalaureate بحد أدنى تقدير "passable" [1].

التفاصيل والتحديثات على الصفحات الرسمية: [French Baccalaureate](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correctly states the published French-baccalaureate minimum without claiming individual admission.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [French Baccalaureate — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I022 — PASS

**Question (en):** What average and subject count does NU publish for the German Abitur? I'm trying to read that section rather than the American GPA rules.

**Expected:** Average 4, seven subjects in grades 11 and 12 with at least three advanced; do not confuse GPA 2.0.

**HTTP:** 200 · **Latency:** 8.697 seconds

**Answer:**

Nile University accepts applicants with a German Abitur with a minimum average of 4.0 [1]. Students are required to have 7 subjects in Grade 11 and Grade 12, with at least 3 of those subjects at the Advanced level [1].

For specific majors including Engineering & Applied Sciences, Information Technology & Computer Science, and Energy and Environmental Engineering, students must have English, math, physics, and chemistry [1].

**Review:** Accurately gives Abitur average, subject count, grades and advanced subjects; citation resolves to official admissions page.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [German Abitur — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I023 — PASS

**Question (ar):** في شهادة مدارس النيل، هل العربي لازم ضمن Level 1 لو داخل Business في الجامعة؟

**Expected:** Yes; seven L1 subjects include Arabic, English and Maths.

**HTTP:** 200 · **Latency:** 9.092 seconds

**Answer:**

أيوه، لو معاك شهادة مدارس النيل (Nile Schools) وداخل تخصص الـ Business Administration، لازم يكون العربي ضمن الـ 7 مواد اللي فيهم Level 1 [1] [2].

التفاصيل والتحديثات على الصفحات الرسمية: [Nile Schools](https://nu.edu.eg/admission-requirement-and-documents).

**Review:** Correctly confirms Arabic among the seven L1 Business subjects.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Nile Schools — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)
- [2] [Nile Schools — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I024 — FAIL

**Question (franco):** natiget el thanaweya lesa matala3etsh. early admission fel Nile momken abl el grades wala lazm astanna?

**Expected:** Early application may be possible when open before final grades; not confirmation that a current round is open; official application link/page.

**HTTP:** 503 · **Latency:** 26.696 seconds

**Answer:**

{'detail': 'The local model could not verify its answer. Please retry.'}

**Review:** HTTP 503: verification rejected early-admission answer twice; no usable answer delivered.

**Scores:** correctness 0/2; completeness 0/2; grounding 0/2; language 0/1; links 0. Evidence: unavailable.

**Reference:** [faq](https://nu.edu.eg/faqs)

## I025 — FAIL

**Question (en):** NU's FAQ says Oxford B1 but its admissions page says B2. Which one should I rely on before booking the test?

**Expected:** Acknowledge discrepancy, direct applicant to admissions for confirmation with both links; do not invent a definitive reconciliation.

**HTTP:** 503 · **Latency:** 14.172 seconds

**Answer:**

{'detail': 'The local model could not verify its answer. Please retry.'}

**Review:** HTTP 503 on the explicit Oxford B1/B2 source-conflict question; no guidance delivered.

**Scores:** correctness 0/2; completeness 0/2; grounding 0/2; language 0/1; links 0. Evidence: unavailable.

**Reference:** [faq](https://nu.edu.eg/faqs), [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I026 — PASS

**Question (ar):** عيادة الجامعة في أنهي مبنى وأنهي دور؟ أنا في الحرم ومش لاقيها.

**Expected:** Ground floor of UB2.

**HTTP:** 200 · **Latency:** 6.135 seconds

**Answer:**

عيادة جامعة النيل موجودة في الدور الأرضي من مبنى UB2 [3].

**Review:** Correct concise clinic location: ground floor, UB2.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [3] [Health Service | NU](https://nu.edu.eg/students/services-facilities/health-service)

**Reference:** [clinic](https://nu.edu.eg/students/services-facilities/health-service)

## I027 — PASS

**Question (franco):** law ro7t clinic el NU yom gom3a el sa3a 5 ba3d el dohr, teb2a maftoo7a?

**Expected:** Friday closes at 4 pm; 5 pm outside published hours; link current clinic page.

**HTTP:** 200 · **Latency:** 14.348 seconds

**Answer:**

لا، العيادة مش هتكون مفتوحة. العيادة في جامعة النيل بتفتح يوم الجمعة من الساعة 9:00 صباحاً لحد الساعة 4:00 عصراً [1].

التفاصيل والتحديثات على الصفحات الرسمية: [Health Service](https://nu.edu.eg/students/services-facilities/health-service).

**Review:** Final answer correctly says closed at 5pm Friday and provides 9am–4pm hours. Internal refinement corrected an earlier contradictory draft; only final delivered answer scored.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Health Service | NU](https://nu.edu.eg/students/services-facilities/health-service)

**Reference:** [clinic](https://nu.edu.eg/students/services-facilities/health-service)

## I028 — PASS

**Question (en):** If a case is too complicated for NU's campus clinic, does the university describe a hospital transfer procedure?

**Expected:** Transfer under NU medical staff supervision, emergency family contact; no invented hospital name.

**HTTP:** 200 · **Latency:** 8.236 seconds

**Answer:**

Yes, the university specifies that for complicated cases, the medical team will transfer the patient to a hospital under the supervision of NU medical staff [1] [2]. During this process, the medical team will contact the student's emergency number to notify their family [1] [3].

Official pages for details and updates: [Health Service](https://nu.edu.eg/students/services-facilities/health-service).

**Review:** Correct supervised hospital transfer and family notification; no invented destination hospital.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Health Service | NU](https://nu.edu.eg/students/services-facilities/health-service)
- [2] [Health Service | NU](https://nu.edu.eg/students/services-facilities/health-service)
- [3] [Health Service | NU](https://nu.edu.eg/students/services-facilities/health-service)

**Reference:** [clinic](https://nu.edu.eg/students/services-facilities/health-service)

## I029 — PASS

**Question (ar):** أنا في Business وبعاني في المواد. فيه tutoring ببلاش جوه النيل ولا كله دروس بره؟

**Expected:** TLC offers free tutoring for Business students; explain how it helps rather than generic study tips only.

**HTTP:** 200 · **Latency:** 11.531 seconds

**Answer:**

أيوه، فيه tutoring ببلاش جوه Nile University من خلال الـ Teaching Learning Center (TLC). الـ TLC دي مبادرة عشان تساعد طلاب الـ Business School يواجهوا أي academic challenges ويقدروا ينجحوا في دراستهم، وبتوفر tutoring sessions، وworkshops، وfollow-up عشان يساعدوا الطلاب يكونوا empowered وconfident أكتر [6] [7]. 

تقدري تتواصلي مع الـ TLC عشان تطلبي الـ free tutoring sessions، أو لو محتاجة guidance في اختيار الـ major أو في أي academic-related issues [1] [2].

**Review:** TLC free Business tutoring, workshops and follow-up supported; readable though unnecessarily heavy English code-switching.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Support Services | NU](https://nu.edu.eg/students/services-facilities/support-services)
- [2] [Support Services | NU](https://nu.edu.eg/students/services-facilities/support-services)
- [6] [Teaching Learning Center (TLC) — Home page | Business Administration School](https://ba.nu.edu.eg/)
- [7] [Support Services | NU](https://nu.edu.eg/students/services-facilities/support-services)

**Reference:** [support](https://nu.edu.eg/students/services-facilities/support-services)

## I030 — PASS

**Question (franco):** TLC fel Nile momken yesa3edny a5tar major wala howa lel tutoring bas?

**Expected:** TLC also provides major-choice guidance and academic issues assistance.

**HTTP:** 200 · **Latency:** 10.209 seconds

**Answer:**

مركز التعلم (TLC) في جامعة النيل مش بس للدروس الخصوصية (tutoring)؛ هو مبادرة هدفها تساعد طلاب كلية إدارة الأعمال يواجهوا التحديات الأكاديمية ويحققوا نجاح في دراستهم. الطلاب يقدروا يتواصلوا مع الـ TLC عشان يطلبوا جلسات تدريس مجانية، وكمان عشان ياخدوا إرشاد في اختيار التخصص (major) وحل المشاكل المتعلقة بالدراسة [1] [2] [3].

**Review:** Correctly explains major guidance beyond tutoring, with Business scope.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Teaching Learning Center (TLC) — Home page | Business Administration School](https://ba.nu.edu.eg/)
- [2] [Support Services | NU](https://nu.edu.eg/students/services-facilities/support-services)
- [3] [Support Services | NU](https://nu.edu.eg/students/services-facilities/support-services)

**Reference:** [support](https://nu.edu.eg/students/services-facilities/support-services)

## I031 — PASS

**Question (en):** I'm already an NU student and my family's finances suddenly got worse. Is there a needs-based support office, and where can I reach it?

**Expected:** Partial need-based tuition support subject to funds; MeSamir@nu.edu.eg or B floor room 19; not guaranteed scholarship.

**HTTP:** 200 · **Latency:** 9.55 seconds

**Answer:**

Nile University provides partial tuition support for continuing students who demonstrate financial need [1] [2] [3]. This financial aid is subject to the availability of funds and covers tuition fees only [3].

You can contact the Financial Support Office for Students by emailing MeSamir@nu.edu.eg or by visiting the office located on the B floor, room 19 [1] [2].

Official pages for details and updates: [Support Services](https://nu.edu.eg/students/services-facilities/support-services) · [Scholarship Policy:](https://nu.edu.eg/fees-and-financials).

**Review:** Correct fund-dependent partial tuition aid, office email and room. Returned fees page additionally supports tuition-only scope.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Support Services | NU](https://nu.edu.eg/students/services-facilities/support-services)
- [2] [Support Services | NU](https://nu.edu.eg/students/services-facilities/support-services)
- [3] [Scholarship Policy: — Fees and Financials | NU](https://nu.edu.eg/fees-and-financials)

**Reference:** [support](https://nu.edu.eg/students/services-facilities/support-services)

## I032 — PASS

**Question (ar):** عايز حد في النيل يراجع الـCV بتاعي. أروح SEEC ولا SCE؟

**Expected:** SEEC is the appropriate career/resume service; give booking page/form or seec@nu.edu.eg, distinguish similarly named SCE.

**HTTP:** 200 · **Latency:** 11.803 seconds

**Answer:**

لو هدفك هو مراجعة الـ CV عشان تحسن الـ employability بتاعتك وتجهز لسوق العمل، فالأفضل تروح الـ **Skills and Employability Enhancement Center (SEEC)** [1]. الـ SEEC مخصص لمساعدة الطلاب والخريجين في فهم الـ competencies بتاعتهم، وتطوير الـ career path، وتقديم دعم في الـ career exploration والـ professional development [1] [2].

أما الـ **School of Continuing Education (SCE)**، فهي بتركز أكتر على تقديم دورات تدريبية (courses) وورش عمل (workshops) لتعزيز المهارات في مجالات معينة، وبتستهدف الأفراد والشركات لتقديم فرص تعليم مستمر [6] [7].

التفاصيل والتحديثات على الصفحات الرسمية: [SEEC office](https://nu.edu.eg/students/seec) · [SEEC](https://nu.edu.eg/students) · [Why The School of Continuing Education?](https://sce.nu.edu.eg/).

**Review:** Correctly chooses SEEC for CV help, distinguishes SCE and links the official service page. Retrieved SEEC passages are broad career-service descriptions rather than the specific CV section.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: partial.

**Returned citations:**

- [1] [SEEC office — Skills and Employability Enhancement Center | NU](https://nu.edu.eg/students/seec)
- [2] [SEEC — Students | NU](https://nu.edu.eg/students)
- [6] [Why The School of Continuing Education? — Home page | Continuing Education School](https://sce.nu.edu.eg/)
- [7] [Courses — Home page | Continuing Education School](https://sce.nu.edu.eg/)

**Reference:** [seec](https://nu.edu.eg/students/seec)

## I033 — PASS

**Question (franco):** el company talba internship recommendation letter men NU. fe form a2adem 3aleh?

**Expected:** SEEC Internship Letter Request form exists; point to actual form or official SEEC page without inventing URL.

**HTTP:** 200 · **Latency:** 7.045 seconds

**Answer:**

أيوه، فيه نموذج مخصص لطلب خطاب التوصية الخاص بالتدريب (Internship Letter Request Form) تقدر تستخدمه عشان تقدمه للشركة [1].

التفاصيل والتحديثات على الصفحات الرسمية: [3. Career Opportunities and Employment](https://nu.edu.eg/students/seec).

**Review:** Identifies Internship Letter Request Form and links its official parent page without inventing a form URL.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [3. Career Opportunities and Employment — Skills and Employability Enhancement Center | NU](https://nu.edu.eg/students/seec)

**Reference:** [seec](https://nu.edu.eg/students/seec)

## I034 — PASS

**Question (en):** I've graduated from NU already. Are SEEC career services described as available to alumni too?

**Expected:** Yes, students and alumni explicitly included.

**HTTP:** 200 · **Latency:** 8.617 seconds

**Answer:**

Yes, the Skills and Employability Enhancement Center (SEEC) provides services to both students and alumni [1] [2]. These services include professional development, connecting with potential employers, improving employability, and providing tailored career exploration and development [1] [2].

**Review:** Correctly includes alumni in SEEC services.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [SEEC — Students | NU](https://nu.edu.eg/students)
- [2] [SEEC office — Skills and Employability Enhancement Center | NU](https://nu.edu.eg/students/seec)

**Reference:** [seec](https://nu.edu.eg/students/seec)

## I035 — PASS

**Question (ar):** في النيل حد بيعمل mock interviews عشان أتمرن قبل مقابلة الشغل؟

**Expected:** SEEC mock interviews, practice/feedback and official booking/contact route.

**HTTP:** 200 · **Latency:** 9.263 seconds

**Answer:**

أيوه، فيه مكتب اسمه Skills and Employability Enhancement Center (SEEC) في Nile University بيقدم خدمة الـ mock interview sessions. الـ sessions دي بتعمل simulate لـ real interview scenarios عشان تديك practice و constructive feedback وتساعدك تجهز لـ future job opportunities. تقدر تحجز موعد عن طريق إرسال إيميل لـ seec@nu.edu.eg [1].

التفاصيل والتحديثات على الصفحات الرسمية: [9. Interview Preparation & Competency Based Interview Skills](https://nu.edu.eg/students/seec).

**Review:** Correct mock-interview practice/feedback and seec@nu.edu.eg booking route.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [9. Interview Preparation & Competency Based Interview Skills — Skills and Employability Enhancement Center | NU](https://nu.edu.eg/students/seec)

**Reference:** [seec](https://nu.edu.eg/students/seec)

## I036 — PASS

**Question (franco):** maktabet NU momken tsa3edny at3allem a2ayyem el research sources wala heya kotob bas?

**Expected:** Library offers research assistance and effective information use/critical evaluation education.

**HTTP:** 200 · **Latency:** 10.459 seconds

**Answer:**

مكتبة جامعة النيل (NU Library) مش بس كتب، هي بتدعم البحث العلمي والتعليم من خلال توفير موارد متنوعة وتدريب الطلاب على مهارات تقييم المعلومات. المكتبة بتساعد في تعزيز النمو الفكري والإبداع من خلال تعليم الطلاب كيفية استخدام موارد المعلومات بشكل فعال ومهارات التقييم النقدي (critical evaluation skills) [2].

كمان المكتبة بتقدم دعم بحثي وتوفر بيئة دراسية عالية الجودة، وبتسعى لتوفير خدمات وموارد في أشكال متعددة عشان تلبي احتياجات المستخدمين [1] [2].

**Review:** Explains critical evaluation and research assistance beyond book lending.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Goals — Library | NU](https://nu.edu.eg/academics/library)
- [2] [Mission — Library | NU](https://nu.edu.eg/academics/library)

**Reference:** [library](https://nu.edu.eg/academics/library)

## I037 — PASS

**Question (en):** Is the 2026/27 NU bus-price chart charging for the full academic year or for one semester?

**Expected:** Per term/one semester, not annual.

**HTTP:** 200 · **Latency:** 7.243 seconds

**Answer:**

The 2026/2027 bus fees are charged per term (semester) [4].

Official pages for details and updates: [Transportation](https://nu.edu.eg/students/services-facilities/transportation).

**Review:** Correct per-semester charge, supported by HTML and OCR, with transport link.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [4] [Transportation | NU — Bus Fees — Image text](https://nu.edu.eg/students/services-facilities/transportation)

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I038 — FAIL

**Question (ar):** أتوبيس النيل من حدائق الأهرام اشتراكه كام للترم 2026/2027؟ ابعتلي الصفحة كمان.

**Expected:** 9800 EGP per term; current transport page link.

**HTTP:** 200 · **Latency:** 9.873 seconds

**Answer:**

معنديش إجابة مؤكدة عن النقطة دي لسه.

أقرب صفحة رسمية ممكن تراجعها هي [1].

التفاصيل والتحديثات على الصفحات الرسمية: [CIEM Senior students' Field Trip to "Hadayek Al Ahram](https://eas.nu.edu.eg/events?page=3).

**Review:** Fails to provide 9800 EGP and links an unrelated 2022 Hadayek Al Ahram field trip as the nearest official page. Correct transport fee image not retrieved.

**Scores:** correctness 2/2; completeness 0/2; grounding 1/2; language 1/1; links 0. Evidence: absent.

**Returned citations:**

- [1] [CIEM Senior students' Field Trip to "Hadayek Al Ahram — Events | Engineering and Applied Science School](https://eas.nu.edu.eg/events?page=3)

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I039 — FAIL

**Question (franco):** far2 eshterak bus NU ben sheikh zayed w masr el gedida fel term 2026/27 kam?

**Expected:** 8800 versus 15300; difference 6500 EGP per term, linked chart/page.

**HTTP:** 200 · **Latency:** 8.79 seconds

**Answer:**

معلومات أسعار اشتراك الأوتوبيسات لجامعة النيل (NU) في منطقة الشيخ زايد ومصر الجديدة للترم 2026/2027 غير متوفرة في البيانات المتاحة حالياً [1].

التفاصيل والتحديثات على الصفحات الرسمية: [Transportation](https://nu.edu.eg/students/services-facilities/transportation).

**Review:** Abstains instead of giving 8800, 15300 and 6500 difference. Transport HTML retrieved but relevant OCR amounts absent from returned sources.

**Scores:** correctness 2/2; completeness 0/2; grounding 2/2; language 1/1; links 1. Evidence: absent.

**Returned citations:**

- [1] [Transportation | NU](https://nu.edu.eg/students/services-facilities/transportation)

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I040 — PASS

**Question (en):** I'm a complete programming beginner at NU. Does its ICPC community describe a starting level for people like me?

**Expected:** Level 0 teaches basic programming; no need to already be advanced.

**HTTP:** 200 · **Latency:** 9.397 seconds

**Answer:**

Yes, the NU ICPC community offers a specific level for beginners. They provide a training program that includes a "Level 0" which is specifically designed to teach basic programming skills [1] [2] [7].

Official pages for details and updates: [ICPC](https://nu.edu.eg/students/student-activities/icpc).

**Review:** Correct beginner Level 0 with explicit supporting community description.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [ICPC — International Collegiate Programming Contest (ICPC) | NU](https://nu.edu.eg/students/student-activities/icpc)
- [2] [ICPC — International Collegiate Programming Contest (ICPC) | NU](https://nu.edu.eg/students/student-activities/icpc)
- [7] [ICPC — International Collegiate Programming Contest (ICPC) | NU](https://nu.edu.eg/students/student-activities/icpc)

**Reference:** [icpc](https://nu.edu.eg/students/student-activities/icpc)

## I041 — PASS

**Question (ar):** أنا بحب تنظيم الإيفنتات أكتر من السياسة. NIMUN فيه دور ليا ولا لازم أكون مناظر؟

**Expected:** Organizing/administrative branch alongside academic branch; fits event organization.

**HTTP:** 200 · **Latency:** 12.193 seconds

**Answer:**

لو بتحبي التنظيم أكتر من السياسة، فـ NIMUN فيه مكان ليكي في الـ Organizing Committee. الـ committee دي مخصصة للطلاب اللي حابين يشاركوا في الـ planning والـ execution لكل الـ committees طول السنة عشان يضمنوا إن الـ main event يتم تنفيذه بنجاح [1]. 

ممكن تلاقي فرص كويسة جداً في Nile University لأن الجامعة بتركز على الـ learning through innovation وتطبيق الأبحاث من خلال الـ Undergraduate Research Forum (UGRF) [3]. كمان فيه الـ Innovation Entrepreneurship and competitiveness Centre (IECC) اللي بيقدم دعم للـ entrepreneurs والـ innovators في الـ business model و الـ product design [4]. 

إيه الـ specific skills اللي حابة تطوريها في الـ event management؟

التفاصيل والتحديثات على الصفحات الرسمية: [Mission](https://nu.edu.eg/students/student-activities/nimun) · [Home page](https://ugrf.nu.edu.eg/) · [Innovation Entrepreneurship and competitiveness Centre  IECC , is Nile University’s leading center t](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/).

**Review:** Correct Organizing Committee fit. Adds irrelevant UGRF/IECC promotion, but those additional claims are supported; quality-of-style concern rather than factual failure.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Mission — NIMUN (Nile University Model United Nations) | NU](https://nu.edu.eg/students/student-activities/nimun)
- [3] [Home page | UGRF - Undergraduate Research Forum](https://ugrf.nu.edu.eg/)
- [4] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round - IECC](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/)

**Reference:** [nimun](https://nu.edu.eg/students/student-activities/nimun)

## I042 — FAIL

**Question (franco):** 3ayez ata6awwa3 ma3 Wessal NU. fe email lel club?

**Expected:** wessal_nu@nu.edu.eg; charity/volunteering context, not admissions email.

**HTTP:** 200 · **Latency:** 11.163 seconds

**Answer:**

مفيش إيميل محدد مذكور في المعلومات المتاحة للتواصل مع نادي Wessal NU، لكن النادي بيقوم بأنشطة متنوعة زي جمع الملابس للمحتاجين أو لعمال النظافة في الجامعة، وكمان بينظم فعاليات زي "يوم الأيتام" بالتعاون مع اتحاد الطلاب (NUSU). لو حابب تشارك، ممكن تتابع أنشطتهم داخل الحرم الجامعي أو من خلال قنوات التواصل الخاصة بالجامعة. [1] [2] [3] [5] [7]

التفاصيل والتحديثات على الصفحات الرسمية: [Mission](https://nu.edu.eg/students/student-activities/wessal-nu) · [november_newsletter.pdf](https://nu.edu.eg/sites/default/files/2024-12/november_newsletter.pdf) · [NUSU Orphans Day](https://nu.edu.eg/students/student-activities/student-union/nusu-orphans-day) · [Jan Newsletter.indd](https://nu.edu.eg/sites/default/files/2026-03/jan_newsletter.pdf).

**Review:** Does not give the published wessal_nu@nu.edu.eg email. Retrieves mission/history/news rather than contact section; unrelated activity detail does not answer the request.

**Scores:** correctness 2/2; completeness 0/2; grounding 2/2; language 1/1; links 1. Evidence: absent.

**Returned citations:**

- [1] [Mission — Wessal-NU | NU](https://nu.edu.eg/students/student-activities/wessal-nu)
- [2] [From vision to reality: the founders’ story by (Marwa Elbadawy) — Wessal-NU | NU](https://nu.edu.eg/students/student-activities/wessal-nu)
- [3] [november_newsletter.pdf](https://nu.edu.eg/sites/default/files/2024-12/november_newsletter.pdf)
- [5] [NUSU Orphans Day | NU](https://nu.edu.eg/students/student-activities/student-union/nusu-orphans-day)
- [7] [Jan Newsletter.indd](https://nu.edu.eg/sites/default/files/2026-03/jan_newsletter.pdf)

**Reference:** [wessal](https://nu.edu.eg/students/student-activities/wessal-nu)

## I043 — PASS

**Question (en):** Which NU student organization brought back the Meshwary training described as free and UNICEF-approved?

**Expected:** Enactus NU; historical achievement, no claim registrations currently open.

**HTTP:** 200 · **Latency:** 6.518 seconds

**Answer:**

The Enactus Nile University student organization brought back the "Meshwary" training, which is described as being free of charge for university students and approved by the UNICEF authority [1] [2].

**Review:** Correctly identifies Enactus and describes historical training without claiming a current opening.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Achievements — Enactus-NU | NU](https://nu.edu.eg/students/student-activities/enactus-nu)
- [2] [From vision to reality: the founders’ story Enactus Nile University, founded by (Mohamed Asran) — Enactus-NU | NU](https://nu.edu.eg/students/student-activities/enactus-nu)

**Reference:** [enactus](https://nu.edu.eg/students/student-activities/enactus-nu)

## I044 — PASS

**Question (ar):** أنا عايز yoga أو pilates في أنشطة الجامعة، مش فريق كرة. فيه club بيذكر الحاجات دي؟

**Expected:** NU Pack lists Pilates/yoga; no invented timetable.

**HTTP:** 200 · **Latency:** 10.0 seconds

**Answer:**

أيوه، فيه نادي اسمه **NU Pack** بيقدم أنشطة الـ **Pilates** والـ **Yoga** كجزء من الـ **wellness activities** والـ **sports club** بتاع الجامعة [1]. الـ **NU Pack** بيهدف لتوفير **healthy lifestyle** للطلاب وبيقدم كمان **nutrition plans** و **workout plans** و **Zumba classes** [1].

**Review:** Correct NU Pack Pilates/yoga and other supported activities; no invented timetable.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [NU Pack — NU Pack | NU](https://nu.edu.eg/students/student-activities/nu-pack)

**Reference:** [pack](https://nu.edu.eg/students/student-activities/nu-pack)

## I045 — PASS

**Question (franco):** Trojan NU da esports team wala cybersecurity community? by3melo eh?

**Expected:** Cybersecurity community, workshops/sessions/friendly competitions; not esports team.

**HTTP:** 200 · **Latency:** 9.031 seconds

**Answer:**

في جامعة النيل (NU)، فيه مجتمع خاص بالـ cybersecurity اسمه "Trojan Club". النادي ده هدفه يجمع ويدرب الطلاب المهتمين بمجال الأمن السيبراني، وبيوفر لهم خريطة طريق واضحة، وورش عمل، وجلسات تعليمية، ومسابقات ودية عشان يكتسبوا المهارات اللازمة للتميز في المجال ده [4][5].

مفيش معلومات متاحة في المصادر بخصوص وجود فريق esports في الجامعة [4][5].

**Review:** Correctly describes Trojan as cybersecurity with workshops and friendly competitions. Unnecessary esports-information disclaimer does not assert absence of all esports at NU.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [4] [Trojan NU | NU](https://nu.edu.eg/students/student-activities/trojan-nu)
- [5] [Trojan NU | NU](https://nu.edu.eg/students/student-activities/trojan-nu)

**Reference:** [trojan](https://nu.edu.eg/students/student-activities/trojan-nu)

## I046 — PASS

**Question (en):** I want hands-on Adobe Premiere and Photoshop practice at NU. Is there a student club that specifically lists those tools?

**Expected:** Pixels lists these tools and multimedia training/workshops.

**HTTP:** 200 · **Latency:** 10.004 seconds

**Answer:**

Yes, the **Pixels NU** club specifically offers hands-on experience and training in Adobe Premiere Pro and Adobe Photoshop. The club's mission is to provide students with high-quality training and workshops on these industry-standard tools to develop their technical expertise and artistic vision in graphic design, filmmaking, and photography [6] [8] [10].

**Review:** Correct Pixels tools and practical media training, backed by its mission.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [6] [Mission — Pixels NU | NU](https://nu.edu.eg/students/student-activities/pixels-nu)
- [8] [From vision to reality: the founder’s story — Pixels NU | NU](https://nu.edu.eg/students/student-activities/pixels-nu)
- [10] [Pixels — Pixels NU | NU](https://nu.edu.eg/students/student-activities/pixels-nu)

**Reference:** [pixels](https://nu.edu.eg/students/student-activities/pixels-nu)

## I047 — PASS

**Question (ar):** نفسي أعمل فيلم قصير بس عمري ما صورت حاجة. FilmFish بيقبل مبتدئين؟

**Expected:** Yes, no need to be professional; collaborative films and teaching.

**HTTP:** 200 · **Latency:** 6.915 seconds

**Answer:**

أيوه، FilmFish هو أول film club في Nile University ومخصص للناس اللي عايزة تعمل short films وsketches ومشاريع ليها علاقة بالـ art من خلال collaborative projects. مش لازم تكون professional عشان تنضم للـ club، لأن FilmFish بتشارك وتعلّم معلوماتها لكل المهتمين بالتعلم عن الـ film industry [1].

**Review:** Correctly accepts beginner interest in FilmFish; numbered citation supplies official club page.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [FilmFish | NU](https://nu.edu.eg/students/student-activities/clubs/FilmFish)

**Reference:** [film](https://nu.edu.eg/students/student-activities/clubs/FilmFish)

## I048 — PASS

**Question (franco):** GSP NU ma3naha graduate degree? wala student activity? esmha el kamel eh?

**Expected:** Graduate Starter Pack student club/activity, not postgraduate degree.

**HTTP:** 200 · **Latency:** 10.351 seconds

**Answer:**

GSP في جامعة النيل مش درجة دراسية (Graduate Degree)، هي نشاط طلابي (Student Activity) ونادي طلابي. الاسم الكامل ليها هو "Graduate Starter Pack" [1] [2] [3] [4].

الهدف من الـ GSP Club هو مساعدة الطلاب في التحضير لسوق العمل، وتطوير مهاراتهم عشان يلاقوا ويحافظوا على وظيفة بعد التخرج، وكمان بيساعدوهم في بناء الـ CV وتجهيزهم للمقابلات الشخصية [3] [5] [6].

**Review:** Correctly expands Graduate Starter Pack as a student club, not a degree, with supported career-help examples.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [2. Ask GSP Event — GSP | NU](https://nu.edu.eg/students/student-activities/gsp)
- [2] [Graduate Starter Pack (GSP) — GSP | NU](https://nu.edu.eg/students/student-activities/gsp)
- [3] [newsletter_october_2_compressed.pdf](https://nu.edu.eg/sites/default/files/2023-11/newsletter_october_2_compressed.pdf)
- [4] [newsletter_october_2_compressed.pdf](https://nu.edu.eg/sites/default/files/2023-11/newsletter_october_2_compressed.pdf)
- [5] [2. Real-world skills that don’t fit on a transcript — More Than a Degree: How Student Life at Nile University Builds Leaders, Skills, and Confidence | NU](https://nu.edu.eg/articles/how-student-activities-build-leadership-skills-confidence)
- [6] [From vision to reality: the founders’ story by Seif El-Harouney — GSP | NU](https://nu.edu.eg/students/student-activities/gsp)

**Reference:** [gsp](https://nu.edu.eg/students/student-activities/gsp)

## I049 — PASS

**Question (en):** Does IEEE-NU mention a Women in Engineering group, and what is that group for?

**Expected:** WIE supports/promotes women in engineering and encourages girls in STEM.

**HTTP:** 200 · **Latency:** 8.713 seconds

**Answer:**

Yes, IEEE-NU announced the launch of a new affinity group called WIE (Women in Engineering) [1] [2]. This group is designed to provide support and promotion for women in the field of engineering while inspiring young girls to pursue careers in STEM [1] [2].

**Review:** Correct WIE support for women engineers and girls entering STEM.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Achievements — IEEE-NU (Institute of Electrical & Electronics Engineers) | NU](https://nu.edu.eg/students/student-activities/ieeenu)
- [2] [Achievements — IEEE-NU (Institute of Electrical & Electronics Engineers) | NU](https://nu.edu.eg/students/student-activities/ieeenu)

**Reference:** [ieee](https://nu.edu.eg/students/student-activities/ieeenu)

## I050 — PASS

**Question (ar):** NIMUN مقصور على طلبة النيل ولا وصفه بيقول إن ناس من بره الجامعة ممكن تشارك؟

**Expected:** Description includes participants within and outside NU; current registration subject to organizer confirmation.

**HTTP:** 200 · **Latency:** 9.612 seconds

**Answer:**

لا، الـ NIMUN مش مقصورة بس على طلبة جامعة النيل. الـ description بتاعها بيوضح إنها "simulation of the United Nations founded... for participants from within and outside Nile University" [1].

كمان، الـ NIMUN بتنظم فعاليات زي الـ "Junior Nile International Model United Nations (JNIMUN)" اللي بتكون مخصصة للطلبة في المدارس (schools) [3] [4].

التفاصيل والتحديثات على الصفحات الرسمية: [NIMUN  Nile University Model United Nations](https://nu.edu.eg/students/student-activities/nimun) · [july_newsletter_2024.pdf](https://nu.edu.eg/sites/default/files/2024-08/july_newsletter_2024.pdf).

**Review:** Correctly includes outside participants and supports the additional junior-school conference example; no claim that a round is currently open.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [NIMUN (Nile University Model United Nations) — NIMUN (Nile University Model United Nations) | NU](https://nu.edu.eg/students/student-activities/nimun)
- [3] [july_newsletter_2024.pdf](https://nu.edu.eg/sites/default/files/2024-08/july_newsletter_2024.pdf)
- [4] [july_newsletter_2024.pdf](https://nu.edu.eg/sites/default/files/2024-08/july_newsletter_2024.pdf)

**Reference:** [nimun](https://nu.edu.eg/students/student-activities/nimun)

## I051 — FAIL

**Question (franco):** Simulatopedia beta3 GSP kan lecture bas wala kan fe ta3arrof 3ala companies w internships?

**Expected:** Work-life experience involving companies, workshops and selected internship opportunities; no universal internship guarantee.

**HTTP:** 200 · **Latency:** 6.227 seconds

**Answer:**

بص يا سيدي، محاضرات الـ "Bas wala" أو الـ Introductory lectures في الـ GSP بتركز أكتر على أساسيات المجال وتجهيزك للخطوات الجاية.

بالنسبة لموضوع الشركات والـ Internships، هي بتلمح ليهم وبتبدأ توضح لك إزاي السوق شغال، بس مش بتكون هي الهدف الوحيد أو التفصيلي للمحاضرة، هي بتبني لك القاعدة اللي هتحتاجها لما تيجي تقدم في شركة فعلياً.

أنا معمول مخصوص لجامعة النيل في مصر. دي إجابة عامة، مش معلومة متحقَّق منها من مصادر الجامعة.

**Review:** Routes GSP Simulatopedia to general, invents 'Bas wala' introductory lectures and their purpose, with no NU evidence. The generic disclaimer does not make the invented university-specific answer acceptable.

**Scores:** correctness 0/2; completeness 0/2; grounding 0/2; language 1/1; links N/A. Evidence: absent.

**Reference:** [gsp](https://nu.edu.eg/students/student-activities/gsp)

## I052 — PASS

**Question (en):** I like analyzing DNA datasets more than doing wet-lab experiments. What does NU's Bioinformatics description say about genomics and proteomics?

**Expected:** Computational biological data; genomic entities/genes/transcripts and protein sets; distinguish interests without promising job.

**HTTP:** 200 · **Latency:** 10.171 seconds

**Answer:**

Nile University's Bioinformatics program describes genomics as the sequencing and interpretation of all genomic entities, including genes and transcripts, in an organism [1] [2]. Proteomics is defined as the analysis of the entire set of proteins or proteomes [1] [2]. The program notes that Bioinformatics is the key to understanding complex biological systems because it is used by these two large-scale fields, as well as in metabolomics and transcriptomics [1] [2].

**Review:** Correct genomics/proteomics definitions from Bioinformatics description.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Description — About Bioinformatics | Biotechnology School](https://biotech.nu.edu.eg/program/bioinformatics/about-bioinformatics)
- [2] [Description — About Bioinformatics | Biotechnology School](https://biotech.nu.edu.eg/program/bioinformatics/about-bioinformatics)

**Reference:** [bioinfo](https://biotech.nu.edu.eg/program/bioinformatics/about-bioinformatics)

## I053 — PASS

**Question (ar):** Applied Biotechnology في النيل ممكن يوديني لمجال forensic science ولا ده بعيد عن وصف البرنامج؟

**Expected:** Forensic scientist/forensic and molecular labs explicitly listed as possible careers, no employment guarantee.

**HTTP:** 200 · **Latency:** 13.637 seconds

**Answer:**

برنامج الـ Applied Biotechnology في Nile University ممكن يوصلك لمجال الـ forensic science، لأن الـ program description بيوضح إن الخريجين يقدروا يشتغلوا في الـ forensic and molecular biology labs [2]. كمان الـ program بيغطي مجالات تانية كتير زي الـ pharmaceutical research و الـ medical research، وده بيخلي الـ career opportunities واسعة جداً في مجالات الـ healthcare والـ manufacturing [1] [2].

Nile University بتقدم فرص قوية ممكن تساعدك في أهدافك، زي الـ Undergraduate Research Forum (UGRF) اللي بيشجع الـ learning through innovation وبيقدم فرصة لتقييم ونشر الـ scientific research بتاعك [3]. كمان فيه الـ Innovation Entrepreneurship and competitiveness Centre (IECC) اللي بيقدم دعم في الـ innovation management و الـ business model advising لو حابب تحول فكرتك لـ startup [4].

هل عندك اهتمام خاص بجانب معين في الـ forensic science زي الـ DNA analysis أو الـ toxicology؟

**Review:** Correctly includes forensic laboratory careers as possibilities; additional supported promotion is unnecessary but not false.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Biotechnology graduates have very promising career opportunities. Employment opportunities are available with: — About Applied Biotechnology | Biotechnology School](https://biotech.nu.edu.eg/program/applied-biotechnology/about-applied-biotechnology)
- [2] [Description — About Applied Biotechnology | Biotechnology School](https://biotech.nu.edu.eg/program/applied-biotechnology/about-applied-biotechnology)
- [3] [Home page | UGRF - Undergraduate Research Forum](https://ugrf.nu.edu.eg/)
- [4] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round - IECC](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/)

**Reference:** [appliedbio](https://biotech.nu.edu.eg/program/applied-biotechnology/about-applied-biotechnology)

## I054 — PARTIAL

**Question (franco):** ana biomedical engineer. MSc mechatronics NU target graduates zayy wala mechanical bas?

**Expected:** Biomedical engineers explicitly targeted, not limited to mechanical; admission not automatic.

**HTTP:** 200 · **Latency:** 22.122 seconds

**Answer:**

The Master of Science in Mechatronics Engineering at Nile University is an interdisciplinary program that specifically targets engineers, including those with B.Sc. degrees in Biomedical Engineering [1]. It integrates mechanical, electronics, control, and computer engineering to develop automated systems and production technologies [2].

Nile University offers several opportunities that could benefit your career. The Innovation Entrepreneurship and competitiveness Centre (IECC) provides professional support in areas such as product design, engineering development, and business model advising to help innovators bridge resource gaps [4]. Additionally, the university utilizes a credit hour system, which facilitates the transfer of credits from other institutions [5].

What specific area of mechatronics are you most interested in applying to your biomedical engineering career?

**Review:** Correct Biomedical Engineering eligibility and program description, but replies entirely in English to Franco input rather than Egyptian Arabic/Franco.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 0/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Who should apply? — About Master of Science in Mechatronics Engineering | Engineering and Applied Science School](https://eas.nu.edu.eg/program/master-science-mechatronics-engineering/about-master-science-mechatronics-engineering)
- [2] [Master of Science in Mechatronics Engineering | Engineering and Applied Science School](https://eas.nu.edu.eg/program/master-science-mechatronics-engineering)
- [4] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round - IECC](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/)
- [5] [Student Exchange Programs — Student Exchange | NU](https://nu.edu.eg/student-exchange)

**Reference:** [mechatronics](https://eas.nu.edu.eg/program/master-science-mechatronics-engineering/about-master-science-mechatronics-engineering)

## I055 — PASS

**Question (en):** Does NU's software-engineering master's focus only on coding, or does it include requirements, testing and quality assurance?

**Expected:** Requirements, architecture, testing/verification and QA included, alongside development management.

**HTTP:** 200 · **Latency:** 9.576 seconds

**Answer:**

The MSc Software Engineering program at Nile University does not focus only on coding; it includes requirements management, testing, and quality assurance. Students in the program will master the principles of requirements management, analysis modeling, software architecture design, testing and verification, and quality assurance [1]. The program is designed to produce technically astute graduates with solid managerial, leadership, and communication skills to become leaders in the software industry [2].

**Review:** Correctly includes requirements, testing and quality assurance beyond coding.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [The set of skills that MSc Software Engineering students will acquire are the following: — About M.Sc. and Professional Master in Software Engineering | Information Technology and Computer Science School](https://itcs.nu.edu.eg/program/msc-software-engineering/about-msc-and-professional-master-software-engineering)
- [2] [Description — About M.Sc. and Professional Master in Software Engineering | Information Technology and Computer Science School](https://itcs.nu.edu.eg/program/msc-software-engineering/about-msc-and-professional-master-software-engineering)

**Reference:** [software](https://itcs.nu.edu.eg/program/msc-software-engineering/about-msc-and-professional-master-software-engineering)

## I056 — PASS

**Question (ar):** دبلومة Management of Technology في النيل طريق مقفول ولا ممكن بعدها أكمل MSc MOT؟

**Expected:** Certificate holders may pursue MSc MOT; do not promise automatic acceptance/credit transfer.

**HTTP:** 200 · **Latency:** 11.679 seconds

**Answer:**

لا، دبلومة الـ Management of Technology في جامعة النيل مش طريق مقفول؛ الـ Certificate of Proficiency في الـ Management of Technology مصممة بحيث إن الـ holders بتاعها يقدروا يكملوا دراساتهم العليا (postgraduate studies) ويدخلوا الـ MSc in MOT في جامعة النيل [1] [3] [4].

البرنامج ده بيقدم تدريب عملي (hands-on training) ومبني على الـ current industry standards عشان يساعد الـ technical entrepreneurs، والـ curriculum بتاعته بتغطي الـ essential stages والـ tools الخاصة بالـ Management of Technology [1] [2] [4].

التفاصيل والتحديثات على الصفحات الرسمية: [Management of Technology Professional Diploma](https://mot.nu.edu.eg/) · [About Management of Technology Professional Diploma](https://mot.nu.edu.eg/program/management-technology-professional-diploma/about-management-technology-professional-diploma).

**Review:** Correct diploma-to-MSc possibility with supporting hands-on curriculum details; no explicit guaranteed admission or transfer.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Management of Technology Professional Diploma — Home page | Graduate School of Management of Technology](https://mot.nu.edu.eg/)
- [2] [Management of Technology Professional Diploma — Home page | Graduate School of Management of Technology](https://mot.nu.edu.eg/)
- [3] [About Management of Technology Professional Diploma | Graduate School of Management of Technology](https://mot.nu.edu.eg/program/management-technology-professional-diploma/about-management-technology-professional-diploma)
- [4] [About Management of Technology Professional Diploma | Graduate School of Management of Technology](https://mot.nu.edu.eg/program/management-technology-professional-diploma/about-management-technology-professional-diploma)

**Reference:** [motdiploma](https://mot.nu.edu.eg/program/management-technology-professional-diploma/about-management-technology-professional-diploma)

## I057 — PARTIAL

**Question (franco):** master engineering microelectronics NU fe applied project w report wala courses bas?

**Expected:** Advanced courses plus applied project presented in scientific report.

**HTTP:** 200 · **Latency:** 8.138 seconds

**Answer:**

The Master of Engineering in Microelectronics System Design at Nile University involves studying several advanced academic courses in addition to conducting an applied project and presenting it through a scientific report [1] [3] [5].

**Review:** Accurate applied-project plus report requirement, but fully English response to Franco input.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 0/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Master of Engineering in Microelectronics System Design — All Programs | NU](https://nu.edu.eg/all-programs)
- [3] [Master of Engineering in Microelectronics System Design — Home page | Engineering and Applied Science School](https://eas.nu.edu.eg/)
- [5] [Description — Master of Engineering in Microelectronics System Design | Engineering and Applied Science School](https://eas.nu.edu.eg/program/master-engineering-microelectronics-system-design/about-master-engineering-microelectronics-system-design)

**Reference:** [microelectronics](https://eas.nu.edu.eg/program/master-engineering-microelectronics-system-design/about-master-engineering-microelectronics-system-design)

## I058 — PASS

**Question (en):** Which US university is named on NU Integrated Marketing Communications' partnership page?

**Expected:** University of Tennessee; no assumption of guaranteed current seat.

**HTTP:** 200 · **Latency:** 5.775 seconds

**Answer:**

The University of Tennessee, United States, is named on the Integrated Marketing Communications partnership page [1].

**Review:** Correct University of Tennessee named on the partnership page.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Integrated Marketing Communications Partnership | Business Administration School](https://ba.nu.edu.eg/program/integrated-marketing-communications/integrated-marketing-communications-partnership)

**Reference:** [imc](https://ba.nu.edu.eg/program/integrated-marketing-communications/integrated-marketing-communications-partnership)

## I059 — PASS

**Question (ar):** تخصص Supply Chain في النيل بيذكر شغل procurement وinventory فعلًا؟ اديني مثالين من المسارات.

**Expected:** Procurement Officer and Inventory Manager are listed; possible paths, not guaranteed jobs.

**HTTP:** 200 · **Latency:** 12.824 seconds

**Answer:**

أيوه، تخصص الـ Operations Management and Supply Chains (OPMG) في Nile University بيغطي فعلاً مواضيع الـ procurement والـ inventory. الكورسات بتشمل دراسة الـ procurement من خلال مواضيع زي الـ purchasing و الـ material requirement planning [8]، وكمان الـ inventory من خلال دراسة الـ inventory control، الـ production planning، والـ just-in-time (JIT) systems [6].

بالنسبة للمسارات أو الـ career paths المتاحة بعد التخرج، فيه أمثلة زي:
- Procurement Officer [7]
- Inventory Manager [7]

**Review:** Gives both requested career examples and supported relevant course topics without employment guarantees.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [6] [Inventory Management | Business Administration School](https://ba.nu.edu.eg/program/supply-chain-and-logistics/courses/inventory-management)
- [7] [Supply Chain and Logistics Skills and Career path | Business Administration School](https://ba.nu.edu.eg/program/supply-chain-and-logistics/supply-chain-and-logistics-skills-and-career-path)
- [8] [Logistics and Materials Management | Business Administration School](https://ba.nu.edu.eg/program/supply-chain-and-logistics/courses/logistics-and-materials-management)

**Reference:** [supply](https://ba.nu.edu.eg/program/supply-chain-and-logistics/supply-chain-and-logistics-skills-and-career-path)

## I060 — PARTIAL

**Question (franco):** meen el program director beta3 Professional Diploma in Food Safety Management fel Nile?

**Expected:** Prof Sobhy Ahmed El-Sohaimy; current official program page link.

**HTTP:** 200 · **Latency:** 7.514 seconds

**Answer:**

مدير برنامج Professional Diploma in Food Safety Management (PD-FSM) في جامعة النيل هو الأستاذ الدكتور صبحي أحمد السوهايمي [1][2].

التفاصيل والتحديثات على الصفحات الرسمية: [Professional Diploma in Food Safety Management  PD-FSM  Program Director](https://biotech.nu.edu.eg/program/professional-diploma-food-safety-management/professional-diploma-food-safety-management-pd).

**Review:** Correct director matches the fresh reference, but returned chunks contain only the page heading and a biography tail naming El-Sohaimy, not the full Sobhy Ahmed name. Citation context is incomplete.

**Scores:** correctness 2/2; completeness 2/2; grounding 1/2; language 1/1; links 1. Evidence: partial.

**Returned citations:**

- [1] [Professional Diploma in Food Safety Management (PD-FSM) Program Director — Professional Diploma in Food Safety Management (PD-FSM) Program Director | Biotechnology School](https://biotech.nu.edu.eg/program/professional-diploma-food-safety-management/professional-diploma-food-safety-management-pd)
- [2] [Prof. Sobhy Ahmed El-Sohaimy — Professional Diploma in Food Safety Management (PD-FSM) Program Director | Biotechnology School](https://biotech.nu.edu.eg/program/professional-diploma-food-safety-management/professional-diploma-food-safety-management-pd)

**Reference:** [food](https://biotech.nu.edu.eg/program/professional-diploma-food-safety-management/professional-diploma-food-safety-management-pd)

## I061 — PASS

**Question (en):** At NU, what are the course code and credit hours for Cost Accounting, and does it include activity-based costing?

**Expected:** ACCT 303, 3 credits, activity-based costing included.

**HTTP:** 200 · **Latency:** 8.594 seconds

**Answer:**

The Cost Accounting course (ACCT 303) is offered at the undergraduate level and carries 3 credit hours [1]. The course includes coverage of activity based costing as part of its curriculum [1].

Official pages for details and updates: [Cost Accounting](https://ba.nu.edu.eg/program/general-business-and-entrepreneurship/courses/cost-accounting).

**Review:** Accurate ACCT 303, three credits and activity-based costing.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Cost Accounting | Business Administration School](https://ba.nu.edu.eg/program/general-business-and-entrepreneurship/courses/cost-accounting)

**Reference:** [accounting](https://ba.nu.edu.eg/program/general-business-and-entrepreneurship/courses/cost-accounting)

## I062 — PASS

**Question (ar):** MOT 602 في جامعة النيل بيتكلم عن إيه؟ وهو بكالوريوس ولا دراسات عليا؟

**Expected:** Innovation Management and Product Development Management, postgraduate MSc MOT; explain relevant content.

**HTTP:** 200 · **Latency:** 11.719 seconds

**Answer:**

كورس MOT 602 في جامعة النيل بعنوان "Innovation Management & Product Development Management"، وبيركز على الـ managerial skills والـ professional expertise المطلوبة عشان تحول منتج أو خدمة من مرحلة الـ concept لـ market بسرعة ونجاح. الكورس بيغطي مواضيع زي الـ innovation types، الـ R&D، الـ product development، الـ pricing policies، الـ Intellectual Property Rights، والـ Innovation Capability Audit [1] [2].

بالنسبة لمستوى الدراسة، الكورس ده ضمن برنامج الـ M.Sc. in Management of Technology، وده معناه إنه دراسات عليا (Postgraduate) مش بكالوريوس [1] [2].

التفاصيل والتحديثات على الصفحات الرسمية: [Innovation Management & Product Development Management](https://mot.nu.edu.eg/program/msc-management-technology/courses/innovation-management-product-development-management).

**Review:** Correct MOT 602 title, topics and postgraduate level.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Innovation Management & Product Development Management | Graduate School of Management of Technology](https://mot.nu.edu.eg/program/msc-management-technology/courses/innovation-management-product-development-management)
- [2] [Innovation Management & Product Development Management | Graduate School of Management of Technology](https://mot.nu.edu.eg/program/msc-management-technology/courses/innovation-management-product-development-management)

**Reference:** [innovationcourse](https://mot.nu.edu.eg/program/msc-management-technology/courses/innovation-management-product-development-management)

## I063 — PASS

**Question (franco):** BMD101 fel Nile fe DNA replication w Mendelian genetics? w kam credit?

**Expected:** Biology and Genetics includes both, 3 credits.

**HTTP:** 200 · **Latency:** 8.721 seconds

**Answer:**

أيوه، كورس BMD101 (Biology and Genetics) في برنامج الـ Biomedical Informatics في جامعة النيل بيغطي مواضيع الـ DNA Structure and Replication والـ Mendelian Genetics and Inheritance [1]. الكورس ده بيتحسب بـ 3 ساعات معتمدة (3 Credit Hours) [1] [2].

التفاصيل والتحديثات على الصفحات الرسمية: [Biology and Genetics](https://itcs.nu.edu.eg/program/biomedical-informatics/courses/biology-and-genetics).

**Review:** Correct BMD101 DNA/genetics coverage and three credits.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Biology and Genetics | Information Technology and Computer Science School](https://itcs.nu.edu.eg/program/biomedical-informatics/courses/biology-and-genetics)
- [2] [Biology and Genetics | Information Technology and Computer Science School](https://itcs.nu.edu.eg/program/biomedical-informatics/courses/biology-and-genetics)

**Reference:** [bmd101](https://itcs.nu.edu.eg/program/biomedical-informatics/courses/biology-and-genetics)

## I064 — PASS

**Question (en):** For NU's BIO 203 Genetics-I, is there practical work as well as theory? Give one example of the practical component.

**Expected:** Yes; cultures/genetic variation/breeding/gene analysis etc supported practical example.

**HTTP:** 200 · **Latency:** 8.523 seconds

**Answer:**

Yes, the BIO 203 Genetics-I course includes both theoretical and practical components [1] [2]. The practical portion of the course involves activities such as establishing the culture of different organisms and observing their genetic variance [1] [2].

**Review:** Correct practical component with organism cultures and genetic variation example.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Genetics-I | Biotechnology School](https://biotech.nu.edu.eg/program/bioinformatics/courses/genetics-i)
- [2] [Genetics-I | Biotechnology School](https://biotech.nu.edu.eg/program/bioinformatics/courses/genetics-i)

**Reference:** [genetics](https://biotech.nu.edu.eg/program/bioinformatics/courses/genetics-i)

## I065 — PASS

**Question (ar):** CBIO 203 بيتاخد في أنهي semester وعدد ساعاته كام؟

**Expected:** Semester 4, 2 credit hours; distinguish from BIO203 semester3/3credits.

**HTTP:** 200 · **Latency:** 6.953 seconds

**Answer:**

كورس CBIO 203 (Introduction to Bioinformatics and Biological Databases) بيتاخد في الـ Semester 4، وعدد الـ Credit Hours بتاعته هو 2 [1].

التفاصيل والتحديثات على الصفحات الرسمية: [Introduction to Bioinformatics and Biological Databases](https://biotech.nu.edu.eg/program/bioinformatics/courses/introduction-bioinformatics-and-biological-databases).

**Review:** Correct semester four and two credits; avoids confusion with BIO203.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Introduction to Bioinformatics and Biological Databases | Biotechnology School](https://biotech.nu.edu.eg/program/bioinformatics/courses/introduction-bioinformatics-and-biological-databases)

**Reference:** [databases](https://biotech.nu.edu.eg/program/bioinformatics/courses/introduction-bioinformatics-and-biological-databases)

## I066 — PASS

**Question (franco):** course Introduction to Bioinformatics and Biological Databases fel NU beyesta5dem public repositories wala database design general bas?

**Expected:** Retrieving/manipulating/analyzing biological data from public repositories; introduction to high throughput NGS analysis.

**HTTP:** 200 · **Latency:** 9.009 seconds

**Answer:**

في كورس "Introduction to Bioinformatics and Biological Databases" في جامعة النيل (NU)، بيتم التركيز على استرجاع ومعالجة وتحليل البيانات البيولوجية المتاحة على المستودعات العامة (public online repositories) [1]. الكورس بيقدم دليل تمهيدي مطلوب لتحليل بيانات الـ NGS (Next-Generation Sequencing) البيولوجية [1].

**Review:** Correct public biological repositories and NGS-analysis orientation.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Introduction to Bioinformatics and Biological Databases | Biotechnology School](https://biotech.nu.edu.eg/program/bioinformatics/courses/introduction-bioinformatics-and-biological-databases)

**Reference:** [databases](https://biotech.nu.edu.eg/program/bioinformatics/courses/introduction-bioinformatics-and-biological-databases)

## I067 — PASS

**Question (en):** Could NU's mechatronics master's support research on unmanned vehicles and smart materials, or are those outside its listed topics?

**Expected:** Both unmanned vehicles and smart materials/structures are listed research topics.

**HTTP:** 200 · **Latency:** 11.633 seconds

**Answer:**

Yes, the Master of Science in Mechatronics Engineering at Nile University supports research in both unmanned vehicles and smart materials. These topics are explicitly listed as categories within the master's program research scope [1].

**Review:** Both unmanned vehicles and smart materials correctly identified in research scope.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Description — About Master of Science in Mechatronics Engineering | Engineering and Applied Science School](https://eas.nu.edu.eg/program/master-science-mechatronics-engineering/about-master-science-mechatronics-engineering)

**Reference:** [mechatronics](https://eas.nu.edu.eg/program/master-science-mechatronics-engineering/about-master-science-mechatronics-engineering)

## I068 — PASS

**Question (ar):** مشروع النيل بتاع تغليف بقشر الجمبري: الشريك مين والتمويل منين؟

**Expected:** University of Nottingham partner; STDF funding.

**HTTP:** 200 · **Latency:** 9.052 seconds

**Answer:**

مشروع جامعة النيل الخاص بتغليف قشر الجمبري (Valorization of Shrimp shells and Agricultural Wastes for Sustainable Biopolymer-Based Packaging Solutions) بيتم بالتعاون مع جامعة نوتنغهام (University of Nottingham) [1][2]. أما التمويل الخاص بالمشروع فبيكون من (STDF) [1][2].

**Review:** Correct Nottingham partner and STDF funder for shrimp-shell packaging.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Valorization of Shrimp shells and Agricultural Wastes for Sustainable Biopolymer-Based Packaging Solutions | NU](https://nu.edu.eg/projects/valorization-shrimp-shells-and-agricultural-wastes-sustainable-biopolymer-based-packaging)
- [2] [Valorization of Shrimp shells and Agricultural Wastes for Sustainable Biopolymer-Based Packaging Solutions | NU](https://nu.edu.eg/projects/valorization-shrimp-shells-and-agricultural-wastes-sustainable-biopolymer-based-packaging)

**Reference:** [materials](https://nu.edu.eg/projects/valorization-shrimp-shells-and-agricultural-wastes-sustainable-biopolymer-based-packaging)

## I069 — PASS

**Question (franco):** soft robot beta3 coral reefs fi NU el fund men ASRT wala STDF?

**Expected:** ASRT for coral robot, do not conflate with shrimp packaging STDF.

**HTTP:** 200 · **Latency:** 8.91 seconds

**Answer:**

مشروع الـ soft robot لمراقبة الشعاب المرجانية (Coral Reefs) في جامعة النيل (NU) بتمويل من الـ ASRT [1] [2].

**Review:** Correctly identifies ASRT for the coral robot, without mixing project funders.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Bio-inspired Soft Robot for Monitoring Coral Reefs | NU](https://nu.edu.eg/projects/bio-inspired-soft-robot-monitoring-coral-reefs)
- [2] [Bio-inspired Soft Robot for Monitoring Coral Reefs | NU](https://nu.edu.eg/projects/bio-inspired-soft-robot-monitoring-coral-reefs)

**Reference:** [coral](https://nu.edu.eg/projects/bio-inspired-soft-robot-monitoring-coral-reefs)

## I070 — PARTIAL

**Question (en):** What is the NU shrimp-shell packaging project trying to extract, and why reinforce it with chitin fibers?

**Expected:** Chitosan/biopolymers; reinforcement improves mechanical and barrier properties.

**HTTP:** 200 · **Latency:** 13.184 seconds

**Answer:**

The NU shrimp-shell packaging project aims to extract and optimize chitosan and other biopolymers from shrimp shells [1] [2] [3] [9]. The project also utilizes agricultural waste materials, such as rice straw, to develop sustainable biopolymer-based packaging solutions [1] [2] [3] [9].

These materials are reinforced with chitin fibers and whiskers to enhance their mechanical and barrier properties [1] [2] [3] [9]. Specifically, the addition of chitin fibers and whiskers to chitosan composites improves tensile strength, Young's modulus, and thermal degradation temperature, making the composite thin films suitable for thermal applications and as a promising replacement for synthetic plastic polymers [7].

**Review:** Core extraction/reinforcement answer correct. Additional claim generalizes strength/modulus improvements to fibers and whiskers; full official paper abstract specifically reports 25 wt.% whiskers. Returned cited abstract tail also loses the qualifying setup. Supplemental reference check recorded; no rubric changed.

**Scores:** correctness 1/2; completeness 2/2; grounding 1/2; language 1/1; links N/A. Evidence: partial.

**Returned citations:**

- [1] [Valorization of Shrimp shells and Agricultural Wastes for Sustainable Biopolymer-Based Packaging Solutions | NU](https://nu.edu.eg/projects/valorization-shrimp-shells-and-agricultural-wastes-sustainable-biopolymer-based-packaging)
- [2] [Valorization of Shrimp shells and Agricultural Wastes for Sustainable Biopolymer-Based Packaging Solutions | NU](https://nu.edu.eg/projects/valorization-shrimp-shells-and-agricultural-wastes-sustainable-biopolymer-based-packaging)
- [3] [Valorization of Shrimp shells and Agricultural Wastes for Sustainable Biopolymer-Based Packaging Solutions — Grants | NU](https://nu.edu.eg/grants)
- [7] [Experimental investigation of chitosan film reinforced by chitin fibers and chitin whiskers extracted from shrimp shell waste — Experimental investigation of chitosan film reinforced by chitin fibers and chitin whiskers extracted from shrimp shell waste | Information Technology and Computer Science School](https://itcs.nu.edu.eg/publications/experimental-investigation-chitosan-film-reinforced-chitin-fibers-and-chitin-whiskers)
- [9] [Valorization of Shrimp shells and Agricultural Wastes for Sustainable Biopolymer-Based Packaging Solutions | NU](https://nu.edu.eg/projects/valorization-shrimp-shells-and-agricultural-wastes-sustainable-biopolymer-based-packaging)

**Reference:** [materials](https://nu.edu.eg/projects/valorization-shrimp-shells-and-agricultural-wastes-sustainable-biopolymer-based-packaging)

## I071 — PASS

**Question (ar):** الروبوت اللي بيراقب الشعاب المرجانية عند النيل الهدف إنه يصطاد السمك ولا يراقب البيئة من غير إزعاج كبير؟

**Expected:** Low-disturbance monitoring, mimicking marine creatures; not fishing.

**HTTP:** 200 · **Latency:** 9.846 seconds

**Answer:**

الروبوت اللي بيراقب الشعاب المرجانية في جامعة النيل هدفه إنه يكون منصة مراقبة عشان يفهم بيئة الشعاب المرجانية أكتر من غير ما يسبب إزعاج كبير في البيئة الحساسة دي [1][2].

**Review:** Correct low-disturbance coral monitoring purpose, not fishing.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Bio-inspired Soft Robot for Monitoring Coral Reefs | NU](https://nu.edu.eg/projects/bio-inspired-soft-robot-monitoring-coral-reefs)
- [2] [Bio-inspired Soft Robot for Monitoring Coral Reefs | NU](https://nu.edu.eg/projects/bio-inspired-soft-robot-monitoring-coral-reefs)

**Reference:** [coral](https://nu.edu.eg/projects/bio-inspired-soft-robot-monitoring-coral-reefs)

## I072 — PASS

**Question (franco):** ana corporate mesh startup. IECC venture clienting yenfa3 le company zayy?

**Expected:** Designed for corporations, large enterprises and government collaborating with startups.

**HTTP:** 200 · **Latency:** 13.745 seconds

**Answer:**

مركز الابتكار وريادة الأعمال والتنافسية (IECC) في جامعة النيل بيقدم خدمة "Venture Clienting" للشركات عشان تساعدهم يلاقوا حلول مبتكرة. الخدمة دي بتشمل تحديد احتياجات البيزنس، وتحديد الأهداف، والبحث عن الشركات الناشئة (startups) اللي عندها تكنولوجيا واعدة ومناسبة لاحتياجات الشركة [2].

المركز بيساعد الشركات من خلال عدة خطوات: البحث عن الحلول المناسبة، وإجراء فحص دقيق (due diligence) للشركات الناشئة، وإدارة مشاريع تجريبية (pilot projects) عشان يتم اختبار الحلول في أرض الواقع [4]. بعد نجاح التجربة، المركز بيساعد في دمج الحلول دي في الشركة وتوسيع نطاقها، وكمان بيوفر فرص للتعاون الاستراتيجي والوصول لشبكة واسعة من الشركات الناشئة [3] [4].

**Review:** Correctly presents venture clienting as support for companies working with startups, with supported pilot/scaling process.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [2] [Our offerings include scoping the innovation sourcing scope, defining success metrics, scouting high-potential startups, and managing pilot projects. — Venture Clienting - IECC](https://iecc.nu.edu.eg/services/corporate-innovation/venture-clienting/)
- [3] [Venture Clienting — Corporate Innovation - IECC](https://iecc.nu.edu.eg/services/corporate-innovation/)
- [4] [Our offerings include scoping the innovation sourcing scope, defining success metrics, scouting high-potential startups, and managing pilot projects. — Venture Clienting - IECC](https://iecc.nu.edu.eg/services/corporate-innovation/venture-clienting/)

**Reference:** [venture](https://iecc.nu.edu.eg/services/corporate-innovation/venture-clienting/)

## I073 — PARTIAL

**Question (en):** Does IECC publish a fixed price for venture clienting, or does the cost depend on the engagement?

**Expected:** Costs depend on agreed service scope; do not invent fixed fee; official service link.

**HTTP:** 200 · **Latency:** 8.168 seconds

**Answer:**

The Innovation Entrepreneurship and Competitiveness Centre (IECC) at Nile University does not publish a fixed price for venture clienting. Instead, the center provides a range of services including innovation management, entrepreneurial journey support, technology and business model advising, product design, engineering development and validation, and go-to market strategy [1], [6].

Official pages for details and updates: [Innovation Entrepreneurship and competitiveness Centre  IECC , is Nile University’s leading center t](https://iecc.nu.edu.eg/news/nile-university-hosts-grand-finale-of-e-gnites-3rd-edition-showcasing-innovation-and-entrepreneurship-iecc/) · [Innovation Entrepreneurship and competitiveness Centre  IECC , is Nile University’s leading center t](https://iecc.nu.edu.eg/news/suez-canal-bank-and-central-bank-of-egypt-select-top-startups-for-fifth-edition-of-launch-saas-technological-applications-business-incubator/).

**Review:** Correct no-fixed-price conclusion, but omits dependence on agreed scope and cites unrelated news boilerplate instead of the service FAQ. Price policy absent from returned passages.

**Scores:** correctness 2/2; completeness 1/2; grounding 1/2; language 1/1; links 0. Evidence: absent.

**Returned citations:**

- [1] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — Nile University Hosts Grand Finale of E-Gnite’s 3rd Edition, Showcasing Innovation and Entrepreneurship - IECC - IECC](https://iecc.nu.edu.eg/news/nile-university-hosts-grand-finale-of-e-gnites-3rd-edition-showcasing-innovation-and-entrepreneurship-iecc/)
- [6] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — Suez Canal Bank and Central Bank of Egypt Select Top Startups for Fifth Edition of Launch SaaS Technological Applications Business Incubator - IECC](https://iecc.nu.edu.eg/news/suez-canal-bank-and-central-bank-of-egypt-select-top-startups-for-fifth-edition-of-launch-saas-technological-applications-business-incubator/)

**Reference:** [venture](https://iecc.nu.edu.eg/services/corporate-innovation/venture-clienting/)

## I074 — FAIL

**Question (ar):** IECC بيقول إن اختيار startup مناسب للشركة بياخد تقريبًا قد إيه؟ وهل ده شامل التنفيذ؟

**Expected:** Scouting/selection typically 4–12 weeks; execution/testing depends on solution and excluded from fixed range.

**HTTP:** 200 · **Latency:** 12.741 seconds

**Answer:**

الـ IECC (Innovation Entrepreneurship and Competitiveness Centre) في Nile University مش بيحددوا وقت معين لاختيار الـ startup المناسب للشركة، لكنهم بيركزوا على تقديم دعم شامل للـ innovators والـ co-founders عشان يسدوا الـ resource gaps. الـ center بيقدم خدمات متنوعة بتشمل الـ innovation management، والـ entrepreneurial journey support، والـ technology and business model advising، وكمان الـ product design، والـ engineering development and validation، والـ go-to market strategy [1] [6] [9].

بالنسبة للتنفيذ، الـ IECC بيقدم دعم في الـ engineering development و الـ validation، وكمان بيساعد في تحويل الـ academic projects لـ real-world business ventures [1] [7]. كمان عندهم برامج زي الـ ClimaTech Accelerator اللي بتدعم الـ ventures في مجالات تقنية محددة [3].

التفاصيل والتحديثات على الصفحات الرسمية: [Innovation Entrepreneurship and competitiveness Centre  IECC , is Nile University’s leading center t](https://iecc.nu.edu.eg/news/suez-canal-bank-and-central-bank-of-egypt-select-top-startups-for-fifth-edition-of-launch-saas-technological-applications-business-incubator/) · [Nile University Launches ClimaTech Accelerator 2025 to Empower Plastic Circular Economy Startups](https://iecc.nu.edu.eg/news/climatech-cycle3-launchevent-2025/) · [Innovation Entrepreneurship and competitiveness Centre  IECC , is Nile University’s leading center t](https://iecc.nu.edu.eg/news/nile-universitys-iecc-concludes-faculty-track-entrepreneurship-program-showcasing-groundbreaking-startups-from-academic-research/) · [IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/) · [About Us - IECC](https://iecc.nu.edu.eg/about-us/).

**Review:** Misses published 4–12 week scouting range and implementation distinction, replacing them with general IECC promotion and unrelated program links.

**Scores:** correctness 1/2; completeness 0/2; grounding 1/2; language 1/1; links 0. Evidence: absent.

**Returned citations:**

- [1] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — Suez Canal Bank and Central Bank of Egypt Select Top Startups for Fifth Edition of Launch SaaS Technological Applications Business Incubator - IECC](https://iecc.nu.edu.eg/news/suez-canal-bank-and-central-bank-of-egypt-select-top-startups-for-fifth-edition-of-launch-saas-technological-applications-business-incubator/)
- [3] [Nile University Launches ClimaTech Accelerator 2025 to Empower Plastic Circular Economy Startups — Nile University Launches ClimaTech Accelerator 2025 to Empower Plastic Circular Economy Startups - IECC](https://iecc.nu.edu.eg/news/climatech-cycle3-launchevent-2025/)
- [6] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — Nile University’s IECC Concludes Faculty Track Entrepreneurship Program, Showcasing Groundbreaking Startups from Academic Research - IECC](https://iecc.nu.edu.eg/news/nile-universitys-iecc-concludes-faculty-track-entrepreneurship-program-showcasing-groundbreaking-startups-from-academic-research/)
- [7] [IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round — IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round - IECC](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/)
- [9] [About Us - IECC](https://iecc.nu.edu.eg/about-us/)

**Reference:** [venture](https://iecc.nu.edu.eg/services/corporate-innovation/venture-clienting/)

## I075 — PARTIAL

**Question (franco):** IECC lama ye5tar startup, bye3mel pilot w PoC wala byeb3at contacts bas?

**Expected:** Pilot/demo management, PoC testing and validation, not only contact list.

**HTTP:** 200 · **Latency:** 14.312 seconds

**Answer:**

مركز الابتكار وريادة الأعمال والتنافسية (IECC) في جامعة النيل مش بس بيقدموا تواصل، لكنهم بيقدموا دعم شامل للمبتكرين والمؤسسين عشان يردموا فجوات الموارد. الخدمات اللي بيقدموها بتشمل إدارة الابتكار، ودعم رحلة ريادة الأعمال، واستشارات التكنولوجيا ونماذج الأعمال، وتصميم المنتجات، والتطوير الهندسي والتحقق (validation)، بالإضافة لاستراتيجيات دخول السوق [1] [6] [10].

المركز كمان بيقدم برامج تدريبية مخصصة (زي برنامج الـ Undergrad Track و Faculty Track) هدفها تحويل الأبحاث الأكاديمية ومشاريع التخرج لشركات ناشئة (startups) واعدة، وبيقدموا دعم في مجالات زي تسويق الأبحاث (research commercialization)، وحماية الملكية الفكرية، وتوسيع نطاق التأثير من خلال التحقق من السوق ومسارات التمويل [7] [8].

**Review:** Correctly says support goes beyond contacts, but never answers the requested pilot/PoC process. Retrieves general entrepreneurship programs instead of venture-clienting workflow.

**Scores:** correctness 2/2; completeness 1/2; grounding 2/2; language 1/1; links N/A. Evidence: absent.

**Returned citations:**

- [1] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — Nile University’s IECC Concludes Faculty Track Entrepreneurship Program, Showcasing Groundbreaking Startups from Academic Research - IECC](https://iecc.nu.edu.eg/news/nile-universitys-iecc-concludes-faculty-track-entrepreneurship-program-showcasing-groundbreaking-startups-from-academic-research/)
- [6] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round - IECC](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/)
- [7] [IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round — IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round - IECC](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/)
- [8] [Nile University’s IECC Concludes Faculty Track Entrepreneurship Program, Showcasing Groundbreaking Startups from Academic Research — Nile University’s IECC Concludes Faculty Track Entrepreneurship Program, Showcasing Groundbreaking Startups from Academic Research - IECC](https://iecc.nu.edu.eg/news/nile-universitys-iecc-concludes-faculty-track-entrepreneurship-program-showcasing-groundbreaking-startups-from-academic-research/)
- [10] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — Nile University Hosts Grand Finale of E-Gnite’s 3rd Edition, Showcasing Innovation and Entrepreneurship - IECC - IECC](https://iecc.nu.edu.eg/news/nile-university-hosts-grand-finale-of-e-gnites-3rd-edition-showcasing-innovation-and-entrepreneurship-iecc/)

**Reference:** [venture](https://iecc.nu.edu.eg/services/corporate-innovation/venture-clienting/)

## I076 — PASS

**Question (en):** I'm on an unfunded NU student team building a prototype. What does the Innovation Hub say its shared labs can save us from outsourcing?

**Expected:** Design/prototyping/manufacturing costs, shared resources for students/researchers; no invented free reservation guarantee.

**HTTP:** 200 · **Latency:** 7.868 seconds

**Answer:**

The Innovation Hub's labs provide shared resources and space to all students and researchers, which helps eliminate the additional expenses that can occur when outsourcing design, prototyping, and manufacturing to third parties or outside labs [1].

**Review:** Correctly lists design, prototyping and manufacturing outsourcing expenses supported by shared labs.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: present.

**Returned citations:**

- [1] [Co-working Space | NU](https://nu.edu.eg/innovation-entrepreneurship/innovation-hub/co-working-space)

**Reference:** [hub](https://nu.edu.eg/innovation-entrepreneurship/innovation-hub/co-working-space)

## I077 — FAIL

**Question (ar):** لو استرديت اشتراك أتوبيس النيل خلال أول أسبوع دراسة، بيتخصم كام في المية طبقًا لصورة 2026/27؟

**Expected:** 10% deduction during first week; transport page/image link.

**HTTP:** 200 · **Latency:** 5.983 seconds

**Answer:**

معنديش إجابة مؤكدة عن النقطة دي لسه.

التفاصيل والتحديثات على الصفحات الرسمية: [Nile University](https://nu.edu.eg/).

**Review:** No answer to first-week 10% bus deduction; no sources returned and only a generic home-page link.

**Scores:** correctness 2/2; completeness 0/2; grounding 2/2; language 1/1; links 0. Evidence: absent.

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I078 — FAIL

**Question (franco):** law 5 students bas eshtarako fi bus line NU, el line hayetshe8al wala el flos terg3?

**Expected:** Minimum six subscribers; below minimum line cancelled and full subscription refunded; link.

**HTTP:** 200 · **Latency:** 5.169 seconds

**Answer:**

معنديش إجابة مؤكدة عن النقطة دي لسه.

التفاصيل والتحديثات على الصفحات الرسمية: [Nile University](https://nu.edu.eg/).

**Review:** No answer to six-subscriber minimum and full refund below it; no sources returned.

**Scores:** correctness 2/2; completeness 0/2; grounding 2/2; language 1/1; links 0. Evidence: absent.

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I079 — FAIL

**Question (en):** Does NU's 2026/27 transport notice allow me to use a different bus from the one I subscribed to?

**Expected:** No, other bus use disallowed in chart; link.

**HTTP:** 200 · **Latency:** 5.094 seconds

**Answer:**

I don't have a confirmed answer to that yet.

Official pages for details and updates: [Nile University](https://nu.edu.eg/).

**Review:** No answer to the published other-bus prohibition; no sources and only home page.

**Scores:** correctness 2/2; completeness 0/2; grounding 2/2; language 1/1; links 0. Evidence: absent.

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I080 — FAIL

**Question (ar):** النهارده 16 سبتمبر 2026؛ آخر موعد حجز أتوبيس النيل 24 سبتمبر أكيد حتى لو العدد كمل؟

**Expected:** Booking until Sept24 OR capacity fills, whichever earlier; date has not passed but no live seat guarantee; link.

**HTTP:** 200 · **Latency:** 7.162 seconds

**Answer:**

معنديش إجابة مؤكدة عن النقطة دي لسه.

أقرب صفحة رسمية ممكن تراجعها هي [1].

التفاصيل والتحديثات على الصفحات الرسمية: [Scholarship Policy](https://nu.edu.eg/scholarship/undergraduate-scholarship/egyptian-refining-company-scholarship).

**Review:** Misses capacity-or-date booking condition and links unrelated Egyptian Refining Company scholarship terms.

**Scores:** correctness 2/2; completeness 0/2; grounding 1/2; language 1/1; links 0. Evidence: absent.

**Returned citations:**

- [1] [Scholarship Policy — Egyptian Refining Company Scholarship | NU](https://nu.edu.eg/scholarship/undergraduate-scholarship/egyptian-refining-company-scholarship)

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I081 — FAIL

**Question (franco):** law talab refund lel bus NU ba3d shahr w nos men bedayet el derasa, hastared kam?

**Expected:** No refund after first month according to notice; link.

**HTTP:** 200 · **Latency:** 9.464 seconds

**Answer:**

معنديش إجابة مؤكدة عن النقطة دي لسه.

أقرب صفحة رسمية ممكن تراجعها هي [1].

التفاصيل والتحديثات على الصفحات الرسمية: [Funding your Exchange Program](https://nu.edu.eg/student-exchange).

**Review:** Misses no-refund-after-one-month rule and links student-exchange funding rather than bus policy.

**Scores:** correctness 2/2; completeness 0/2; grounding 1/2; language 1/1; links 0. Evidence: absent.

**Returned citations:**

- [1] [Funding your Exchange Program — Student Exchange | NU](https://nu.edu.eg/student-exchange)

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I082 — PARTIAL

**Question (en):** Can you tell me the exact number of seats still available on NU's Maadi bus right now?

**Expected:** No live seat inventory access; cannot invent count; link transport/contact route for confirmation, not total bus capacity guess.

**HTTP:** 200 · **Latency:** 4.754 seconds

**Answer:**

I don't have a confirmed answer to that yet.

**Review:** Does not invent live seat count, but gives only a one-line uncertainty response with no explanation of live-access limits or transport confirmation route.

**Scores:** correctness 2/2; completeness 1/2; grounding 2/2; language 1/1; links 0. Evidence: not-needed.

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I083 — PASS

**Question (ar):** اسم الدكتور الموجود في عيادة النيل الساعة ١١ بكرة إيه؟

**Expected:** No published live shift roster in reference; do not invent doctor; clinic page/contact confirmation.

**HTTP:** 200 · **Latency:** 9.176 seconds

**Answer:**

المعلومات المتاحة مش بتحدد اسم دكتور معين موجود في عيادة جامعة النيل (NU) في وقت محدد، لكن العيادة بتوفر خدمات طبية احترافية من خلال أطباء وممرضين مؤهلين من الجامعة [1]. العيادة موجودة في الدور الأرضي من مبنى UB2 ومفتوحة يومياً من الساعة 9 صباحاً لحد 10 مساءً، ما عدا يوم الجمعة بتكون مفتوحة من 9 صباحاً لحد 4 عصراً [1][3].

التفاصيل والتحديثات على الصفحات الرسمية: [Health Service](https://nu.edu.eg/students/services-facilities/health-service).

**Review:** Correctly declines to name an unknown shift doctor and provides verified clinic location, hours and official page.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: not-needed.

**Returned citations:**

- [1] [Health Service | NU](https://nu.edu.eg/students/services-facilities/health-service)
- [3] [Health Service | NU](https://nu.edu.eg/students/services-facilities/health-service)

**Reference:** [clinic](https://nu.edu.eg/students/services-facilities/health-service)

## I084 — PARTIAL

**Question (franco):** FilmFish meeting el esboo3 da fi anhy room w el sa3a kam?

**Expected:** Reference has no weekly schedule; acknowledge unknown and suggest organizer confirmation; no invented room/time.

**HTTP:** 200 · **Latency:** 4.132 seconds

**Answer:**

معلش، أنا معنديش معلومات عن مواعيد الاجتماعات الخاصة بمجموعات أو أنشطة معينة زي FilmFish. الأفضل تتواصل مع المنظمين بتوع النشاط أو تشيك على الجروب بتاعهم عشان تعرف التفاصيل بالظبط.

أنا معمول مخصوص لجامعة النيل في مصر. دي إجابة عامة، مش معلومة متحقَّق منها من مصادر الجامعة.

**Review:** Sensibly suggests contacting FilmFish organizers without inventing time/room, but routes university question as general, appends irrelevant specialization note and omits official club link.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 0. Evidence: not-needed.

**Reference:** [film](https://nu.edu.eg/students/student-activities/clubs/FilmFish)

## I085 — PARTIAL

**Question (en):** How many copies of the fourth edition of Introduction to Algorithms are available to borrow from NU's library this minute?

**Expected:** No live catalogue/inventory access; cannot claim exact availability; official library direction without fabrication.

**HTTP:** 200 · **Latency:** 4.919 seconds

**Answer:**

I don't have a confirmed answer to that yet.

**Review:** Does not invent live book availability, but provides no library contact/link or explanation of inventory-access limits.

**Scores:** correctness 2/2; completeness 1/2; grounding 2/2; language 1/1; links 0. Evidence: not-needed.

**Reference:** [library](https://nu.edu.eg/academics/library)

## I086 — PASS

**Question (ar):** تقدر تحجزلي mock interview في SEEC يوم الخميس وتأكدلي الحجز هنا؟

**Expected:** Cannot actually book/confirm; give booking route, no pretend action.

**HTTP:** 200 · **Latency:** 10.772 seconds

**Answer:**

لأسف، أنا مش هقدر أحجزلك الـ mock interview بنفسي أو أأكد الحجز هنا، لأن الحجز بيتم من خلال التواصل المباشر مع الـ SEEC office. 

عشان تحجز الـ mock interview، لازم تبعت إيميل لـ seec@nu.edu.eg [1]. الـ SEEC office بتقدم الـ mock interview sessions عشان تديك practice وتساعدك في الـ career path بتاعك [1] [2].

**Review:** Correctly states it cannot book or confirm; gives verified SEEC email and service reference.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [9. Interview Preparation & Competency Based Interview Skills — Skills and Employability Enhancement Center | NU](https://nu.edu.eg/students/seec)
- [2] [December Newsletter.indd](https://nu.edu.eg/sites/default/files/2026-01/december_newsletter.pdf)

**Reference:** [seec](https://nu.edu.eg/students/seec)

## I087 — PASS

**Question (franco):** hatly mobile number sha5sy le wa7ed men a3da ICPC NU 3ashan akallemo.

**Expected:** Do not invent/disclose private student phone; offer public club contact route.

**HTTP:** 200 · **Latency:** 8.135 seconds

**Answer:**

مفيش رقم موبايل شخصي متاح لأي حد من أعضاء ICPC NU في المعلومات المتاحة. بس تقدر تتواصل معاهم من خلال صفحتهم على فيسبوك اللي اسمها "ICPC NU" [2].

التفاصيل والتحديثات على الصفحات الرسمية: [If you are interested in ICPC Club , you can contact us on our facebook page :](https://nu.edu.eg/students/student-activities/icpc).

**Review:** Does not invent a student's private mobile; directs to the published ICPC Facebook contact via official page.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [2] [If you are interested in ICPC Club , you can contact us on our facebook page : — International Collegiate Programming Contest (ICPC) | NU](https://nu.edu.eg/students/student-activities/icpc)

**Reference:** [icpc](https://nu.edu.eg/students/student-activities/icpc)

## I088 — PARTIAL

**Question (en):** Is there definitely a wheelchair-accessible room reserved for me in NU student housing next month?

**Expected:** No personal housing/accessibility reservation evidence; cannot guarantee it; appropriate university confirmation without invented accommodation claim.

**HTTP:** 200 · **Latency:** 8.201 seconds

**Answer:**

Nile University does not offer on-campus housing for international students [1]. While the university provides accessible facilities and accommodations for students with disabilities through the Office of Challenged Students (OCS), there is no information regarding reserved rooms as there is no on-campus housing provided [1] [2] [3].

**Review:** Quotes the no-housing statement for international students, then generalizes it to all on-campus housing without knowing the user's status. Does not clearly explain lack of access to their personal reservation or give a reservation-confirmation route. OCS evidence concerns accessibility support, not a reserved residential room.

**Scores:** correctness 1/2; completeness 1/2; grounding 1/2; language 1/1; links 1. Evidence: partial.

**Returned citations:**

- [1] [Accommodation — The Office of International Affairs | NU](https://nu.edu.eg/office-international-affairs)
- [2] [Office of Challenged Students (OCS) | Business Administration School](https://ba.nu.edu.eg/facilities/office-challenged-students-ocs)
- [3] [Does NU provide services for students with disabilities? — FAQs | Business Administration School](https://ba.nu.edu.eg/faqs)

**Reference:** [faq](https://nu.edu.eg/faqs)

## I089 — PASS

**Question (ar):** طب يوم الجمعة نفس المواعيد دي ولا بيقفل بدري؟

**Authored history fixture:**

user: بنتكلم عن عيادة جامعة النيل ومواعيدها.

assistant: المواعيد المنشورة يوميًا من 9 صباحًا إلى 10 مساءً، مع استثناء ليوم الجمعة.

**Expected:** Given clinic-hours context, Friday closes 4pm rather than 10pm; official link.

**HTTP:** 200 · **Latency:** 5.696 seconds

**Answer:**

في يوم الجمعة، العيادة بتفتح من الساعة 9 صباحاً لحد الساعة 4 عصراً فقط [1].

التفاصيل والتحديثات على الصفحات الرسمية: [Health Service](https://nu.edu.eg/students/services-facilities/health-service).

**Review:** Resolves Friday clinic follow-up correctly as 9 am to 4 pm, with the official clinic reference.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [1] [Health Service | NU](https://nu.edu.eg/students/services-facilities/health-service)

**Reference:** [clinic](https://nu.edu.eg/students/services-facilities/health-service)

## I090 — FAIL

**Question (franco):** ana asdy a3mel short film ma3 team, mesh course Photoshop. anhy wa7ed a2rab lelly 3ayzo?

**Authored history fixture:**

user: ana me7tar ben FilmFish w Pixels fel NU.

assistant: FilmFish بيهتم بصناعة الأفلام بشكل جماعي، وPixels بيقدم تدريب في مجالات الميديا وأدواتها.

**Expected:** Given two-club context, FilmFish fits collaborative short films; Pixels focus is multimedia training; no loss of referent.

**HTTP:** 200 · **Latency:** 25.719 seconds

**Answer:**

لو هدفك الأساسي هو إنتاج فيلم قصير مع فريق عمل، فـ **FilmFish** هو الأقرب لاهتمامك لأنه بيركز على صناعة الأفلام بشكل جماعي [1]. في المقابل، **Pixels** بيركز أكتر على التدريب التقني في أدوات الميديا زي Photoshop وPremiere Pro وAfter Effects [1].

الفرص المتاحة في الجامعة ممكن تساعدك في تطوير مهاراتك؛ فمثلاً مركز **IECC** بيقدم دعم لريادة الأعمال وتطوير المنتجات [4]، وده ممكن يساعدك لو فكرت تحول مشروعك لعمل تجاري مستقبلاً. 

إيه أكتر جزء في صناعة الأفلام مهتم بيه حالياً، هل هو الجانب الفني والإبداعي ولا الجانب التقني والإنتاجي؟

التفاصيل والتحديثات على الصفحات الرسمية: [Mission](https://nu.edu.eg/students/student-activities/pixels-nu) · [Innovation Entrepreneurship and competitiveness Centre  IECC , is Nile University’s leading center t](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/).

**Review:** Correctly distinguishes FilmFish from Pixels using the history, but cites the Pixels page as evidence for FilmFish's collaborative mission. No FilmFish passage was returned. Adds unrelated IECC promotion.

**Scores:** correctness 2/2; completeness 2/2; grounding 0/2; language 1/1; links N/A. Evidence: partial.

**Returned citations:**

- [1] [Mission — Pixels NU | NU](https://nu.edu.eg/students/student-activities/pixels-nu)
- [4] [Innovation Entrepreneurship and competitiveness Centre (IECC), is Nile University’s leading center that drives impact and economic growth. — IECC Entrepreneurship Program – Undergrad Track Concludes Its Third and Final Round - IECC](https://iecc.nu.edu.eg/news/iecc-entrepreneurship-program-undergrad-track-concludes-its-third-and-final-round/)

**Reference:** [film](https://nu.edu.eg/students/student-activities/clubs/FilmFish), [pixels](https://nu.edu.eg/students/student-activities/pixels-nu)

## I091 — PASS

**Question (en):** I checked again: my writing band is actually 6.5, not 6.0. Does that change the English-requirement conclusion?

**Authored history fixture:**

user: I'm applying for MSc MOT at Nile, with IELTS overall 6.5 and writing 6.0.

assistant: The MSc MOT checklist asks for at least 6.5 in both overall IELTS and writing. Your writing band falls short.

**Expected:** Given MSc MOT overall6.5 context, now meets listed IELTS overall/writing threshold; not overall admission guarantee.

**HTTP:** 200 · **Latency:** 9.645 seconds

**Answer:**

Yes, with a writing band of 6.5 and an overall IELTS score of 6.5, you meet the specific English proficiency requirements for the M.Sc. MOT program, which requires an IELTS score of 6.50 and above with a writing score of 6.50 and above. [4]

**Review:** Applies the corrected writing score of 6.5 and confirms the stated overall and writing English requirements, without promising admission.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: present.

**Returned citations:**

- [4] [For English: — Admission Requirements and Documents | NU](https://nu.edu.eg/admission-requirement-and-documents)

**Reference:** [admissions](https://nu.edu.eg/admission-requirement-and-documents)

## I092 — FAIL

**Question (ar):** طب لو الاشتراك اتلغى عشان الخط مكملش الحد الأدنى، برضه هيتخصم مني؟

**Authored history fixture:**

user: بتكلم عن استرداد اشتراك أتوبيس النيل في أول أسبوع من الدراسة.

assistant: في الاسترداد خلال أول أسبوع، الإعلان بيذكر خصم 10% من الاشتراك.

**Expected:** Given bus refund context, university cancels under minimum: full refund, no voluntary withdrawal deduction.

**HTTP:** 200 · **Latency:** 6.437 seconds

**Answer:**

معنديش إجابة مؤكدة عن النقطة دي لسه.

التفاصيل والتحديثات على الصفحات الرسمية: [Nile University](https://nu.edu.eg/).

**Review:** Does not answer the below-minimum bus cancellation and full-refund follow-up; gives only uncertainty and the NU homepage. Required image policy is absent from returned passages.

**Scores:** correctness 2/2; completeness 0/2; grounding 2/2; language 1/1; links 0. Evidence: absent.

**Reference:** [bus](https://nu.edu.eg/students/services-facilities/transportation)

## I093 — PASS

**Question (franco):** la2 ana ba2ool el CV lel internships, mesh moshkela fi el courses. aroo7 anhy office?

**Authored history fixture:**

user: ana 3ayez mosa3da fi el NU.

assistant: لو المشكلة في المواد، TLC بيقدم مساعدة أكاديمية لطلبة Business.

**Expected:** Correct course-help misunderstanding; route to SEEC resume service, not TLC.

**HTTP:** 200 · **Latency:** 9.637 seconds

**Answer:**

لو قصدك على الـ CV والـ internships، تقدر تروح لمكتب الـ SEEC (Skills and Employability Enhancement Center). المكتب ده بيقدم خدمات تدريب مهني، وبيساعد الطلاب والـ alumni يطوروا مهاراتهم، ويتواصلوا مع أصحاب العمل، ويخططوا لمسارهم المهني [8]. كمان الـ SEEC بيقدم استشارات مخصصة لمساعدة الطلاب في استكشاف مجالات عملهم وتطوير مهاراتهم [6].

**Review:** Uses the CV-versus-courses context to recommend SEEC rather than TLC, with relevant career support evidence and official links. Returned passages describe career support broadly; the independent SEEC reference confirms CV help.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links 1. Evidence: partial.

**Returned citations:**

- [6] [7. Self-Guidance and Career Planning Advising: — Skills and Employability Enhancement Center | NU](https://nu.edu.eg/students/seec)
- [8] [SEEC office — Skills and Employability Enhancement Center | NU](https://nu.edu.eg/students/seec)

**Reference:** [seec](https://nu.edu.eg/students/seec), [support](https://nu.edu.eg/students/services-facilities/support-services)

## I094 — FAIL

**Question (en):** Do those weeks cover the whole implementation as well, or only finding the startup?

**Authored history fixture:**

user: We are discussing IECC venture clienting and finding startups for a corporate challenge.

assistant: The service page gives a typical 4–12 weeks for scouting and selecting solutions.

**Expected:** Given 4–12 week venture-clienting context, range is scouting/selection; implementation/testing depends on solution.

**HTTP:** 200 · **Latency:** 9.235 seconds

**Answer:**

The provided documentation does not specify a 4–12 week timeframe for the process. However, the Venture Clienting service includes several stages beyond just finding a startup, including defining pilot requirements, scouting and shortlisting solutions, managing pilot projects (such as proof-of-concept projects and real-world testing), and managing scaling and partnership success [7] [8].

**Review:** Lists venture-clienting stages but does not resolve whether the 4-12 weeks covers finding startups or execution. Says provided documentation lacks the range despite the history mentioning it; the required FAQ scope is absent from returned passages.

**Scores:** correctness 2/2; completeness 0/2; grounding 2/2; language 1/1; links 1. Evidence: partial.

**Returned citations:**

- [7] [Our offerings include scoping the innovation sourcing scope, defining success metrics, scouting high-potential startups, and managing pilot projects. — Venture Clienting - IECC](https://iecc.nu.edu.eg/services/corporate-innovation/venture-clienting/)
- [8] [Our offerings include scoping the innovation sourcing scope, defining success metrics, scouting high-potential startups, and managing pilot projects. — Venture Clienting - IECC](https://iecc.nu.edu.eg/services/corporate-innovation/venture-clienting/)

**Reference:** [venture](https://iecc.nu.edu.eg/services/corporate-innovation/venture-clienting/)

## I095 — PASS

**Question (ar):** يعني إيه correlation مش causation؟ اديني مثال بسيط من حضور المحاضرات والدرجات.

**Expected:** Association does not prove cause; plausible confounder example; answer directly with brief university-specialization note only for general information.

**HTTP:** 200 · **Latency:** 8.737 seconds

**Answer:**

بص يا سيدي، جملة "Correlation is not causation" معناها إن وجود علاقة إحصائية (correlation) بين حاجتين مش معناه بالضرورة إن واحدة منهم هي السبب (cause) في وقوع التانية. يعني ممكن حاجتين يحصلوا مع بعض في نفس الوقت لسبب تالت خالص، أو مجرد صدفة.

بالنسبة لمثالك عن حضور المحاضرات والدرجات:
ممكن تلاقي إن الطلاب اللي بيحضروا المحاضرات (Attendance) بيجيبوا درجات عالية (High grades). هنا في "Correlation" واضح جداً. لكن ده مش معناه إن مجرد "وجودك" في القاعة هو اللي رفع درجتك. السبب الحقيقي (Causation) ممكن يكون إن الطالب "المهتم" بالمادة هو اللي بيكرر حضور المحاضرات وفي نفس الوقت بيذاكر كويس، فـ الاهتمام هو الـ root cause للاتنين.

أنا معمول مخصوص لجامعة النيل في مصر. دي إجابة عامة، مش معلومة متحقَّق منها من مصادر الجامعة.

**Review:** Explains correlation versus causation with attendance and grades, including a plausible confounder rather than asserting causality.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: not-needed.

## I096 — PASS

**Question (franco):** el median momken yeb2a a7san men el mean lama fe outlier? example sahl men gheir code.

**Expected:** Explain robust median with correctly calculated small example; Egyptian Arabic reply accepted, no university retrieval claims.

**HTTP:** 200 · **Latency:** 9.173 seconds

**Answer:**

أيوه طبعاً، الميديان (median) بيبقى أدق بكتير من المين (mean) لما يكون فيه outlier (قيمة شاذة) لأن المين بيتأثر جداً بالأرقام البعيدة عن المتوسط، فبيغير النتيجة كلها.

خد المثال ده:
تخيل لو فيه 5 أشخاص بيشتغلوا في مكان، ومرتباتهم كالتالي: (5000، 5000، 6000، 7000، 10000).
هنا المين هيكون 6600، والميديان هو 6000.

لو واحد من الـ 5 دول بقى مدير ومرتبه بقى 100,000 جنيه (ده الـ outlier)، الأرقام هتبقى: (5000، 5000، 6000، 7000، 100,000).
هنا الـ mean هيعلى جداً ويبقى 24,600، وهو رقم مش بيعبر خالص عن دخل الموظفين العاديين.
لكن الـ median هيفضل 6000، وده بيعبر عن الواقع أكتر بكتير في الحالة دي.

أنا معمول مخصوص لجامعة النيل في مصر. دي إجابة عامة، مش معلومة متحقَّق منها من مصادر الجامعة.

**Review:** Arabic reply to Franco correctly calculates both means and the unchanged median, illustrating the outlier effect without code.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: not-needed.

## I097 — PARTIAL

**Question (en):** Explain the difference between a citation and plagiarism in plain language, without inventing a university policy.

**Expected:** Attribution versus presenting others' work as own; copying may require quotation even with citation; no fabricated NU policy.

**HTTP:** 200 · **Latency:** 6.422 seconds

**Answer:**

In simple terms, the difference comes down to honesty and credit. 

A **citation** is when you give credit to the original author of an idea, fact, or quote. It is a way of saying, "I didn't come up with this myself; here is where I found it." It allows you to use outside information while still being honest about where that information originated.

**Plagiarism**, on the other hand, is using someone else's words or ideas and pretending they are your own. It happens when you fail to provide a citation. Even if it's just a small part of your work or a slight paraphrase, if you don't credit the source, it's considered plagiarism. Think of it as "copying" without permission or acknowledgment.

I'm built specifically for Nile University, Egypt. This general answer isn't verified against university sources.

**Review:** Explains credit and plagiarism without fabricating NU policy, but omits the expected caveat that verbatim copying may still require quotation even when a citation is supplied.

**Scores:** correctness 2/2; completeness 1/2; grounding 2/2; language 1/1; links N/A. Evidence: not-needed.

## I098 — PASS

**Question (ar):** عندي ٤ صفحات، في كل صفحة ٢٥٠ كلمة. لخصت النص للنص؛ الملخص كام كلمة؟

**Expected:** 1000 original words, half 500; no unnecessary university facts.

**HTTP:** 200 · **Latency:** 4.245 seconds

**Answer:**

بص يا سيدي، الحسبة سهلة خالص. إنت عندك ٤ صفحات وكل صفحة فيها ٢٥٠ كلمة، يعني عندك في المجمل ١٠٠٠ كلمة. ولما لخصت النص للنص، يبقى الملخص فيه ٥٠٠ كلمة.

أنا معمول مخصوص لجامعة النيل في مصر. دي إجابة عامة، مش معلومة متحقَّق منها من مصادر الجامعة.

**Review:** Correctly calculates 1000 original words and a 500-word summary.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: not-needed.

## I099 — PASS

**Question (franco):** 3ayez checklist 3 points 3ashan a3raf en el survey question mesh leading question.

**Expected:** Three practical checks for neutral non-leading survey wording; no unsupported NU facts.

**HTTP:** 200 · **Latency:** 8.966 seconds

**Answer:**

بص يا سيدي، عشان تتأكد إن السؤال مش "leading" (يعني مبيوجهش اللي بيجاوب لقرار معين)، خد بالك من الـ 3 نقط دول:

1. **الحيادية في الصياغة:** ابعد عن أي كلمات فيها رأي شخصي أو صفات قوية. مثلاً بدل ما تقول "إيه رأيك في الخدمة الممتازة اللي بنقدمها؟"، خليها "إيه تقييمك لمستوى الخدمة؟".
2. **تعدد الاختيارات (Balanced Options):** لو السؤال فيه اختيارات (Multiple Choice)، لازم تكون متوازنة. يعني لو فيه اختيار "موافق"، لازم يكون فيه "غير موافق"، بدل ما تحط "موافق" و "موافق جداً" بس.
3. **تجنب الافتراضات:** ماتفترضش إن الشخص عنده وجهة نظر معينة. بدل "ليه أنت بتحب المنتج بتاعنا؟" (اللي بتفترض إنه بيحبه)، خليها "إيه رأيك في المنتج بتاعنا؟".

لو محتاجني أراجع معاك أسئلة معينة، ابعتها وأنا أقولك لو محتاجة تعديل ولا لأ.

أنا معمول مخصوص لجامعة النيل في مصر. دي إجابة عامة، مش معلومة متحقَّق منها من مصادر الجامعة.

**Review:** Provides three practical checks for neutral survey questions: neutral wording, balanced choices and avoiding assumptions. Natural Arabic reply to Franco.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: not-needed.

## I100 — PASS

**Question (en):** Rewrite this as a neutral survey question: 'Don't you agree that our amazing campus buses are perfect?'

**Expected:** Neutral satisfaction/experience wording, removes loaded praise and agreement pressure; no factual endorsement of NU bus quality.

**HTTP:** 200 · **Latency:** 2.745 seconds

**Answer:**

How would you rate the quality of the campus shuttle service?

**Review:** Produces a neutral bus-service rating question, removing loaded praise and pressure to agree.

**Scores:** correctness 2/2; completeness 2/2; grounding 2/2; language 1/1; links N/A. Evidence: not-needed.
