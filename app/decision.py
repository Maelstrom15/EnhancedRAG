"""Very simple decision engine placeholder.
   Takes parsed query and retrieved clauses, returns dummy decision.
"""
from typing import List, Dict

from app.models import QueryResponse, Clause


def evaluate(parsed_query: Dict[str, str], clauses: List[str]) -> QueryResponse:
    """Ask LLM to reason on retrieved clauses and return a structured decision JSON."""
    import json
    from app.utils.llm import chat

    if not clauses:
        return QueryResponse(decision="rejected", amount=None, justification=[])

    system_prompt = (
        "You are an insurance policy reasoning assistant. Given structured query fields and a set of relevant policy clauses, "
        "decide whether the claim is approved, and the payout amount if applicable. "
        "Output ONLY valid JSON matching this schema: {\n"
        "  \"decision\": 'approved' | 'rejected',\n"
        "  \"amount\": number | null,\n"
        "  \"justification\": [\n"
        "     {\"clause_id\": string, \"text\": string, \"used_for\": string}\n"
        "  ]\n}"
    )

    user_content = (
        f"Parsed query fields: {json.dumps(parsed_query)}\n\n"
        f"Relevant clauses (each separated by ---):\n" + "\n---\n".join(clauses)
    )

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        response = chat(messages, max_tokens=300)
        data = json.loads(response)
        if isinstance(data, dict):
            justification_objs = [
                Clause(
                    clause_id=j.get("clause_id", ""),
                    text=j.get("text", ""),
                    source_path="N/A",
                )
                for j in data.get("justification", [])
            ]
            return QueryResponse(
                decision=data.get("decision"),
                amount=data.get("amount"),
                justification=justification_objs,
            )
    except Exception:
        # fallback simplistic decision: approve if any clauses mention the procedure
        approved = any(parsed_query.get("procedure", "").split()[0].lower() in c.lower() for c in clauses)
        decision = "approved" if approved else "rejected"
        justification = [
            Clause(clause_id=f"clause_{i}", text=clause, source_path="N/A")
            for i, clause in enumerate(clauses)
        ]
        return QueryResponse(decision=decision, amount=None, justification=justification)
