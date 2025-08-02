"""Document ingestion and embedding pipeline stub."""
from pathlib import Path
from typing import List

import faiss
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS

from app.config import VECTOR_DB_DIR
from pdfminer.high_level import extract_text as pdf_extract_text
import docx
from email import policy
from email.parser import BytesParser


def _read_file(path: Path) -> str:
    """Return raw text from PDF, DOCX, email (.eml), or plaintext file."""
    try:
        if path.suffix.lower() == ".pdf":
            return pdf_extract_text(str(path))
        if path.suffix.lower() in {".docx", ".doc"}:
            doc = docx.Document(str(path))
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        if path.suffix.lower() == ".eml":
            with path.open("rb") as fp:
                msg = BytesParser().parse(fp)
            # Prefer plain text body; fallback to HTML stripped of tags
            if msg.is_multipart():
                parts = [p.get_payload(decode=True) for p in msg.walk() if p.get_content_type() == "text/plain"]
                return "\n".join((bytes(part).decode(errors="ignore") if isinstance(part, (bytes, bytearray)) else str(part)) for part in parts)
            payload = msg.get_payload(decode=True)
            if isinstance(payload, (bytes, bytearray)):
                return payload.decode(errors="ignore")
            # If payload is already a string or other type, coerce to string safely
            return str(payload)
        # Fallback: treat as plaintext
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        print(f"Skipping unreadable file {path}: {exc}")
        return ""


def _chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Simple sliding-window chunker over text characters."""
    if not text:
        return []
    chunks = []
    start = 0
    length = len(text)
    while start < length:
        end = min(start + chunk_size, length)
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def load_documents(paths: List[Path]) -> List[str]:
    """Load all files and return list of chunk texts."""
    all_chunks: List[str] = []
    for p in paths:
        raw_text = _read_file(p)
        all_chunks.extend(_chunk_text(raw_text))
    return all_chunks


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
