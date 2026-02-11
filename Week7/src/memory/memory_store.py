import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path("CHAT-LOGS.json")
MAX_TURNS = 5


def load_memory():
    if not MEMORY_FILE.exists():
        return []
    return json.loads(MEMORY_FILE.read_text())


def save_memory(memory):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))


def add_message(role, content):
    memory = load_memory()
    memory.append({
        "time": datetime.utcnow().isoformat(),
        "role": role,
        "content": content
    })
    save_memory(memory[-MAX_TURNS:])


def get_memory():
    return load_memory()
