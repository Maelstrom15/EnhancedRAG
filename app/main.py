"""FastAPI entry point wiring ingestion, retrieval, and decision modules."""
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import IngestResponse, QueryRequest, QueryResponse
from app import ingestion, retrieval, decision
from app.utils.query_parser import parse_query

app = FastAPI(title="LLM Clause Decision API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ingest", response_model=IngestResponse)
def ingest(files: List[str]):
    """Ingest documents given their filesystem paths (simple stub)."""
    try:
        count = ingestion.ingest(files)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return IngestResponse(status="success", files_ingested=count)


@app.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    """Parse query, retrieve relevant clauses, and make a decision."""
    parsed = parse_query(req.query)
    clauses = retrieval.retrieve(req.query, top_k=req.top_k)
    response = decision.evaluate(parsed, clauses)
    return response
