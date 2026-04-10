import hnswlib
from embeddings.embedder import Embedder
from config.settings import HNSW_M, HNSW_EF

class HNSWIndex:
    def __init__(self):
        self.embedder = Embedder()
        self.index = None
        self.texts = []

    def build(self, texts):
        embeddings = self.embedder.encode(texts)
        dim = len(embeddings[0])

        self.index = hnswlib.Index(space='cosine', dim=dim)
        self.index.init_index(max_elements=len(texts), ef_construction=200, M=HNSW_M)
        self.index.add_items(embeddings)
        self.index.set_ef(HNSW_EF)

        self.texts = texts

    def query(self, query, k=10):
        q_emb = self.embedder.encode([query])
        labels, _ = self.index.knn_query(q_emb, k=k)
        return labels[0]