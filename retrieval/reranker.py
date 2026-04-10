from sentence_transformers import CrossEncoder
from config.settings import CROSS_ENCODER_MODEL, FINAL_TOP_K

model = CrossEncoder(CROSS_ENCODER_MODEL)

def rerank(query, chunks):
    pairs = [(query, c["content"]) for c in chunks]
    scores = model.predict(pairs)

    ranked = sorted(zip(chunks, scores), key=lambda x: x[1], reverse=True)

    return [r[0] for r in ranked[:FINAL_TOP_K]]