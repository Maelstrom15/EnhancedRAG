from typing import List, Optional
from pydantic import BaseModel, Field


class IngestResponse(BaseModel):
    status: str = Field(..., description="Result of ingestion request")
    files_ingested: int = Field(..., description="Number of documents successfully ingested")


class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query from the user")
    top_k: int = Field(5, description="Number of clauses to retrieve")


class Clause(BaseModel):
    clause_id: str
    text: str
    source_path: str


class QueryResponse(BaseModel):
    decision: Optional[str] = None
    amount: Optional[float] = None
    justification: List[Clause] = Field(default_factory=list)
