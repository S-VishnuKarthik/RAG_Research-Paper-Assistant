import json

from evaluation.metrics import RAGEvaluator
from indexing.faiss_index import FAISSIndex
from indexing.bm25_index import BM25Index
from retrieval.hybrid_retriever import hybrid_search
from retrieval.context_builder import ContextBuilder
from llm.generator import generate_answer
from ingestion.pdf_loader import extract_text_from_pdf
from ingestion.chunker import chunk_text

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
def prepare_data(pdf_paths):
    all_chunks = []

    for path in pdf_paths:
        data = extract_text_from_pdf(path)
        chunks = chunk_text(data, path)

        # 🔥 Ensure IDs exist
        for i, c in enumerate(chunks):
            c["id"] = f"{path}_chunk_{i}"

        all_chunks.extend(chunks)

    texts = [c["content"] for c in all_chunks]

    hnsw = FAISSIndex()
    hnsw.build(texts)

    bm25 = BM25Index(texts)

    return all_chunks, hnsw, bm25


def run_evaluation():
    evaluator = RAGEvaluator()
    context_builder = ContextBuilder()

    # 👉 Load test queries
    with open("evaluation/test_queries.json") as f:
        test_queries = json.load(f)

    # 👉 Load your PDFs
    pdfs = [
        "data/BayesOptimality.pdf", "data/LoRA.txt"
    ]

    chunks, hnsw, bm25 = prepare_data(pdfs)

    for test in test_queries:
        query = test["query"]
        relevant_docs = test["relevant_docs"]

        print("\n==============================")
        print("Query:", query)

        retrieved = hybrid_search(query, hnsw, bm25, chunks)

        context = context_builder.build_context(retrieved)

        answer = generate_answer(query, retrieved, "factual")

        results = evaluator.evaluate_pipeline(
            query,
            retrieved,
            relevant_docs,
            answer,
            context
        )

        print("Results:", results)


if __name__ == "__main__":
    run_evaluation()