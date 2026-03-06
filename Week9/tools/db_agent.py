import sqlite3


class DBAgent:
    """
    Database Agent

    Responsibilities:
    - Connect to SQLite database
    - Execute SQL queries
    - Return query results
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize()

    def _initialize(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            value TEXT
        )
        """)

        conn.commit()
        conn.close()

    def execute(self, query: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(query)

            if query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                return rows
            else:
                conn.commit()
                return "Query executed successfully"

        except sqlite3.Error as e:
            return f"SQL Error: {e}"

        finally:
            conn.close()