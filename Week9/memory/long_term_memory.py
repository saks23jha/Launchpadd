import sqlite3
import os
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

        # create DB if it does not exist
        self._initialize_database()

    
    # Initialize Database

    def _initialize_database(self):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            timestamp TEXT
        )
        """)

        conn.commit()
        conn.close()

    
    # Store Memory
    
    def store(self, content: str):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO memories (content, timestamp) VALUES (?, ?)",
            (content, datetime.now().isoformat())
        )

        conn.commit()
        conn.close()

    
    # Retrieve Memories

    def retrieve_all(self):

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT content FROM memories")

        rows = cursor.fetchall()

        conn.close()

        return [row[0] for row in rows]