import json
import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import tiktoken

# ==============================
# CONFIG
# ==============================

TRAIN_PATH = "data/processed/train.jsonl"
VAL_PATH = "data/processed/val.jsonl"
ANALYSIS_DIR = "analysis"

os.makedirs(ANALYSIS_DIR, exist_ok=True)

# same tokenizer family used earlier
tokenizer = tiktoken.get_encoding("cl100k_base")

# ==============================
# HELPERS
# ==============================

def load_jsonl(path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]


def count_tokens(row):
    text = f"{row['instruction']} {row['input']} {row['output']}"
    return len(tokenizer.encode(text))


def detect_task_type(instruction: str) -> str:
    inst = instruction.lower()
    if "extract" in inst:
        return "extraction"
    if "reason" in inst:
        return "reasoning"
    return "qa"


# ==============================
# MAIN ANALYSIS
# ==============================

def main():
    print("Loading processed data...")
    train_data = load_jsonl(TRAIN_PATH)
    val_data = load_jsonl(VAL_PATH)

    all_data = train_data + val_data

    print(f"Train samples: {len(train_data)}")
    print(f"Validation samples: {len(val_data)}")
    print(f"Total samples: {len(all_data)}")

    # ==============================
    # TOKEN LENGTH ANALYSIS
    # ==============================

    token_lengths = [count_tokens(row) for row in all_data]

    print("\nToken length statistics:")
    print(f"Min tokens : {int(np.min(token_lengths))}")
    print(f"Max tokens : {int(np.max(token_lengths))}")
    print(f"Mean tokens: {np.mean(token_lengths):.2f}")
    print(f"P95 tokens : {np.percentile(token_lengths, 95):.2f}")

    plt.figure(figsize=(8, 5))
    plt.hist(token_lengths, bins=40)
    plt.title("Token Length Distribution")
    plt.xlabel("Number of tokens")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"{ANALYSIS_DIR}/token_length_distribution.png")
    plt.close()

    # ==============================
    # TASK TYPE DISTRIBUTION
    # ==============================

    task_types = [detect_task_type(row["instruction"]) for row in all_data]
    task_counts = Counter(task_types)

    print("\nTask type distribution:")
    for k, v in task_counts.items():
        print(f"{k}: {v}")

    plt.figure(figsize=(6, 4))
    plt.bar(task_counts.keys(), task_counts.values())
    plt.title("QA / Reasoning / Extraction Distribution")
    plt.xlabel("Task type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"{ANALYSIS_DIR}/task_distribution.png")
    plt.close()

    # ==============================
    # INSTRUCTION DIVERSITY
    # ==============================

    unique_instructions = set(row["instruction"] for row in all_data)
    print(f"\nUnique instruction templates: {len(unique_instructions)}")

    print("\nAnalysis complete ")
    print("Saved plots:")
    print(f"- {ANALYSIS_DIR}/token_length_distribution.png")
    print(f"- {ANALYSIS_DIR}/task_distribution.png")


if __name__ == "__main__":
    main()
