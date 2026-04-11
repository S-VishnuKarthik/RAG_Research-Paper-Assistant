import faiss
import numpy as np
import os

from embeddings.embedder import Embedder
from utils.logger import setup_logger

logger = setup_logger()


class FAISSIndex:
    def __init__(self, index_type="flat", use_gpu=False):
        """
        index_type:
            - flat (exact search)
            - ivf (faster approximate)
        """
        self.embedder = Embedder()
        self.index = None
        self.texts = []
        self.metadata = []
        self.index_type = index_type
        self.use_gpu = use_gpu
        self.dimension = None

    # 🔥 Normalize vectors (for cosine similarity)
    def _normalize(self, vectors):
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return vectors / (norms + 1e-10)

    # 🔥 Build index
    def build(self, texts, metadata=None):
        if not texts:
            raise ValueError("No texts provided for indexing")

        logger.info("Generating embeddings...")

        embeddings = self.embedder.encode(texts)
        embeddings = np.array(embeddings).astype("float32")

        # 🔥 Normalize (important for cosine similarity)
        embeddings = self._normalize(embeddings)

        self.dimension = embeddings.shape[1]

        logger.info(f"Embedding dimension: {self.dimension}")

        # 🔥 Choose index type
        if self.index_type == "flat":
            self.index = faiss.IndexFlatIP(self.dimension)  # cosine similarity

        elif self.index_type == "ivf":
            nlist = 100  # clusters
            quantizer = faiss.IndexFlatIP(self.dimension)
            self.index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist)

            logger.info("Training IVF index...")
            self.index.train(embeddings)

        else:
            raise ValueError("Unsupported index type")

        # 🔥 Add vectors
        self.index.add(embeddings)

        self.texts = texts
        self.metadata = metadata if metadata else [{} for _ in texts]

        logger.info(f"FAISS index built with {len(texts)} vectors")

    # 🔥 Query single
    def query(self, query, k=10):
        if self.index is None:
            raise ValueError("Index not built yet")

        q_emb = self.embedder.encode([query])
        q_emb = np.array(q_emb).astype("float32")

        q_emb = self._normalize(q_emb)

        scores, indices = self.index.search(q_emb, k)

        return indices[0], scores[0]

    # 🔥 Query batch (VERY USEFUL)
    def query_batch(self, queries, k=10):
        q_emb = self.embedder.encode(queries)
        q_emb = np.array(q_emb).astype("float32")

        q_emb = self._normalize(q_emb)

        scores, indices = self.index.search(q_emb, k)

        return indices, scores

    # 🔥 Return chunks directly
    def query_with_metadata(self, query, k=10):
        indices, scores = self.query(query, k)

        results = []

        for idx, score in zip(indices, scores):
            results.append({
                "content": self.texts[idx],
                "score": float(score),
                "metadata": self.metadata[idx]
            })

        return results

    # 🔥 Save index
    def save(self, path="faiss_index.bin"):
        if self.index is None:
            raise ValueError("No index to save")

        faiss.write_index(self.index, path)
        logger.info(f"Index saved to {path}")

    # 🔥 Load index
    def load(self, path="faiss_index.bin"):
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found")

        self.index = faiss.read_index(path)
        logger.info(f"Index loaded from {path}")

    # 🔥 Get stats
    def get_stats(self):
        return {
            "total_vectors": self.index.ntotal if self.index else 0,
            "dimension": self.dimension,
            "index_type": self.index_type
        }