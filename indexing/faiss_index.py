import faiss
import numpy as np
from embeddings.embedder import Embedder

class FAISSIndex:
    def __init__(self):
        self.embedder = Embedder()
        self.index = None
        self.texts = []

    def build(self, texts):
        embeddings = self.embedder.encode(texts)
        embeddings = np.array(embeddings).astype('float32')

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        self.texts = texts

    def query(self, query, k=10):
        q_emb = self.embedder.encode([query])
        q_emb = np.array(q_emb).astype('float32')

        distances, indices = self.index.search(q_emb, k)
        return indices[0]