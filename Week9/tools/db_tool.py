import sqlite3
import os

DB_PATH = "data/sales.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table_from_csv(data: list[dict], table_name: str = "sales"):
    if not data:
        raise ValueError("No data provided.")

    columns = list(data[0].keys())
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

    col_defs = ", ".join([f"{col} TEXT" for col in columns])
    cursor.execute(f"CREATE TABLE {table_name} ({col_defs})")

    for row in data:
        values = [row[col] for col in columns]
        placeholders = ", ".join(["?" for _ in columns])
        cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)

    conn.commit()
    conn.close()
    print(f"[DB TOOL] Table '{table_name}' created with {len(data)} rows")


def run_query(query: str) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    print(f"[DB TOOL] Query returned {len(rows)} rows")
    return rows


def run_write_query(query: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()
    print(f"[DB TOOL] Write query executed")


def get_table_info(table_name: str = "sales") -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row["name"] for row in cursor.fetchall()]

    cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
    count = cursor.fetchone()["count"]

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
    sample = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "table": table_name,
        "columns": columns,
        "row_count": count,
        "sample": sample,
    }


def list_tables() -> list[str]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row["name"] for row in cursor.fetchall()]
    conn.close()
    print(f"[DB TOOL] Tables: {tables}")
    return tables