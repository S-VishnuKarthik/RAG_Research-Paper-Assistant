from rank_bm25 import BM25Okapi
from utils.text_utils import normalize_text, remove_special_chars
from utils.logger import setup_logger

import numpy as np

logger = setup_logger()


class BM25Index:
    def __init__(self, texts, metadata=None):
        """
        texts: list of chunk contents
        metadata: list of chunk metadata (optional)
        """

        self.texts = texts
        self.metadata = metadata or [{} for _ in texts]

        # 🔥 Preprocess corpus
        self.tokenized_corpus = [self._preprocess(t) for t in texts]

        logger.info("Building BM25 index...")
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    # 🔥 Advanced preprocessing
    def _preprocess(self, text):
        text = normalize_text(text)
        text = remove_special_chars(text)

        tokens = text.split()

        # 🔥 Remove stopwords (basic)
        stopwords = {"the", "is", "and", "of", "in", "to", "a", "for"}
        tokens = [t for t in tokens if t not in stopwords]

        return tokens

    # 🔥 Query expansion (simple but effective)
    def _expand_query(self, query):
        query = query.lower()

        expansions = {
            "method": ["approach", "algorithm", "technique"],
            "result": ["performance", "evaluation"],
            "summary": ["overview", "abstract"]
        }

        expanded = query.split()

        for word in query.split():
            if word in expansions:
                expanded.extend(expansions[word])

        return expanded

    # 🔥 Score normalization
    def _normalize_scores(self, scores):
        if len(scores) == 0:
            return scores

        min_s = np.min(scores)
        max_s = np.max(scores)

        if max_s - min_s == 0:
            return scores

        return (scores - min_s) / (max_s - min_s)

    # 🔥 Section-based boosting
    def _apply_section_boost(self, scores, query_tokens):
        boosted = scores.copy()

        for i, meta in enumerate(self.metadata):
            section = meta.get("section", "")

            # 🔥 Example boosting logic
            if "method" in query_tokens and section == "methodology":
                boosted[i] += 0.2

            if "result" in query_tokens and section == "results":
                boosted[i] += 0.2

            if "abstract" in query_tokens and section == "abstract":
                boosted[i] += 0.3

        return boosted

    # 🔥 Main query function
    def query(self, query, k=10, threshold=0.0):
        """
        Returns top-k indices ranked by BM25 score
        """

        # 🔥 Preprocess query
        tokens = self._preprocess(query)

        # 🔥 Expand query
        tokens = self._expand_query(" ".join(tokens))

        # 🔥 Get raw scores
        scores = np.array(self.bm25.get_scores(tokens))

        # 🔥 Normalize scores
        scores = self._normalize_scores(scores)

        # 🔥 Apply section boost
        scores = self._apply_section_boost(scores, tokens)

        # 🔥 Filter by threshold
        valid_indices = [i for i, s in enumerate(scores) if s > threshold]

        # 🔥 Sort
        ranked = sorted(valid_indices, key=lambda i: scores[i], reverse=True)

        top_k = ranked[:k]

        logger.info(f"BM25 retrieved {len(top_k)} results")

        return list(map(int, np.array(top_k).flatten()))

    # 🔥 Debug utility
    def get_scores(self, query):
        tokens = self._preprocess(query)
        return self.bm25.get_scores(tokens)