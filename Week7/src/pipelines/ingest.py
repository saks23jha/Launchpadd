from pathlib import Path
import json
import re
from pypdf import PdfReader
from transformers import AutoTokenizer

# Paths
RAW_DIR = Path("src/data/raw")
CHUNKS_DIR = Path("src/data/chunks")
PDF_PATH = RAW_DIR / "annual.pdf"
OUTPUT_FILE = CHUNKS_DIR / "document_chunks.jsonl"

# Load tokenizer for BGE-small
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-small-en")


def clean_text(text: str) -> str:
    """
    Clean PDF extraction artifacts.
    """

    # remove dotted leaders from tables of contents
    text = re.sub(r"\.{3,}", " ", text)

    # remove section markers like ##5, ##4b etc
    text = re.sub(r"##\w+", " ", text)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def chunk_text(text: str, chunk_size=450, overlap=80):
    """
    Token-based chunking using BGE tokenizer.
    """

    tokens = tokenizer.encode(text, add_special_tokens=False)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size

        chunk_tokens = tokens[start:end]

        chunk = tokenizer.decode(chunk_tokens, skip_special_tokens=True)

        chunks.append(chunk)

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

            # clean PDF formatting artifacts
            text = clean_text(text)

            chunks = chunk_text(text)

            for chunk in chunks:

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