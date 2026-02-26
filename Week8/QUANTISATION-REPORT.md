report = f"""# QUANTISATION REPORT — Day 3
**Week 8 | Launchpad Program**

## Model Details
- Base Model: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- Fine-tuned with Day 2 LoRA adapters (merged before quantisation)
- Dataset: ChatDoctor-HealthCareMagic-100k (500 examples)

## What is Quantisation?
Quantisation reduces model size by storing weights in lower precision formats.
This saves memory and speeds up inference with minimal quality loss.
It is applied after training — no retraining needed.

## Post-Training Quantisation
- Static Quantisation: scale factors are fixed before inference (faster)
- Dynamic Quantisation: scale factors computed during inference (more accurate)

## FP16 vs INT8 vs INT4
- FP16: 16-bit floating point — highest precision, largest size, baseline
- INT8: 8-bit integer — good balance of size and quality
- INT4: 4-bit integer — smallest size, fastest, best for deployment

## llama.cpp & GGUF
- GGUF is a format designed for llama.cpp
- Optimized for CPU inference — no GPU needed
- Converted using convert_hf_to_gguf.py with q8_0 quantisation
- Best for local machines and edge devices

## Size & Speed Results
| Format | Size (GB) | Speed (s) |
|--------|-----------|-----------|
| FP16   | 2.2       | 5.34      |
| INT8   | 1.24      | 8.94      |
| INT4   | 0.81      | 3.48      |
| GGUF   | 1.17      | 1.48      |

## Quality (Actual Responses to Patient Query)
Prompt: "I have been feeling very thirsty and urinating frequently. What could be wrong?"

FP16:
Hi! Thanks for asking Chat Doctor. I understand your concern. Thirst is one of the 
most common symptoms in dehydration. It can happen due to various reasons like low 
blood volume or electrolyte imbalance. If it persists then there may be an underlying 
problem which needs further investigation by a healthcare professional.

INT8:
Hi! Thanks for asking Chat Doctor. I understand your concern. You may need to take 
some medications like water pills or diuretics if you feel that there is an excessive 
amount of fluid in body. This can help reduce symptoms such as frequent urination 
and increased thirst.

INT4:
Hi! Thanks for your question in Chat Doctor. I can understand your concern regarding 
frequent urination and thirstiness. It is common to experience these symptoms when 
we are dehydrated or under stress. If it persists over several days then consult 
with your physician as there may be some underlying cause that needs attention.

GGUF:
It is possible that you have been suffering from urinary tract infection (UTI) or 
kidney stone. You are having frequent urination and painful urine stream, which 
could be due to this reason. Make sure that your condition is normal by doing some 
physical examinations.

## Key Observations
- INT4 is the best quantised model — smallest size (0.81GB), fast (3.48s), good quality
- FP16 gives best quality but is largest (2.2GB)
- GGUF is best for CPU/local deployment — no GPU needed
- Fine-tuning from Day 2 is visible in responses — ChatDoctor style preserved
- Quantisation did not significantly reduce response quality

## Conclusion
INT4 is the best overall quantised model for GPU deployment.
GGUF is the best choice for CPU/local deployment.
Both achieve significant size reduction while maintaining good response quality.

