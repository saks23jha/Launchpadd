# RAG Architecture – Week 7 Day 1

## Introduction
Week 7 – Day 1 is focused on building the **foundation of a Retrieval-Augmented Generation (RAG) system**.  
Instead of directly answering questions, the goal of this day is to ensure that the system can **reliably retrieve the most relevant information** from a given document when a user asks a query.

In a RAG system, retrieval and generation are **two separate responsibilities**:
- **Retriever** → finds relevant information
- **Generator (LLM)** → forms a natural language answer

This day is entirely dedicated to the **Retriever pipeline**.

---

## Objective
The objectives of Week 7 – Day 1 are:

- Load and process a raw document (`annual.pdf`)
- Convert the document into manageable text chunks
- Attach meaningful metadata to each chunk
- Generate **local embeddings** for every chunk
- Store embeddings in a **vector database (FAISS)**
- Build a retriever that maps a query to relevant chunks

> **Note:**  
> Answer generation using an LLM is **intentionally excluded** and will be handled in Week 7 – Day 2.

---

## High-Level RAG Flow (Day 1 Scope)

```text
annual.pdf
   ↓
PDF Text Extraction
   ↓
Text Chunking
   ↓
Metadata Enrichment
   ↓
Local Embedding Generation (BGE-small)
   ↓
Vector Storage (FAISS)
   ↓
Retriever (Query → Relevant Chunk IDs)
