"""Deterministic safeguards for named Nile University entities."""

import re

NU_ENTITIES = (
    "nile university",
    "جامعة النيل",
    "nu bus",
    "nu library",
    "filmfish",
    "pixels",
    "wessal",
    "simulatopedia",
    "simulatopidia",
    "graduate starter pack",
    "gsp",
    "ugrf",
    "iecc",
    "nilepreneurs",
    "constructx",
    "nile bus",
)

UNIVERSITY_CONTEXT = re.compile(
    r"\b(?:nile university|NU|campus|admission|tuition|scholarship|UGRF|IECC|"
    r"FilmFish|Wessal|Simulatopedia|NilePreneurs)\b|جامعة النيل|الجامعة|الجامعه|الحرم|حرم النيل",
    re.I,
)


def mentions_nu_entity(text: str) -> bool:
    lowered = text.casefold()
    if any(entity in lowered for entity in NU_ENTITIES):
        return True
    return bool(re.search(r"\bNU(?:'s)?\b", text, re.I))


def has_university_context(text: str) -> bool:
    """Catch explicit or strongly implied university wording before a fast route."""
    return mentions_nu_entity(text) or bool(UNIVERSITY_CONTEXT.search(text))


def direct_live_query(text: str) -> str:
    """Build a stable retrieval query for answers that require a live NU system."""
    if re.search(r"\b(?:bus|transport|seats?|capacity)\b|أتوبيس|اتوبيس|نقل", text, re.I):
        return "Nile University transportation bus service official contact"
    if re.search(r"\b(?:library|book|copies|catalog(?:ue)?)\b|مكتبة|كتاب|نسخ", text, re.I):
        return "Nile University library catalogue official contact"
    if re.search(r"\b(?:guest house|housing|reservation|booking)\b|سكن|حجز", text, re.I):
        return "Nile University guest house reservation official contact"
    if re.search(r"filmfish", text, re.I):
        return "Nile University FilmFish official page contact"
    return "Nile University official contact"


def is_simple_named_nu_question(text: str) -> bool:
    """Allow one clear English NU question to use the original query directly."""
    if not mentions_nu_entity(text) or text.count("?") > 1:
        return False
    # Keep the model planner for messages that combine an NU request with unrelated work.
    return not bool(
        re.search(
            r"\band\s+(?:also\s+)?(?:explain|write|rewrite|translate|calculate|code|summari[sz]e)\b",
            text,
            re.I,
        )
    )


def is_nu_fact_request(text: str) -> bool:
    """Identify concrete NU facts that must not become a recruitment answer."""
    return bool(
        re.search(
            r"\b(?:admission|requirement|eligible|eligibility|accept|target graduates?|"
            r"IB|TOK|TOEFL|IELTS|GPA|MSc|PhD|master|diploma|certificate|fees?|cost|"
            r"price|timeline|weeks?|bus|transport|email|director|project|report|PoC|pilot)\b|"
            r"قبول|شروط|مصاريف|رسوم|أتوبيس|اتوبيس|مدير|مدة|مشروع|تقرير",
            text,
            re.I,
        )
    )
