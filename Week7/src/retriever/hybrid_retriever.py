import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

# Paths
INDEX_FILE = Path("src/data/index/faiss.index")
CHUNKS_FILE = Path("src/data/chunks/document_chunks.jsonl")

# Load models
embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")
index = faiss.read_index(str(INDEX_FILE))

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]

texts = [c["text"] for c in chunks]
bm25 = BM25Okapi([t.lower().split() for t in texts])


# Metadata filter 
def apply_filters(chunk, filters):
    for k, v in filters.items():
        if chunk["metadata"].get(k) != v:
            return False
    return True

#semantic search (faiss)
def semantic_search(query, top_k, filters=None):
    qvec = embedder.encode([query], normalize_embeddings=True).astype("float32")
    dists, idxs = index.search(qvec, top_k)

    results = []
    for i, d in zip(idxs[0], dists[0]):
        if filters and not apply_filters(chunks[i], filters):
            continue
        results.append({
            "chunk_id": int(i),
            "score": float(d),
            "source": "semantic"
        })
    return results

#keyword search(BM25)
def keyword_search(query, top_k, filters=None):
    scores = bm25.get_scores(query.lower().split())
    top_idxs = np.argsort(scores)[::-1][:top_k]

    results = []
    for i in top_idxs:
        if filters and not apply_filters(chunks[i], filters):
            continue
        results.append({
            "chunk_id": int(i),
            "score": float(scores[i]),
            "source": "keyword"
        })
    return results

#dedupllication
def deduplicate(results):
    deduped = {}

    for r in results:
        cid = r["chunk_id"]
        entry = deduped.setdefault(
            cid, {"chunk_id": cid, "scores": {}, "sources": []}
        )
        entry["scores"][r["source"]] = r["score"]
        entry["sources"].append(r["source"])

    return list(deduped.values())


def hybrid_retrieve(query, top_k=5, filters=None):
    results = (
        semantic_search(query, top_k, filters)
        + keyword_search(query, top_k, filters)
    )
    return deduplicate(results)


if __name__ == "__main__":
    query = input("Enter query: ").strip()

    filters = {
        "year": "2024",
        "type": "policy"
    }

    print("\nDeduplicated Hybrid Results:\n")
    for r in hybrid_retrieve(query, top_k=5, filters=filters):
        print(r)
