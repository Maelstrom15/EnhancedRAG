"""Very simple decision engine placeholder.
   Takes parsed query and retrieved clauses, returns dummy decision.
"""
from typing import List, Dict

from app.models import QueryResponse, Clause


def evaluate(parsed_query: Dict[str, str], clauses: List[str]) -> QueryResponse:
    # Placeholder: always approve if any clauses returned, else reject
    decision = "approved" if clauses else "rejected"
    justification = [
        Clause(clause_id=f"clause_{i}", text=clause, source_path="N/A")
        for i, clause in enumerate(clauses)
    ]
    return QueryResponse(decision=decision, amount=None, justification=justification)
