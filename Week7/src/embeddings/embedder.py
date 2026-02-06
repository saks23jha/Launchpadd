from pathlib import Path
import json
from sentence_transformers import SentenceTransformer

# Paths
CHUNKS_FILE = Path("src/data/chunks/document_chunks.jsonl")
EMBEDDINGS_DIR = Path("src/data/embeddings")
OUTPUT_FILE = EMBEDDINGS_DIR / "embeddings.jsonl"

# Local BGE-small model
model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def run_embedding():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError("Chunks not found. Run ingestion first.")

    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    texts = []
    metadata_list = []

    # load chunks and metadata
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            texts.append(obj["text"])
            metadata_list.append(obj["metadata"])

    print(f"🔹 Generating embeddings for {len(texts)} chunks")

    # Generated local embeddings
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,   # IMPORTANT for BGE
        show_progress_bar=True
    )

    # Save embeddings
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for meta, emb in zip(metadata_list, embeddings):
            f.write(json.dumps({
                "embedding": emb.tolist(),
                "metadata": meta
            }) + "\n")

    print(" Local embeddings generated and saved successfully")


if __name__ == "__main__":
    run_embedding()
