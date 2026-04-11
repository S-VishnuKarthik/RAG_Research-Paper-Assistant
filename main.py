
import logging
logging.getLogger("transformers").setLevel(logging.ERROR)
from ingestion.pdf_loader import extract_text_from_pdf
from ingestion.chunker import chunk_text
from indexing.bm25_index import BM25Index
from retrieval.hybrid_retriever import hybrid_search
from retrieval.reranker import rerank
from query.classifier import classify_query
from retrieval.context_builder import build_context
from llm.generator import generate_answer
import sys
import os
from dotenv import load_dotenv
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

from indexing.faiss_index import FAISSIndex
hnsw = FAISSIndex()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load PDFs
files = ["data/2106_09685v2_LoRA.pdf"]

all_chunks = []

for file in files:
    data = extract_text_from_pdf(file)
    chunks = chunk_text(data, file)
    all_chunks.extend(chunks)

texts = [c["content"] for c in all_chunks]

# Build indexes
hnsw = FAISSIndex()
hnsw.build(texts)

bm25 = BM25Index(texts)

# Query loop
while True:
    query = input("\nAsk: ")

    q_type = classify_query(query)

    retrieved = hybrid_search(query, hnsw, bm25, all_chunks)

    reranked = rerank(query, retrieved)

    answer = generate_answer(query, reranked, q_type)

    print("\nANSWER:\n", answer)