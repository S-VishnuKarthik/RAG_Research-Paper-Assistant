        
import streamlit as st
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#  Import modules
from ingestion.pdf_loader import extract_text_from_pdf
from ingestion.chunker import chunk_text
from indexing.faiss_index import FAISSIndex
from indexing.bm25_index import BM25Index
from retrieval.hybrid_retriever import hybrid_search
from retrieval.reranker import rerank
from retrieval.filter import filter_chunks, fallback_filter
from retrieval.context_builder import ContextBuilder
from query.classifier import classify_query
from query.query_processor import QueryProcessor
from llm.generator import generate_answer
from utils.file_utils import save_uploaded_file

#  Import UI components
from app.components import *

#  Load CSS
def load_css():
    with open("app/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.set_page_config(page_title="RAG Assistant", layout="wide")

render_header()

#  Initialize session
if "chunks" not in st.session_state:
    st.session_state.chunks = None
    st.session_state.hnsw = None
    st.session_state.bm25 = None
    st.session_state.processor = QueryProcessor()
    st.session_state.context_builder = ContextBuilder()

#  Upload
uploaded_files = render_file_uploader()

#  Process PDFs
if uploaded_files and render_process_button():
    try:
        all_chunks = []

        for file in uploaded_files:
            filepath = save_uploaded_file(file)

            data = extract_text_from_pdf(filepath)
            chunks = chunk_text(data, filepath)

            all_chunks.extend(chunks)

        texts = [c["content"] for c in all_chunks]

        #  Build indexes
        hnsw = FAISSIndex(index_type="flat")
        hnsw.build(texts, metadata=all_chunks)

        bm25 = BM25Index(texts, metadata=all_chunks)

        st.session_state.chunks = all_chunks
        st.session_state.hnsw = hnsw
        st.session_state.bm25 = bm25

        render_success("PDFs processed successfully!")

    except Exception as e:
        render_error(str(e))

#  Query
query = render_query_input()

if query and st.session_state.chunks:

    start_time = time.time()

    with st.spinner("Thinking... 🤖"):

        #  Step 1: classify
        q_type = classify_query(query)

        #  Step 2: process query
        processed = st.session_state.processor.process(query, q_type)

        #  Step 3: retrieval
        retrieved = hybrid_search(
            processed["enhanced_query"],
            st.session_state.hnsw,
            st.session_state.bm25,
            st.session_state.chunks
        )

        #  Step 4: filtering
        filtered = filter_chunks(retrieved, processed["constraints"])
        final_chunks = fallback_filter(retrieved, filtered)

        #  Step 5: rerank
        reranked = rerank(query, final_chunks)
        for c in reranked[:5]:
            print(c["section"], c["content"][:100])

        #  Step 6: context
        context = st.session_state.context_builder.build_context(reranked)

        #  Step 7: LLM
        answer = generate_answer(query, reranked, q_type)

    end_time = time.time()

    #  Output
    render_answer(answer)

    render_metrics(end_time - start_time, len(reranked))

    render_sources(reranked)

    render_debug_info(q_type, processed, retrieved, filtered, reranked)

#  Empty state
elif not st.session_state.chunks:
    render_empty()