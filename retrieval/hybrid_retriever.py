
import numpy as np

def safe_to_int_list(arr):
    """
    Converts ANY numpy/list structure to flat int list safely
    """
    try:
        arr = np.array(arr)

        # flatten deeply
        arr = arr.reshape(-1)

        # convert each element safely
        return [int(x) if np.isscalar(x) else int(np.array(x).item()) for x in arr]

    except Exception as e:
        print("ERROR converting indices:", arr)
        raise e


def safe_to_float_list(arr):
    try:
        arr = np.array(arr).reshape(-1)
        return [float(x) if np.isscalar(x) else float(np.array(x).item()) for x in arr]
    except Exception as e:
        print("ERROR converting scores:", arr)
        raise e


def hybrid_search(query, hnsw, bm25, chunks, k=20, alpha=0.7):

    # 🔥 FAISS QUERY
    faiss_result = hnsw.query(query, k)

    if isinstance(faiss_result, tuple):
        h_indices, h_scores = faiss_result
    else:
        h_indices = faiss_result
        h_scores = [1.0] * len(h_indices)

    # 🔥 SAFE CONVERSION
    h_indices = safe_to_int_list(h_indices)
    h_scores = safe_to_float_list(h_scores)

    # 🔥 BM25 QUERY
    b_indices = bm25.query(query, k)
    b_indices = safe_to_int_list(b_indices)

    # 🔥 DEBUG (VERY IMPORTANT)
    print("FAISS indices:", h_indices[:5])
    print("BM25 indices:", b_indices[:5])

    scores = {}

    # 🔥 FAISS scoring
    for idx, score in zip(h_indices, h_scores):
        scores[idx] = scores.get(idx, 0) + alpha * score

    # 🔥 BM25 scoring
    for rank, idx in enumerate(b_indices):
        scores[idx] = scores.get(idx, 0) + (1 - alpha) * (1 / (rank + 1))

    # 🔥 Normalize
    if scores:
        max_score = max(scores.values())
        if max_score > 0:
            scores = {k: v / max_score for k, v in scores.items()}

    # 🔥 Sort
    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

    # 🔥 SAFE RETURN
    results = []
    for i in sorted_ids[:k]:
        if isinstance(i, int) and 0 <= i < len(chunks):
            results.append(chunks[i])

    return results