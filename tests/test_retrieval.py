from retrieval.hybrid_retriever import hybrid_search

def test_hybrid_retrieval(dummy_hnsw, dummy_bm25, dummy_chunks):
    results = hybrid_search("test query", dummy_hnsw, dummy_bm25, dummy_chunks)
    assert isinstance(results, list)
    assert len(results) > 0