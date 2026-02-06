from pathlib import Path
import json
import pickle
import numpy as np
import faiss

EMBEDDINGS_FILE = Path("src/data/embeddings/embeddings.jsonl")
INDEX_DIR = Path("src/data/index")
INDEX_FILE = INDEX_DIR / "faiss.index"
META_FILE = INDEX_DIR / "metadata.pkl"


def run_indexing():
    vectors = []
    metadata = []

    with open(EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            vectors.append(obj["embedding"])
            metadata.append(obj["metadata"])

    vectors = np.array(vectors, dtype="float32")

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_FILE))

    with open(META_FILE, "wb") as f:
        pickle.dump(metadata, f)

    print(f"FAISS index built with {index.ntotal} vectors")


if __name__ == "__main__":
    run_indexing()
