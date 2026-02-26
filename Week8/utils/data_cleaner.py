import json
import os
import random
import re
import numpy as np

# ==============================
# CONFIG
# ==============================

RAW_PATH = "data/raw/healthcare_raw.jsonl"
OUT_DIR = "data/processed"

TRAIN_PATH = os.path.join(OUT_DIR, "train.jsonl")
VAL_PATH = os.path.join(OUT_DIR, "val.jsonl")

TRAIN_RATIO = 0.8
SEED = 42

# cleaning + outlier rules
MIN_CHARS = 50
MAX_CHARS = 3000
IQR_MULTIPLIER = 1.5

# task ratios
QA_RATIO = 0.6
REASONING_RATIO = 0.25
EXTRACTION_RATIO = 0.15

random.seed(SEED)

# ==============================
# HELPERS
# ==============================

def load_jsonl(path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]

def save_jsonl(data, path):
    with open(path, "w") as f:
        for row in data:
            f.write(json.dumps(row) + "\n")

def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_simple_entities(text: str) -> dict:
    """
    VERY simple synthetic extraction
    (exercise-focused, not medical diagnosis)
    """
    symptoms = []
    common_symptoms = [
        "fever", "headache", "cough", "pain",
        "nausea", "vomiting", "dizziness",
        "fatigue", "shortness of breath"
    ]

    for s in common_symptoms:
        if s in text.lower():
            symptoms.append(s)

    duration_match = re.search(r"\b(\d+)\s*(day|days|week|weeks|month|months)\b", text.lower())
    duration = duration_match.group(0) if duration_match else "unknown"

    return {
        "symptoms": symptoms,
        "duration": duration
    }

# ==============================
# MAIN
# ==============================

def main():
    print("Loading raw data...")
    raw_data = load_jsonl(RAW_PATH)
    print("Raw samples:", len(raw_data))

    cleaned = []

    # -------- STEP 1: BASIC CLEANING --------
    for row in raw_data:
        if not row.get("instruction") or not row.get("input") or not row.get("output"):
            continue

        instruction = clean_text(row["instruction"])
        input_text = clean_text(row["input"])
        output_text = clean_text(row["output"])

        total_len = len(instruction) + len(input_text) + len(output_text)

        if total_len < MIN_CHARS or total_len > MAX_CHARS:
            continue

        cleaned.append({
            "instruction": instruction,
            "input": input_text,
            "output": output_text,
            "char_length": total_len
        })

    print("After basic cleaning:", len(cleaned))

    # -------- STEP 2: OUTLIER REMOVAL (IQR) --------
    lengths = np.array([x["char_length"] for x in cleaned])

    q1, q3 = np.percentile(lengths, [25, 75])
    iqr = q3 - q1

    lower = q1 - IQR_MULTIPLIER * iqr
    upper = q3 + IQR_MULTIPLIER * iqr

    filtered = [x for x in cleaned if lower <= x["char_length"] <= upper]
    print("After outlier removal:", len(filtered))

    # -------- STEP 3: CREATE 3 TASK TYPES --------
    final_data = []
    task_stats = {"qa": 0, "reasoning": 0, "extraction": 0}

    for row in filtered:
        r = random.random()

        if r < QA_RATIO:
            # QA
            final_data.append({
                "instruction": "Answer the healthcare question clearly.",
                "input": row["input"],
                "output": row["output"]
            })
            task_stats["qa"] += 1

        elif r < QA_RATIO + REASONING_RATIO:
            # Reasoning
            final_data.append({
                "instruction": "Explain the reasoning behind the healthcare response.",
                "input": row["input"],
                "output": row["output"]
            })
            task_stats["reasoning"] += 1

        else:
            # Extraction
            extracted = extract_simple_entities(row["input"])
            final_data.append({
                "instruction": "Extract key clinical information from the text.",
                "input": row["input"],
                "output": json.dumps(extracted)
            })
            task_stats["extraction"] += 1

    print("Task distribution:", task_stats)

    # -------- STEP 4: TRAIN / VAL SPLIT --------
    random.shuffle(final_data)
    split_idx = int(len(final_data) * TRAIN_RATIO)

    train_data = final_data[:split_idx]
    val_data = final_data[split_idx:]

    os.makedirs(OUT_DIR, exist_ok=True)

    save_jsonl(train_data, TRAIN_PATH)
    save_jsonl(val_data, VAL_PATH)

    print("Train samples:", len(train_data))
    print("Validation samples:", len(val_data))
    print("FULL 3-TYPE DATA CLEANING PIPELINE DONE ")


if __name__ == "__main__":
    main()
