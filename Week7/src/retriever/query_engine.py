import pickle
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Paths
INDEX_FILE = Path("src/data/index/faiss.index")
META_FILE = Path("src/data/index/metadata.pkl")

# Load embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def query_engine(query, top_k=5):
    # Load FAISS index
    index = faiss.read_index(str(INDEX_FILE))

    # Load metadata
    with open(META_FILE, "rb") as f:
        metadata = pickle.load(f)

    # Embed query
    query_vector = model.encode(
        [query],
        normalize_embeddings=True
    ).astype("float32")

    # Search FAISS
    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx, score in zip(indices[0], distances[0]):
        results.append({
            "chunk_id": metadata[idx]["chunk_id"],
            "source": metadata[idx]["source"],
            "score": float(score)
        })

    return results


if __name__ == "__main__":
    print("FAISS Query Engine (type 'exit' to quit)\n")

    while True:
        query = input("Enter your query: ").strip()

        if query.lower() in {"exit", "quit"}:
            break

        results = query_engine(query, top_k=5)

        print("\nResults:")
        for r in results:
            print(
                f"chunk_id: {r['chunk_id']}, "
                f"source: {r['source']}, "
                f"score: {r['score']}"
            )
        print("-" * 40)
