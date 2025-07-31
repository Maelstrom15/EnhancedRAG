"""Quick demo script: ingest sample docs and run a sample query."""
from pathlib import Path
from app import ingestion, retrieval, decision
from app.utils.query_parser import parse_query

SAMPLE_DOC = Path("data/samples/policy.txt").resolve()


def main():
    print("Ingesting sample document…")
    ingestion.ingest([str(SAMPLE_DOC)])

    sample_query = "46M, knee surgery, Pune, 3-month policy"
    print(f"Running query: {sample_query}")
    parsed = parse_query(sample_query)
    clauses = retrieval.retrieve(sample_query, top_k=5)
    result = decision.evaluate(parsed, clauses)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
