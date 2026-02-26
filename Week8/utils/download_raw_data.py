from datasets import load_dataset
import os

dataset = load_dataset(
    "lavita/ChatDoctor-HealthCareMagic-100k",
    split="train"
)

print("Total rows in original dataset:", len(dataset))

dataset = dataset.shuffle(seed=42)
dataset_1200 = dataset.select(range(1200))

print("Rows after sampling:", len(dataset_1200))

os.makedirs("data/raw", exist_ok=True)

dataset_1200.to_json(
    "data/raw/healthcare_raw.jsonl",
    orient="records",
    lines=True
)

print("Saved to data/raw/healthcare_raw.jsonl")
