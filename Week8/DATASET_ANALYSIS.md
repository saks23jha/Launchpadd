# Day 1 – Dataset Analysis (Healthcare Domain)

## Objective
The objective of Day 1 is to **select a domain-specific dataset, analyze its structure, clean the data, and prepare train–validation splits** for future supervised fine-tuning.  

A **healthcare-focused dataset** was chosen to ensure domain relevance and meaningful instruction–response learning.

## Dataset Selection

### Domain
**Healthcare / Medical Question Answering**

### Source
The dataset was sourced from **Hugging Face Datasets**.  
It contains healthcare-related questions and expert-style responses covering symptoms, diagnosis, treatment, and general medical advice.

Since the original dataset is large, a controlled subset was selected for experimentation.


## Raw Dataset Handling

### Sampling Strategy
- The original dataset was randomly shuffled
- **1200 samples** were selected to ensure diversity
- Sampling was performed to keep experimentation manageable

### Raw Data Storage
The sampled raw dataset is stored at:data/raw/healthcare_raw.jsonl


Format: **JSON Lines (JSONL)**  
Each line represents a single healthcare instruction–response example.

---

## Data Schema
Each record follows an instruction-based schema:

```json
{
  "instruction": "Healthcare-related question or task",
  "input": "Optional medical context",
  "output": "Expected healthcare-related response"
}