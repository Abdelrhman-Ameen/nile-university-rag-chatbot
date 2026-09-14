"""Citation handling must leave code examples unchanged."""

import re

CODE = re.compile(r"```[\s\S]*?(?:```|$)|`[^`\n]*`")


def citation_ids(answer: str) -> set[int]:
    return {int(n) for n in re.findall(r"\[(\d+)\]", CODE.sub("", answer))}


def normalize_citations(answer: str) -> str:
    def replace_groups(prose):
        return re.sub(
            r"\[(\d+(?:\s*,\s*\d+)+)\]",
            lambda m: " ".join(f"[{n}]" for n in re.findall(r"\d+", m[1])),
            prose,
        )

    pieces, start = [], 0
    for match in CODE.finditer(answer):
        pieces.extend([replace_groups(answer[start : match.start()]), match[0]])
        start = match.end()
    pieces.append(replace_groups(answer[start:]))
    return "".join(pieces)
