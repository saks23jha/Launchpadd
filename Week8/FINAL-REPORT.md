# FINAL REPORT — Week 8
**Launchpad Program**

## Overview
This report summarises the complete Week 8 journey of building, fine-tuning, quantising and deploying a local LLM API using TinyLlama.

## Day 1 — Environment Setup
- Set up Google Colab with T4 GPU
- Installed all required libraries — transformers, peft, bitsandbytes, accelerate
- Loaded TinyLlama/TinyLlama-1.1B-Chat-v1.0 base model
- Verified GPU availability and model loading

## Day 2 — QLoRA Fine-tuning
- Dataset: ChatDoctor-HealthCareMagic-100k (500 examples)
- Fine-tuned TinyLlama using QLoRA (4-bit quantisation)
- Trainable parameters: 0.4% of total parameters
- Training loss reduced from 2.71 to 2.18
- Saved LoRA adapters to /adapters/

## Day 3 — Quantisation
- Merged Day 2 LoRA adapters with base model
- Converted to 4 formats:
  - FP16: 2.2GB (baseline)
  - INT8: 1.24GB (44% smaller)
  - INT4: 0.81GB (63% smaller)
  - GGUF: 1.17GB (47% smaller)
- Best quantised model: INT4 (smallest size, good quality)
- GGUF best for CPU/local deployment

## Day 4 — Inference Benchmarking
- Tested all 3 models — Base, Fine-tuned, GGUF
- Measured Tokens/sec, VRAM, Latency, Accuracy

### Benchmark Results (Colab — T4 GPU)
- Base Model: Latency 5.26s | Tokens/sec 19.01 | VRAM 6.62GB
- Fine-tuned Model: Latency 2.86s | Tokens/sec 34.97 | VRAM 6.62GB
- GGUF Model: Latency 18.08s | Tokens/sec 5.53 | VRAM 0.0GB (CPU)

### Benchmark Results (Local — CPU only)
- Base Model: Latency 12.33s | Tokens/sec 8.11 | VRAM 0.0GB
- Fine-tuned Model: Latency 11.82s | Tokens/sec 8.46 | VRAM 0.0GB
- GGUF Model: Latency 4.0s | Tokens/sec 25.0 | VRAM 0.0GB

- Implemented Streaming output mode
- Implemented Batch inference
- Implemented Multi-prompt test

## Day 5 — Capstone: Local LLM API
- Built FastAPI server with 2 endpoints:
  - POST /generate — single response generation
  - POST /chat — infinite chat mode with history
- Features implemented:
  - Uses quantised GGUF model
  - Infinite chat mode
  - System + user prompts
  - Top-k, top-p, temperature controls
  - Logs + request id
  - Medical keyword filter
  - Ready for RAG / Agents
- Built Streamlit UI for chatting with the model
- Tested on both FastAPI Swagger UI and Streamlit UI
- Dockerized the application

## Key Learnings
- QLoRA allows fine-tuning large models with very few resources
- Quantisation reduces model size by up to 63% with minimal quality loss
- GGUF format is best for local CPU deployment
- Fine-tuned model is faster than base model on GPU
- FastAPI makes it easy to deploy LLMs as microservices
- Streamlit makes it easy to build UI for LLMs

## Conclusion
Successfully built an end-to-end LLM pipeline:
- Fine-tuned TinyLlama on medical data 
- Quantised to GGUF format 
- Benchmarked inference performance 
- Deployed as local FastAPI microservice 
- Built Streamlit UI 
- Dockerized the application 

