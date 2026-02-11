import json
from pathlib import Path
from PIL import Image
import pytesseract
from transformers import BlipProcessor, BlipForConditionalGeneration

# Paths
IMAGE_DIR = Path("src/data/images")
OUTPUT_DIR = Path("src/data/images/processed")
OUTPUT_FILE = OUTPUT_DIR / "image_metadata.jsonl"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load BLIP captioning model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

def generate_caption(image):
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs, max_length=50)
    return processor.decode(out[0], skip_special_tokens=True)

def run_ingestion():
    records = []

    images = list(IMAGE_DIR.glob("*.png")) + list(IMAGE_DIR.glob("*.jpeg")) + list(IMAGE_DIR.glob("*.jpg"))

    if not images:
        raise ValueError("No images found in src/data/images/")

    for img_path in images:
        image = Image.open(img_path).convert("RGB")

        # OCR
        ocr_text = pytesseract.image_to_string(image).strip()

        # Caption
        caption = generate_caption(image)

        record = {
            "image_id": img_path.name,
            "image_path": str(img_path),
            "ocr_text": ocr_text,
            "caption": caption
        }

        records.append(record)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print(f"Ingested {len(records)} images")

if __name__ == "__main__":
    run_ingestion()
