# Retrieval Strategies – Week 7 Day 2

This document summarizes the **retrieval layer** implemented on **Week 7 – Day 2** of the RAG pipeline.  
The focus was on improving **context quality**, not answer generation.

---

## Retrieval Flow


---

## 1. Hybrid Retrieval

- Uses **FAISS** for semantic search (dense embeddings)
- Uses **BM25** for keyword-based search
- Combines both to improve recall

---

## 2. Deduplication

- Removes duplicate chunks using `chunk_id`
- Tracks retrieval sources (semantic / keyword)

---

## 3. Reranking

- Reorders chunks using **cosine similarity**
- Uses BGE-small embeddings
- Improves precision by ranking truly relevant chunks higher

---

## 4. MMR (Max Marginal Relevance)

- Selects chunks that are **relevant and non-redundant**
- Balances relevance and diversity
- Prevents repeated or overlapping context

---

## 5. Context Builder

- Orchestrates retrieval, reranking, and MMR
- Produces final structured context:
  - chunk text
  - metadata
  - chunk ID

---
## Summary

Week 7 Day 2 delivers a **robust retrieval pipeline** that produces relevant, diverse, and clean context for downstream RAG answer generation.
