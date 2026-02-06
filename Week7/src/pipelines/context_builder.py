import json
from src.retriever.hybrid_retriever import hybrid_retrieve
from src.retriever.reranker import rerank
from src.retriever.mmr import mmr

CHUNKS_FILE = "src/data/chunks/document_chunks.jsonl"

# Load chunks 
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]


def build_context(query, top_k=5):
    # Step 1: Hybrid Retrieval
    candidates = hybrid_retrieve(query, top_k=top_k * 2)

    # Step 2: Reranking
    reranked = rerank(query, candidates, chunks, top_k=top_k * 2)

    # Step 3: MMR (diversity)
    final_chunks = mmr(query, reranked, chunks, k=top_k)

    # Step 4: Format final context
    context = []
    for c in final_chunks:
        chunk = chunks[c["chunk_id"]]
        context.append({
            "chunk_id": c["chunk_id"],
            "text": chunk["text"],
            "metadata": chunk["metadata"]
        })

    return context


if __name__ == "__main__":
    query = input("Enter query: ").strip()

    context = build_context(query, top_k=5)

    print("\nFinal Context:\n")
    for c in context:
        print("Chunk ID:", c["chunk_id"])
        print("Metadata:", c["metadata"])
        print("Text:", c["text"][:300])
        print("-" * 50)
