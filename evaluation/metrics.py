import numpy as np
from openai import OpenAI
from utils.logger import setup_logger

client = OpenAI()
logger = setup_logger()


class RAGEvaluator:
    def __init__(self):
        self.logger = logger

    # 🔥 Precision@K
    def precision_at_k(self, retrieved_chunks, relevant_docs, k=5):
        retrieved_ids = [c["id"] for c in retrieved_chunks[:k]]
        relevant_set = set(relevant_docs)

        hits = sum([1 for r in retrieved_ids if r in relevant_set])
        return hits / k if k > 0 else 0

    # 🔥 Recall@K
    def recall_at_k(self, retrieved_chunks, relevant_docs, k=5):
        retrieved_ids = [c["id"] for c in retrieved_chunks[:k]]
        relevant_set = set(relevant_docs)

        hits = sum([1 for r in retrieved_ids if r in relevant_set])
        return hits / len(relevant_set) if relevant_set else 0

    # 🔥 Mean Reciprocal Rank (MRR)
    def mean_reciprocal_rank(self, retrieved_chunks, relevant_docs):
        for i, c in enumerate(retrieved_chunks):
            if c["id"] in relevant_docs:
                return 1 / (i + 1)
        return 0

    # 🔥 LLM-based answer evaluation
    def evaluate_answer(self, query, answer, context):
        prompt = f"""
You are an evaluator.

Evaluate the answer based ONLY on the provided context.

Query: {query}

Context:
{context}

Answer:
{answer}

Score the following (0 to 10):
1. Relevance
2. Faithfulness (no hallucination)
3. Completeness

Return JSON:
{{
  "relevance": score,
  "faithfulness": score,
  "completeness": score
}}
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"Evaluation error: {e}")
            return {}

    # 🔥 Full pipeline evaluation
    def evaluate_pipeline(self, query, retrieved_chunks, relevant_docs, answer, context):
        results = {}

        results["precision@5"] = self.precision_at_k(retrieved_chunks, relevant_docs, 5)
        results["recall@5"] = self.recall_at_k(retrieved_chunks, relevant_docs, 5)
        results["mrr"] = self.mean_reciprocal_rank(retrieved_chunks, relevant_docs)

        results["llm_eval"] = self.evaluate_answer(query, answer, context)

        return results