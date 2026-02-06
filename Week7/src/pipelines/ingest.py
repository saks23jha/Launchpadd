from pathlib import Path
import json
from pypdf import PdfReader

RAW_DIR = Path("src/data/raw")
CHUNKS_DIR = Path("src/data/chunks")
PDF_PATH = RAW_DIR / "annual.pdf"
OUTPUT_FILE = CHUNKS_DIR / "document_chunks.jsonl"


def chunk_text(text, size=300, overlap=50):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap

    return chunks


def run_ingestion():
    if not PDF_PATH.exists():
        raise FileNotFoundError("annual.pdf not found in src/data/raw")

    reader = PdfReader(PDF_PATH)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    chunk_id = 0
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for page_no, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            for chunk in chunk_text(text):
                record = {
                    "text": chunk,
                    "metadata": {
                        "source": "annual.pdf",
                        "page": page_no,
                        "chunk_id": chunk_id
                    }
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                chunk_id += 1

    print(f"Ingestion done. Total chunks: {chunk_id}")


if __name__ == "__main__":
    run_ingestion()
