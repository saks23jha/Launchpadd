import pickle
from pathlib import Path

import faiss
import torch
from PIL import Image
import pytesseract
from transformers import CLIPModel, CLIPProcessor

# ------------------ PATHS ------------------
INDEX_FILE = Path("src/data/images/index/image_faiss.index")
META_FILE = Path("src/data/images/index/image_metadata.pkl")

device = "cuda" if torch.cuda.is_available() else "cpu"

# ------------------ LOAD MODELS ------------------
model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
).to(device)

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

# ------------------ LOAD INDEX ------------------
index = faiss.read_index(str(INDEX_FILE))

with open(META_FILE, "rb") as f:
    metadata = pickle.load(f)


# =================================================
# MODE 1: TEXT → IMAGE
# =================================================
def text_to_image(query, top_k=5):
    inputs = processor(text=[query], return_tensors="pt", padding=True).to(device)

    with torch.no_grad():
        text_out = model.text_model(**inputs)
        text_emb = model.text_projection(text_out.pooler_output)

    text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)

    scores, indices = index.search(
        text_emb.cpu().numpy().astype("float32"), top_k
    )

    return scores[0], indices[0]


# =================================================
# MODE 2: IMAGE → IMAGE
# =================================================
def image_to_image(image_path, top_k=5):
    image = Image.open(image_path).convert("RGB")

    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        vision_out = model.vision_model(pixel_values=inputs["pixel_values"])
        image_emb = model.visual_projection(vision_out.pooler_output)

    image_emb = image_emb / image_emb.norm(dim=-1, keepdim=True)

    scores, indices = index.search(
        image_emb.cpu().numpy().astype("float32"), top_k
    )

    return scores[0], indices[0]


# =================================================
# MODE 3: IMAGE → TEXT
# =================================================
def image_to_text(image_path):
    image = Image.open(image_path).convert("RGB")

    # ocr_text = pytesseract.image_to_string(image)
    ocr_text = next(
    (m["ocr_text"] for m in metadata if m["image_path"] == image_path),
    "No OCR text available"
)


    caption = next(
        (m["caption"] for m in metadata if m["image_path"] == image_path),
        "No caption available"
    )

    return caption, ocr_text


# =================================================
# CLI
# =================================================
if __name__ == "__main__":
    print("\nImage-RAG Query Engine\n")
    print("1 → Text to Image")
    print("2 → Image to Image")
    print("3 → Image to Text")

    choice = input("\nSelect mode (1 / 2 / 3): ").strip()

    if choice == "1":
        query = input("Enter text query: ").strip()
        scores, idxs = text_to_image(query)

        print("\nRetrieved Images:\n")
        for i, (idx, score) in enumerate(zip(idxs, scores), 1):
            item = metadata[idx]
            print(f"Result {i}")
            print("Image:", item["image_path"])
            print("Score:", float(score))
            print("Caption:", item["caption"])
            print("OCR Text:", item["ocr_text"][:200])
            print("-" * 50)

    elif choice == "2":
        path = input("Enter image path: ").strip()
        scores, idxs = image_to_image(path)

        print("\nSimilar Images:\n")
        for i, (idx, score) in enumerate(zip(idxs, scores), 1):
            item = metadata[idx]
            print(f"Result {i}")
            print("Image:", item["image_path"])
            print("Score:", float(score))
            print("Caption:", item["caption"])
            print("-" * 50)

    elif choice == "3":
        path = input("Enter image path: ").strip()
        caption, ocr_text = image_to_text(path)

        print("\nImage Explanation:\n")
        print("Caption:")
        print(caption)
        print("\nOCR Text:")
        print(ocr_text[:500])

    else:
        print("Invalid choice")
    __all__ = [
    "text_to_image",
    "image_to_image",
    "image_to_text"
]
