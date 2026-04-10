def hybrid_search(query, hnsw, bm25, chunks):
    h_ids = hnsw.query(query)
    b_ids = bm25.query(query)

    combined_ids = list(set(h_ids) | set(b_ids))

    return [chunks[i] for i in combined_ids]