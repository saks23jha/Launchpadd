import json
import pickle
from pathlib import Path

import faiss
import numpy as np
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

# Paths
METADATA_FILE = Path("src/data/images/processed/image_metadata.jsonl")
INDEX_DIR = Path("src/data/images/index")
INDEX_FILE = INDEX_DIR / "image_faiss.index"
META_FILE = INDEX_DIR / "image_metadata.pkl"

INDEX_DIR.mkdir(parents=True, exist_ok=True)

device = "cuda" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
).to(device)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

def run_clip_embedding():
    records = []
    vectors = []

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    for r in records:
        image = Image.open(r["image_path"]).convert("RGB")

        inputs = processor(images=image, return_tensors="pt")
        pixel_values = inputs["pixel_values"].to(device)

        with torch.no_grad():
            # Vision encoder ONLY
            vision_outputs = model.vision_model(pixel_values=pixel_values)
            pooled_output = vision_outputs.pooler_output

            # Apply CLIP projection head
            image_features = model.visual_projection(pooled_output)

        # Normalize
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        vectors.append(image_features.cpu().numpy()[0])

    vectors = np.array(vectors).astype("float32")

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    faiss.write_index(index, str(INDEX_FILE))

    with open(META_FILE, "wb") as f:
        pickle.dump(records, f)

    print(f"CLIP embeddings generated for {len(records)} images")

if __name__ == "__main__":
    run_clip_embedding()
