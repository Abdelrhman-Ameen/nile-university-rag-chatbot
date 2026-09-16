"""Select the applicable evidence and expose real source links for changing information."""

import re
from urllib.parse import urlsplit

from nu_chat.citations import citation_ids


def scoped_queries(queries: list[str], meaning: str) -> list[str]:
    """Don't turn a tuition follow-up into an extra application-charge question.

    A model rewrite is a search suggestion, not authorization to broaden the user's
    question. Admission steps remain distinct from the cost of submitting a form.
    """
    charges = r"\b(?:admission|application|entrance)\s+(?:fees?|costs?|charges?)\b|\b(?:fees?|costs?|charges?)\s+(?:of|for|to)\s+(?:apply|applying|application)\b"
    if any(re.search(r"\btuition\b", q, re.I) for q in queries) and not re.search(
        charges, meaning, re.I
    ):
        queries = [q for q in queries if not re.search(charges, q, re.I)]
    gpa_queries = [q for q in queries if re.search(r"\bGPA\b", q, re.I)]
    if gpa_queries and re.search(r"\bGPA\b", meaning, re.I) and not re.search(
        r"how much.{0,30}pay|tuition (?:fee|cost|amount)|annual fee|cost after", meaning, re.I
    ):
        queries = gpa_queries
    return list(dict.fromkeys(queries))


def general_tuition(query: str) -> bool:
    """Undergraduate rates without a more specific student/certificate policy."""
    tuition_topic = re.search(r"\btuition\b", query, re.I) or (
        re.search(r"\b(fees?|costs?)\b", query, re.I)
        and re.search(
            r"\b(school|undergraduate|bachelor|ITCS|EAS|computer|computing|business|biotechnology|engineering)\b",
            query,
            re.I,
        )
        and not re.search(
            r"application|admission|housing|accommodation|transport|exam|test|dorm", query, re.I
        )
    )
    return bool(tuition_topic) and not re.search(
        r"\b(gpa|continuing|historical|international|foreign|non.egyptian|postgraduate|"
        r"graduate|master|emba|credit|igcse|ib|american|thanaw|abitur|stem)\b",
        query,
        re.I,
    )


def focus_sources(query: str, sources: list[dict]) -> list[dict]:
    """Focus each subquestion independently; never merge different student fee categories.

    The original passage remains available in Sources. answer_text is a narrower view
    of a reviewed table, not a new fact or a hardcoded fee.
    """
    if re.search(r"\bGPA\b", query, re.I):
        sources = [
            s for s in sources if re.search(r"\bGPA\b", s["text"] + s.get("title", ""), re.I)
        ]
    if general_tuition(query):
        years = re.findall(r"\b20\d{2}\b", query)
        tables = [
            s
            for s in sources
            if s.get("ocr_reviewed")
            and "Tuition fees by discount category" in s["text"]
            and all(year in s["text"] for year in years)
        ]
        if tables:
            sources = tables
            # A plain tuition question needs the base rate. Keep discount rows only
            # when the question asks about them; don't assume a high-school certificate.
            base_only = not re.search(r"discount|scholarship|categor|%", query, re.I) or bool(
                re.search(
                    r"before (?:any )?(?:discount|scholarship)|undiscounted|base", query, re.I
                )
            )
            if base_only:
                projected = []
                for source in sources:
                    lines = source["text"].splitlines()
                    kept = [
                        line
                        for line in lines
                        if not re.match(r"(?:Special )?Category\b", line)
                        or re.search(r"scholarship discount 0%", line)
                    ]
                    projected.append({**source, "answer_text": "\n".join(kept)})
                sources = projected

    procedure = re.search(
        r"\bapply\b|(?:application|admission) (?:steps|process|procedure)", query, re.I
    )
    special_application = re.search(
        r"document|requirement|certificate|international|transfer|scholarship|grant|postgrad|fee|cost",
        query,
        re.I,
    )
    if procedure and not special_application:
        steps = [
            s
            for s in sources
            if re.search(r"Apply Now", s["text"], re.I)
            and re.search(r"create.{0,30}account", s["text"], re.I)
            and not re.search(
                r"international students|study in egypt|office-international",
                s["text"] + s.get("url", ""),
                re.I,
            )
        ]
        sources = steps
    return [{**s, "citation": i} for i, s in enumerate(sources, 1)]


def needs_current_link(text: str) -> bool:
    return bool(
        re.search(
            r"\b(fees?|tuition|cost|scholarship|discount|deadline|apply|application|admission|"
            r"eligibility|policy|policies|schedule|event|competition|registration|current|latest|"
            r"today|open|president|director|contact|phone|hours|inventory|available|availability|"
            r"seats?|copies|meeting|room|reserved|reservation|202\d)\b|"
            r"مصاريف|المصاريف|رسوم|الرسوم|منح|خصم|تقديم|موعد|مواعيد|شروط|دلوقتي|حاليا|"
            r"أحدث|احدث|مدير|رئيس|تليفون|مفتوح|متاح|أماكن|اماكن|اجتماع|قاعة|حجز|محجوز",
            text,
            re.I,
        )
    )


def append_current_links(answer: str, sources: list[dict], language: str) -> str:
    """Links come from retrieved NU pages, not URLs invented by the language model."""
    cited = citation_ids(answer)
    selected = [s for s in sources if s["citation"] in cited] or sources[:2]
    links = {}
    for source in selected:
        url = source.get("url", "")
        try:
            parsed = urlsplit(url)
            host = parsed.hostname or ""
        except ValueError:
            continue
        if parsed.scheme != "https" or not (
            host == "nu.edu.eg"
            or host.endswith(".nu.edu.eg")
            or host == "np.eg"
            or host.endswith(".np.eg")
        ):
            continue
        # A label plus its host is understandable even when the source title is English.
        title = source.get("title", host).split(" — ")[0].split(" | ")[0]
        title = re.sub(r"[\[\]()\n\r]", " ", title).strip()[:100]
        periods = sorted(set(re.findall(r"\b20\d{2}/20\d{2}\b", source.get("text", ""))))
        if source.get("ocr_reviewed") and len(periods) == 1:
            title += " — " + periods[0]
        links.setdefault(url, f"[{title}]({url})")
    missing = [link for url, link in links.items() if f"]({url})" not in answer]
    if not links and "](https://nu.edu.eg/)" not in answer:
        missing = ["[Nile University](https://nu.edu.eg/)"]
    if not missing:
        return answer
    label = (
        "Official pages for details and updates"
        if language == "en"
        else (
            "El links el rasmeya lel tafaseel wel ta7deesat"
            if language == "franco"
            else "التفاصيل والتحديثات على الصفحات الرسمية"
        )
    )
    return answer.rstrip() + "\n\n" + label + ": " + " · ".join(missing) + "."
