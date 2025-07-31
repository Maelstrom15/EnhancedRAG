"""Very simple query parser using regex heuristics.
In production, replace with LLM-based structured extraction."""
import re
from typing import Dict

KEYS = {
    "age": r"(\d{2})(?=\s*(?:years?|y/o|yo|M|F|male|female))",
    "procedure": r"(?:knee|hip|heart|surgery|operation|procedure)\w*",
    "city": r"Pune|Mumbai|Delhi|Bangalore|Chennai",
    "policy_duration": r"(\d+)[-\s]*(?:month|year)"
}

def parse_query(text: str) -> Dict[str, str]:
    extracted: Dict[str, str] = {}
    for key, pattern in KEYS.items():
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            extracted[key] = m.group(0)
    return extracted
