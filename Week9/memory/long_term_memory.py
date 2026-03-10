import os
import sqlite3
from datetime import datetime


class LongTermMemory:
    """
    Persistent Memory using SQLite

    Responsibilities:
    - Store important facts
    - Retrieve stored facts
    - Maintain persistent knowledge
    """

    def __init__(self, db_path="memory/long_term.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize_database()

    # -------------------------
    # Initialize Database
    # -------------------------
    def _initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            content   TEXT NOT NULL,
            category  TEXT DEFAULT 'general',
            timestamp TEXT
        )
        """)

        conn.commit()
        conn.close()
        print("[LONG TERM MEMORY] Database ready.")

    # -------------------------
    # Store Memory
    # -------------------------
    def store(self, content: str, category: str = "general"):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO memories (content, category, timestamp) VALUES (?, ?, ?)",
                (content, category, datetime.now().isoformat())
            )

            conn.commit()
            conn.close()
            print(f"[LONG TERM MEMORY] Stored: {content[:50]}...")

        except Exception as e:
            print(f"[LONG TERM MEMORY] Failed to store: {e}")

    # -------------------------
    # Retrieve All Memories
    # -------------------------
    def retrieve_all(self) -> list:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT content FROM memories ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            conn.close()

            return [row[0] for row in rows]

        except Exception as e:
            print(f"[LONG TERM MEMORY] Failed to retrieve: {e}")
            return []

    # -------------------------
    # Retrieve by Category
    # -------------------------
    def retrieve_by_category(self, category: str) -> list:
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT content FROM memories WHERE category = ? ORDER BY timestamp DESC",
                (category,)
            )
            rows = cursor.fetchall()
            conn.close()

            return [row[0] for row in rows]

        except Exception as e:
            print(f"[LONG TERM MEMORY] Failed to retrieve by category: {e}")
            return []

    # -------------------------
    # Clear All Memories
    # -------------------------
    def clear(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories")
            conn.commit()
            conn.close()
            print("[LONG TERM MEMORY] All memories cleared.")

        except Exception as e:
            print(f"[LONG TERM MEMORY] Failed to clear: {e}")