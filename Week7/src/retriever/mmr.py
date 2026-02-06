import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def mmr(query, candidates, chunks, k=5, lambda_=0.7):
    qvec = model.encode([query], normalize_embeddings=True)[0]

    # Precompute candidate embeddings
    vecs = {
        c["chunk_id"]: model.encode(
            [chunks[c["chunk_id"]]["text"]],
            normalize_embeddings=True
        )[0]
        for c in candidates
    }

    selected = []
    selected_ids = []

    while len(selected) < k and candidates:
        best, best_score = None, -1e9

        for c in candidates:
            cid = c["chunk_id"]

            sim_query = np.dot(qvec, vecs[cid])
            sim_selected = (
                max(np.dot(vecs[cid], vecs[sid]) for sid in selected_ids)
                if selected_ids else 0
            )

            score = lambda_ * sim_query - (1 - lambda_) * sim_selected

            if score > best_score:
                best, best_score = c, score

        selected.append(best)
        selected_ids.append(best["chunk_id"])
        candidates = [c for c in candidates if c["chunk_id"] != best["chunk_id"]]

    return selected
