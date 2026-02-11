# Deployment Notes – Day 5 (RAG Capstone)

## Overview
Day 5 integrates all previous tasks into a single **end-to-end Retrieval-Augmented Generation (RAG) system**.  
The system supports **text QA, image-based QA, and SQL-based QA**, along with memory, evaluation, and a user interface.

This capstone demonstrates how independent components from earlier days can be composed into a deployable system.

---

## Architecture Summary

The system is divided into three logical layers:

1. **Retrieval & Reasoning Layer**
2. **Application Layer (FastAPI endpoints)**
3. **User Interface Layer (Streamlit)**

Each endpoint corresponds directly to a previous day’s task.

---

## Endpoints Implemented

### 1. `/ask` – Text RAG (Day 2)
- Uses document embeddings created during Day 2
- Retrieves relevant chunks based on semantic similarity
- Generates a response using retrieved context
- Stores conversation history (last 5 messages)
- Evaluates answer faithfulness and confidence

**Purpose:**  
Demonstrates text-based RAG using embeddings.

---

### 2. `/ask-image` – Image RAG (Day 3)
- Uses image embeddings created during Day 3
- Supports:
  - Text → Image retrieval
  - Image explanation
- Returns similarity scores and explanations

**Purpose:**  
Demonstrates multimodal (vision + language) retrieval.

---

### 3. `/ask-sql` – SQL QA (Day 4)
- Converts natural language questions into SQL
- Executes queries on `sales.db`
- Returns tabular results (columns + rows)
- Matches Day 4 SQL QA behavior exactly

**Purpose:**  
Demonstrates structured data grounding via SQL.

---

## Memory Management

- Implemented using `CHAT-LOGS.json`
- Stores:
  - Timestamp
  - Role (`user` / `assistant`)
  - Content
- Retains last **5 conversation turns**
- Shared across all endpoints

---

## Evaluation Layer

Each response is evaluated using:
- **Faithfulness score**
- **Confidence score**
- **Hallucination detection**

Evaluation results are returned along with answers for transparency.

---

## User Interface (Streamlit)

- Streamlit UI acts as a frontend client
- Allows users to:
  - Ask text questions
  - Ask SQL questions
  - Interact with image-based queries
- Streamlit communicates directly with backend logic
- Designed for quick local testing and demo purposes


