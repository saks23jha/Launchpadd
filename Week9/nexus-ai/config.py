import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from parent directory (Week9/.env)
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# -------------------------
# Model Configuration
# -------------------------
MODEL_NAME = "llama-3.1-8b-instant"
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = "https://api.groq.com/openai/v1"
TEMPERATURE = 0.3

MODEL_INFO = {
    "provider": "groq",
    "family": "llama",
    "context_length": 8192,
    "vision": False,
    "function_calling": False,
    "json_output": False,
    "structured_output": False,
}

# -------------------------
# Memory Configuration
# -------------------------
SESSION_MEMORY_WINDOW = 10
LONG_TERM_DB_PATH = "../memory/long_term.db"
FAISS_INDEX_PATH = "../memory/faiss.index"
FAISS_TEXTS_PATH = "../memory/faiss_texts.txt"

# -------------------------
# Tools Configuration
# -------------------------
SALES_CSV_PATH = "../data/sales.csv"
SQLITE_DB_PATH = "../data/sales.db"

# -------------------------
# Logs Configuration
# -------------------------
LOG_DIR = "logs"
LOG_FILE = "logs/nexus.log"

# -------------------------
# Agent Names
# -------------------------
AGENTS = [
    "orchestrator",
    "planner",
    "researcher",
    "coder",
    "analyst",
    "critic",
    "optimizer",
    "validator",
    "reporter",
]