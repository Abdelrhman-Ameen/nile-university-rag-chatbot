"""Transparent language routing, not an SBERT classification head.

Franco is unstandardized: rules are a baseline, and the UI allows correction.
Qwen performs the actual contextual Franco-to-English query normalization.
"""

import re
import unicodedata

FRANCO_WORDS = {
    "enta",
    "enty",
    "meen",
    "ezay",
    "ezzay",
    "ezai",
    "3ayez",
    "3ayza",
    "3aiz",
    "3aiza",
    "3ayz",
    "3awz",
    "3awza",
    "ana",
    "eh",
    "eih",
    "ay",
    "feen",
    "fen",
    "kam",
    "bekam",
    "bkam",
    "masareef",
    "masarif",
    "game3a",
    "gam3a",
    "elgam3a",
    "elgame3a",
    "men7a",
    "mena7",
    "shoroot",
    "shorout",
    "ta2deem",
    "a2adem",
    "a2dem",
    "momken",
    "el",
    "elly",
    "3an",
    "3andy",
    "3andi",
    "3ndkom",
    "3andkom",
    "3ala",
    "7aga",
    "7agat",
    "fi",
    "fe",
    "fy",
    "da",
    "dah",
    "di",
    "de",
    "law",
    "mesh",
    "msh",
    "ba2a",
    "bta3",
    "bta3et",
    "3araby",
    "bel",
    "keda",
    "kda",
    "3amla",
    "3amel",
    "nafs",
    "elneel",
    "elnile",
}
AMBIGUOUS = {
    "ana",
    "eh",
    "ay",
    "kam",
    "el",
    "fi",
    "fe",
    "fy",
    "da",
    "di",
    "de",
    "law",
    "mesh",
    "bel",
}
FRANCO_HINTS = {
    "mabsoot": "happy",
    "mabsout": "happy",
    "naga7t": "I passed",
    "sa2att": "I failed",
    "3ashan": "because",
    "makhnoo2": "frustrated and overwhelmed",
    "makhno2": "frustrated and overwhelmed",
    "mdaye2": "upset",
    "za3lan": "upset",
    "bakrah": "I hate",
    "masareef": "tuition fees",
    "masarif": "tuition fees",
    "bekam": "cost",
    "bkam": "cost",
    "men7a": "scholarship",
    "mena7": "scholarships",
    "shoroot": "requirements",
    "shorout": "requirements",
    "ta2deem": "admission apply",
    "a2adem": "apply",
    "a2dem": "apply",
    "game3a": "university",
    "gam3a": "university",
    "elgame3a": "university",
    "elgam3a": "university",
    "feen": "location",
    "fen": "location",
    "tanseek": "admission minimum score",
    "awra2": "documents",
    "wara2": "documents",
    "man7a": "scholarship",
    "elneel": "Nile",
    "elnile": "Nile",
    "a7awel": "transfer",
    "ta7weel": "transfer",
    "emt7an": "exam",
    "emte7an": "exam",
}
FRANCO_WORDS.update(FRANCO_HINTS)


def tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text.lower())
    text = re.sub(r"[\u064b-\u065f\u0670\u0640]", "", text)
    text = re.sub("[أإآ]", "ا", text).replace("ى", "ي")
    return re.findall(r"[^\W_]+", text, flags=re.UNICODE)


def detect_language(text: str) -> str:
    arabic = bool(re.search(r"[\u0621-\u064a]", text))
    latin = bool(re.search(r"[a-zA-Z]", text))
    if arabic:
        return "mixed" if latin else "ar"
    words = tokens(text)
    # Digits in ordinary dates/numbers do not count as Arabizi evidence.
    arabizi = any(re.fullmatch(r"[a-z]*[2356789][a-z]{2,}[a-z2356789]*", w) for w in words)
    distinct = set(words) & (FRANCO_WORDS - AMBIGUOUS)
    if arabizi or distinct or len(set(words) & FRANCO_WORDS) >= 2:
        return "franco"
    return "en"


def fallback_query(text: str) -> str:
    """A small domain glossary when Qwen is unavailable; not a full translator."""
    hints = [FRANCO_HINTS[w] for w in tokens(text) if w in FRANCO_HINTS]
    return text + ("\n" + " ".join(hints) if hints else "")
