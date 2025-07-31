"""Document ingestion and embedding pipeline stub."""
from pathlib import Path
from typing import List

import faiss
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

from app.config import VECTOR_DB_DIR


def load_documents(paths: List[Path]) -> List[str]:
    # TODO: real PDF/Word/email parsing. For now, read plain text.
    texts = []
    for p in paths:
        try:
            texts.append(p.read_text())
        except Exception:
            print(f"Skipping unreadable file {p}")
    return texts


def build_vector_store(texts: List[str]) -> FAISS:
    embed_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.from_texts(texts, embed_model)
    vectordb.save_local(str(VECTOR_DB_DIR))
    return vectordb


def ingest(paths: List[str]):
    doc_paths = [Path(p) for p in paths]
    texts = load_documents(doc_paths)
    _ = build_vector_store(texts)
    return len(texts)
