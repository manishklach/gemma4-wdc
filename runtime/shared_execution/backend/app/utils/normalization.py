from __future__ import annotations

import json
import re
from hashlib import sha256
from typing import Any


def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def normalize_intent_text(text: str) -> str:
    text = normalize_whitespace(text)
    text = text.replace("-", " ")
    replacements = {
        "locate": "find",
        "identify": "find",
        "state machine": "transition path",
        "code path": "transition path",
        "path that": "",
        "moves": "transition",
        "moving": "transition",
        "begins execution": "to executing",
        "begin execution": "to executing",
        "beginning execution": "to executing",
        "leave the admission window": "to executing",
        "leaves the admission window": "to executing",
        "from pending to executing": "to executing",
        "pending shared work": "shared execution units",
        "shared work": "shared execution units",
        "discussing": "about",
        "mentions": "about",
        "passages": "evidence",
        "extract": "summarize",
        "claims": "argument",
        "trade offs": "tradeoffs",
        "trade off": "tradeoffs",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def normalize_sql(query: str) -> str:
    query = normalize_whitespace(query)
    query = re.sub(r"\s*,\s*", ", ", query)
    query = re.sub(r"\s*=\s*", " = ", query)
    query = re.sub(r"'([a-z0-9_\-]+)'", r"\1", query)
    return query


def normalize_text_list(items: list[str]) -> list[str]:
    return sorted(normalize_whitespace(item) for item in items)


def stable_hash(value: Any) -> str:
    return sha256(stable_json(value).encode("utf-8")).hexdigest()[:16]
