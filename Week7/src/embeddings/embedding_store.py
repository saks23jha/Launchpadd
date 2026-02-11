import os
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# -------- PATHS --------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHUNKS_PATH = os.path.join(
    BASE_DIR, "data", "chunks", "document_chunks.jsonl"
)

EMBEDDINGS_PATH = os.path.join(
    BASE_DIR, "data", "embeddings", "embeddings.jsonl"
)

TOP_K = 3
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# -------- LOADERS --------
def load_chunks():
    chunks = []
    with open(CHUNKS_PATH, "r") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))
    return chunks


def load_embeddings():
    embeddings = []
    with open(EMBEDDINGS_PATH, "r") as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                vector = (
                    obj.get("embedding")
                    or obj.get("embeddings")
                    or obj.get("vector")
                    or obj.get("values")
                )
                embeddings.append(vector)
    return np.array(embeddings)


def embed_query(query: str):
    return model.encode([query])


# retrieval
def retrieve_context(query: str):
    chunks = load_chunks()
    vectors = load_embeddings()

    texts = [c["text"] for c in chunks]

    query_vector = embed_query(query)
    scores = cosine_similarity(query_vector, vectors)[0]

    top_indices = scores.argsort()[-TOP_K:][::-1]

    return [texts[i] for i in top_indices]
