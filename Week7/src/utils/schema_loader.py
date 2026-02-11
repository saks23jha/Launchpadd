import sqlite3
from pathlib import Path

DB_PATH = Path("src/data/sales.db")

def load_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    schema_lines = []

    for (table,) in tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]
        schema_lines.append(f"Table {table}: columns = {', '.join(col_names)}")

    conn.close()
    return "\n".join(schema_lines)

if __name__ == "__main__":
    print(load_schema())
