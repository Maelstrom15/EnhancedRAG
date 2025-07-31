"""Semantic retrieval using FAISS vector store."""
from typing import List

from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

from app.config import VECTOR_DB_DIR

_embed_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


def _load_store() -> FAISS:
    return FAISS.load_local(str(VECTOR_DB_DIR), _embed_model)


def retrieve(query: str, top_k: int = 5) -> List[str]:
    try:
        store = _load_store()
    except Exception as exc:
        raise RuntimeError("Vector store not found. Run /ingest first.") from exc

    docs = store.similarity_search(query, k=top_k)
    return [d.page_content for d in docs]
