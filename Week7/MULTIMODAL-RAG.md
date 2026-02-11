# Multimodal RAG – Week 7 Day 3 (Image-RAG)

## Objective
The objective of **Week 7 – Day 3** was to extend the previously built **text-based RAG system** into a **Multimodal RAG (Image-RAG)** pipeline.  
The goal was to enable the system to **understand, retrieve, and explain images**, in addition to handling text documents.

## Why Multimodal RAG?
Traditional RAG systems work only on text data. However, many real-world documents such as:
- Annual reports
- Scientific papers
- Engineering documents

contain **important information in images**, including:
- Charts
- Tables
- Diagrams
- Infographics

Multimodal RAG allows the system to:
- Retrieve relevant images using text queries
- Find visually similar images
- Explain image content in natural language

---

## Multimodal RAG Architecture (Day 3 Scope)

```text
Images (PNG / JPEG)
   ↓
Image Ingestion Pipeline
   ↓
OCR + Image Captioning
   ↓
CLIP Image Embeddings
   ↓
Image FAISS Vector Store
   ↓
Multimodal Query Engine
   ├── Text → Image
   ├── Image → Image
   └── Image → Text
