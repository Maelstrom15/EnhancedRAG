"""Very simple query parser using regex heuristics.
In production, replace with LLM-based structured extraction."""
import re
import json
from typing import Dict
from app.utils.llm import chat

KEYS = {
    "age": r"(\\d{2})(?=\\s*(?:years?|y/o|yo|M|F|male|female))",
    "procedure": r"(?:knee|hip|heart|surgery|operation|procedure)\\w*",
    "city": r"Pune|Mumbai|Delhi|Bangalore|Chennai",
    "policy_duration": r"(\\d+)[-\\s]*(?:month|year)"
}

LLM_SCHEMA = {
    "age": "string (e.g., '46') or empty",
    "procedure": "string (e.g., 'knee surgery') or empty",
    "city": "string (e.g., 'Pune') or empty",
    "policy_duration": "string (e.g., '3-month') or empty"
}


def _regex_parse(text: str) -> Dict[str, str]:
    extracted: Dict[str, str] = {}
    for key, pattern in KEYS.items():
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            extracted[key] = m.group(0)
    return extracted


def parse_query(text: str) -> Dict[str, str]:
    """Parse natural language query into structured fields using LLM, fallback to regex."""
    try:
        prompt = (
            "You are an extraction engine. Given a natural language insurance claim query, "
            "extract the following fields and return **ONLY** valid JSON without any extra text. "
            f"Schema: {json.dumps(LLM_SCHEMA)}. If a field is missing, use an empty string."
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ]
        response = chat(messages, max_tokens=150)
        data = json.loads(response)
        if isinstance(data, dict):
            return data
    except Exception:
        # Fall back to simple regex if LLM fails or env var missing.
        pass
    return _regex_parse(text)
