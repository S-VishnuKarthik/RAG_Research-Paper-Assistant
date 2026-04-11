from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL
from utils.logger import setup_logger

import numpy as np
import torch
import hashlib

class Embedder:
    def __init__(self, normalize=True, use_cache=True):
        self.logger = setup_logger()
        self.normalize = normalize
        self.use_cache = use_cache

        # 🔥 Auto device detection
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        self.logger.info(f"Using device: {self.device}")

        self.model = SentenceTransformer(EMBEDDING_MODEL, device=self.device)

        # 🔥 Simple in-memory cache
        self.cache = {}

    # 🔥 Hash function for caching
    def _hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    # 🔥 Normalize embeddings
    def _normalize(self, embeddings):
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / (norms + 1e-10)

    # 🔥 Core encoding function
    def encode(self, texts, batch_size=32):
        """
        Supports:
        - single string
        - list of strings
        """

        if isinstance(texts, str):
            texts = [texts]

        results = []
        uncached_texts = []
        uncached_indices = []

        # 🔥 Step 1: Check cache
        for i, text in enumerate(texts):
            key = self._hash(text)

            if self.use_cache and key in self.cache:
                results.append(self.cache[key])
            else:
                results.append(None)
                uncached_texts.append(text)
                uncached_indices.append(i)

        # 🔥 Step 2: Encode uncached texts
        if uncached_texts:
            try:
                embeddings = self.model.encode(
                    uncached_texts,
                    batch_size=batch_size,
                    convert_to_numpy=True,
                    show_progress_bar=False
                )

                # 🔥 Normalize if enabled
                if self.normalize:
                    embeddings = self._normalize(embeddings)

                # 🔥 Store in cache + results
                for idx, emb in zip(uncached_indices, embeddings):
                    results[idx] = emb
                    if self.use_cache:
                        key = self._hash(texts[idx])
                        self.cache[key] = emb

            except Exception as e:
                self.logger.error(f"Embedding error: {e}")
                raise

        return np.array(results)

    # 🔥 Utility: clear cache
    def clear_cache(self):
        self.cache = {}
        self.logger.info("Embedding cache cleared")

    # 🔥 Utility: cache size
    def cache_size(self):
        return len(self.cache)