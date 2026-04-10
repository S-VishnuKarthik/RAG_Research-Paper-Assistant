from rank_bm25 import BM25Okapi

class BM25Index:
    def __init__(self, texts):
        tokenized = [t.split() for t in texts]
        self.bm25 = BM25Okapi(tokenized)

    def query(self, query, k=10):
        scores = self.bm25.get_scores(query.split())
        return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]