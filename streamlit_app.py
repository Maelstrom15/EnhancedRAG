"""Streamlit UI for uploading documents, ingesting, querying, and showing decisions."""
import json
from pathlib import Path
from typing import List

import streamlit as st

from app import ingestion, retrieval, decision
from app.utils.query_parser import parse_query

st.set_page_config(page_title="LLM Clause Decision UI", layout="wide")
st.title("📄🧠 LLM-Powered Clause Decision Helper")

# --- Sidebar: Document ingestion ---
st.sidebar.header("📁 Document Ingestion")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF, DOCX, EML, or TXT files", accept_multiple_files=True
)

if st.sidebar.button("Ingest Documents"):
    if not uploaded_files:
        st.sidebar.warning("No files selected.")
    else:
        save_dir = Path("uploaded")
        save_dir.mkdir(exist_ok=True)
        saved_paths: List[str] = []
        for uf in uploaded_files:
            dest = save_dir / uf.name
            dest.write_bytes(uf.getbuffer())
            saved_paths.append(str(dest))
        count = ingestion.ingest(saved_paths)
        st.sidebar.success(f"Ingested {count} chunks from {len(uploaded_files)} document(s).")

# --- Main: Query form ---
st.subheader("🔍 Query")
query_text = st.text_input(
    "Enter natural language claim query", value="46-year-old male, knee surgery in Pune, 3-month-old policy"
)
col1, col2 = st.columns([1, 3])
with col1:
    top_k = st.number_input("Top K clauses", min_value=1, max_value=10, value=5, step=1)
    run_btn = st.button("Run Query")

if run_btn and query_text:
    with st.spinner("Parsing query & retrieving clauses…"):
        parsed = parse_query(query_text)
        clauses = retrieval.retrieve(query_text, top_k=int(top_k))
        result = decision.evaluate(parsed, clauses)

    st.write("### Parsed Fields")
    st.json(parsed, expanded=False)

    st.write("### Decision")
    st.json(json.loads(result.model_dump_json()), expanded=False)

    st.write("### Clauses")
    for idx, clause in enumerate(clauses):
        st.write(f"**Clause {idx+1}:**")
        st.code(clause)
