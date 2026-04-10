import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingestion.pdf_loader import extract_text_from_pdf
from ingestion.chunker import chunk_text
from indexing.faiss_index import FAISSIndex
from indexing.bm25_index import BM25Index
from retrieval.hybrid_retriever import hybrid_search
from retrieval.reranker import rerank
from query.classifier import classify_query
from llm.generator import generate_answer

import os

st.title("📄 Smart Research Paper Assistant (RAG)")

# Upload PDFs
uploaded_files = st.file_uploader(
    "Upload Research Papers (PDFs)",
    type="pdf",
    accept_multiple_files=True
)

# Store processed data
if "chunks" not in st.session_state:
    st.session_state.chunks = None
    st.session_state.hnsw = None
    st.session_state.bm25 = None

# Process PDFs
if uploaded_files and st.button("Process PDFs"):
    all_chunks = []

    for file in uploaded_files:
        with open(file.name, "wb") as f:
            f.write(file.getbuffer())

        data = extract_text_from_pdf(file.name)
        chunks = chunk_text(data, file.name)
        all_chunks.extend(chunks)

    texts = [c["content"] for c in all_chunks]

    # Build indexes
    hnsw = FAISSIndex()
    hnsw.build(texts)

    bm25 = BM25Index(texts)

    st.session_state.chunks = all_chunks
    st.session_state.hnsw = hnsw
    st.session_state.bm25 = bm25

    st.success("✅ PDFs processed successfully!")

# Query section
query = st.text_input("Ask your question")

if query and st.session_state.chunks:
    with st.spinner("Thinking... 🤖"):

        q_type = classify_query(query)

        retrieved = hybrid_search(
            query,
            st.session_state.hnsw,
            st.session_state.bm25,
            st.session_state.chunks
        )

        reranked = rerank(query, retrieved)

        answer = generate_answer(query, reranked, q_type)

    st.subheader("📌 Answer")
    st.write(answer)