report = """# BENCHMARK REPORT — Day 4
**Week 8 | Launchpad Program**

## Overview
Day 4 focuses on Inference Optimisation and Benchmarking.
We tested 3 models and measured their performance on key metrics.

## Models Tested
1. Base Model — TinyLlama/TinyLlama-1.1B-Chat-v1.0 (no fine-tuning)
2. Fine-tuned Model — TinyLlama + Day 2 ChatDoctor LoRA adapters (merged)
3. Quantised Model — GGUF (q8_0) running via llama.cpp on CPU

## Benchmark Results (Colab — T4 GPU)
- Base Model: Latency 5.26s | Tokens/sec 19.01 | VRAM 6.62GB
- Fine-tuned Model: Latency 2.86s | Tokens/sec 34.97 | VRAM 6.62GB
- GGUF Model: Latency 18.08s | Tokens/sec 5.53 | VRAM 0.0GB (CPU)

## Benchmark Results (Local VS Code — CPU only)
- Base Model: Latency 12.33s | Tokens/sec 8.11 | VRAM 0.0GB
- Fine-tuned Model: Latency 11.82s | Tokens/sec 8.46 | VRAM 0.0GB
- GGUF Model: Latency 4.0s | Tokens/sec 25.0 | VRAM 0.0GB


## Accuracy (Actual Responses)
**Prompt:** I have been feeling very thirsty and urinating frequently. What could be wrong?

**Base Model:**
It sounds like your body is trying to tell you that there may be an issue with hydration or bladder functioning. Dehydration can lead to frequent urination due to excessive fluid loss from the kidneys.

**Fine-tuned Model:**
Hi! Thanks for your question on Chat Doctor. I understand the concern you have raised. You may be suffering from a urinary tract infection (UTI). This can cause frequent urination, fever or chills, nausea/vomiting, painful urination, dizziness, headache, fatigue, weakness, muscle aches.

**GGUF Model:**
Several possible reasons could be causing your thirst and urinating frequently: 1. Dehydration 2. Kidney stones - A buildup in your kidneys that causes them to work harder than normal may also lead to frequent urination.

## Streaming Output
- Implemented for all 3 models
- Tokens appear word by word in real time — just like ChatGPT
- Fine-tuned model streams in ChatDoctor style 
- GGUF streaming works via llama-cpp-python stream=True 

## Batch Inference
| Model | Batch Time (Colab) | Batch Time (Local) |
|-------|-------------------|-------------------|
| Base Model | 2.25s | 10.77s |
| Fine-tuned Model | 1.39s | 9.92s |
| GGUF Model | 51.34s | 5.3s |

## Multi-prompt Test
- Tested all 3 models on 5 different medical questions
- Questions: insulin, cholesterol, blood sugar, heart attack, stress
- GGUF gave most detailed and relevant responses 
- Fine-tuned model showed ChatDoctor style in responses 

## Key Observations
- Fine-tuned model is fastest on GPU (34.97 tokens/sec) 
- GGUF is fastest on CPU (25.0 tokens/sec) 
- Fine-tuned model shows ChatDoctor style from Day 2 training 
- GPU inference is 3-4x faster than CPU inference
- GGUF performs better on CPU than HuggingFace models

## Conclusion
- Fine-tuned model is best for GPU deployment (fastest, best quality)
- GGUF model is best for CPU/local deployment (no GPU needed)
- Fine-tuning improved both speed and response quality
- All 3 models successfully tested on both Colab and local machine 
