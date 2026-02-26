# TRAINING REPORT — Day 2: QLoRA Fine-Tuning
**Week 8 | Launchpad Program**

---

## 1. Objective
Fine-tune a Large Language Model (LLM) using QLoRA (Quantized Low-Rank Adaptation) on Google Colab T4 GPU while using memory-saving tricks like 4-bit loading, gradient checkpointing, and mixed precision training.

---

## 2. Environment
- Platform: Google Colab
- GPU: Tesla T4 (15.6 GB VRAM)
- Framework: PyTorch + HuggingFace Transformers + PEFT + TRL

---

## 3. Model
- **Base Model:** TinyLlama/TinyLlama-1.1B-Chat-v1.0
- **Total Parameters:** 1,104,553,984 (~1.1B)

---

## 4. Dataset
- **Dataset:** lavita/ChatDoctor-HealthCareMagic-100k
- **Examples Used:** 500 (subset)
- **Format:** Instruction / Input / output (medical Q&A)
- **Sample Format:**
```
### Instruction:
If you are a doctor, please answer the medical questions based on the patient's description.

### Input:
<patient question>

### output:
<doctor answer>
```

---

## 5. Hyperparameters
| Parameter | Value |
|-----------|-------|
| LoRA Rank (r) | 16 |
| Learning Rate (lr) | 2e-4 |
| Batch Size | 4 |
| Epochs | 3 |
| LoRA Alpha | 32 |
| LoRA Dropout | 0.05 |
| Quantization | 4-bit NF4 |
| Compute Dtype | bfloat16 |
| Optimizer | paged_adamw_8bit |
| LR Scheduler | cosine |
| Max Sequence Length | 512 |

---

## 6. Key Techniques Used

### 4-bit Loading (BitsAndBytes)
Loaded the model in 4-bit NF4 format using BitsAndBytesConfig. This reduced VRAM usage significantly, allowing a 1.1B model to train comfortably on a 15.6GB T4 GPU.

### LoRA (Low-Rank Adaptation)
Applied LoRA adapters to attention projection layers (q_proj, k_proj, v_proj, o_proj). Only the adapter matrices were trained, keeping the base model frozen.

### Gradient Checkpointing
Enabled via prepare_model_for_kbit_training() to save GPU memory during backpropagation by recomputing activations instead of storing them.

### Mixed Precision
Trained in bf16 to reduce memory usage and speed up computation.

---

## 7. Results

### Parameter Efficiency
| | Count | Percentage |
|--|-------|------------|
| Trainable Params | 4,505,600 | 0.4% |
| Frozen Params | 1,100,048,384 | 99.6% |
| Total Params | 1,104,553,984 | 100% |

Trainable params only ~1% confirmed!

### Training Loss
| Step | Loss |
|------|------|
| 10 | 2.714731 |
| 50 | 2.384622 |
| 100 | 2.347161 |
| 200 | 2.187923 |
| 300 | 2.192757 |
| 370 | 2.181947 |

Loss optimizing across all 3 epochs confirmed!

---

## 8. Saved Artifacts
| File | Description |
|------|-------------|
| adapter_model.safetensors | LoRA adapter weights |
| adapter_config.json | LoRA configuration |
| tokenizer.json | Tokenizer |
| tokenizer_config.json | Tokenizer config |
| chat_template.jinja | Chat template |

Adapter weights saved confirmed!


