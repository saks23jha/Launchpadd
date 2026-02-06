import numpy as np
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def cosine_similarity(a, b):
    return np.dot(a, b)


def rerank(query, candidates, chunks, top_k=5):
    """
    query: user query string
    candidates: output of hybrid_retrieve (deduplicated)
    chunks: list of all chunk objects
    """

    query_vec = model.encode(
        [query],
        normalize_embeddings=True
    )[0]

    reranked = []

    for item in candidates:
        cid = item["chunk_id"]
        text = chunks[cid]["text"]

        chunk_vec = model.encode(
            [text],
            normalize_embeddings=True
        )[0]

        score = cosine_similarity(query_vec, chunk_vec)

        reranked.append({
            "chunk_id": cid,
            "rerank_score": float(score),
            "sources": item["sources"]
        })

    # Sort by rerank score (higher is better)
    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)

    return reranked[:top_k]
