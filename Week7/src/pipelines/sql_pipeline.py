import sqlite3
from pathlib import Path
from src.utils.schema_loader import load_schema
from src.generator.sql_generator import generate_sql

DB_PATH = Path("src/data/sales.db")

def validate_sql(sql):
    sql_lower = sql.lower()
    if not sql_lower.startswith("select"):
        raise ValueError("Only SELECT queries allowed")
    for word in ["drop", "delete", "update", "insert", ";"]:
        if word in sql_lower:
            raise ValueError("Unsafe SQL detected")
    return True

def execute_sql(sql):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    conn.close()
    return cols, rows

def run_sql_qa(question):
    schema = load_schema()
    sql = generate_sql(question, schema)

    print("\nGenerated SQL:\n", sql)

    validate_sql(sql)
    cols, rows = execute_sql(sql)

    return cols, rows

if __name__ == "__main__":
    q = input("Ask a question: ")
    cols, rows = run_sql_qa(q)

    print("\nResult:")
    print(cols)
    for r in rows:
        print(r)
