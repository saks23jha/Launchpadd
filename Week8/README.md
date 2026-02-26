# Week 8 — Local LLM API: Medical Assistant

## Overview
A local LLM API built using TinyLlama fine-tuned on ChatDoctor dataset.
Deployed as a FastAPI server with a Streamlit UI.

## Project Structure
```
Week8/
├── deploy/
│   ├── app.py           # FastAPI server with /generate and /chat endpoints
│   ├── model_loader.py  # Loads and caches GGUF model
│   ├── config.py        # All settings and configurations
│   └── streamlit_app.py # Streamlit UI
├── quantised/
│   └── model.gguf       # Quantised GGUF model
├── README.md
├── DOCKERFILE
└── FINAL-REPORT.md
```

## Setup

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install fastapi uvicorn llama-cpp-python streamlit requests pydantic
```

### 3. Run FastAPI server
```bash
python deploy/app.py
```
Server runs at: http://localhost:8000

### 4. Run Streamlit UI
```bash
streamlit run deploy/streamlit_app.py
```
UI runs at: http://localhost:8501

## API Endpoints

### POST /generate
Single response generation.
```json
{
  "prompt": "I have a headache and fever. What should I do?",
  "max_tokens": 200,
  "temperature": 0.7,
  "top_k": 40,
  "top_p": 0.95
}
```

### POST /chat
Chat with memory (infinite chat mode).
```json
{
  "message": "I have a headache and fever. What should I do?",
  "history": [],
  "max_tokens": 200,
  "temperature": 0.7,
  "top_k": 40,
  "top_p": 0.95
}
```

## Features
- Uses quantised GGUF model — no GPU needed
- Infinite chat mode with conversation history
- System + user prompts
- Top-k, top-p, temperature controls
- Logs + request id for every request
- Medical keyword filter — only answers medical questions
- Ready for RAG / Agents

## Model Details
- Base Model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- Fine-tuned on: ChatDoctor-HealthCareMagic-100k (500 examples)
- Quantised to: GGUF (q8_0) via llama.cpp

## API Docs
FastAPI Swagger UI available at:
```
http://localhost:8000/docs
```