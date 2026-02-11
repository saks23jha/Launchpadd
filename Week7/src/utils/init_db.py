import sqlite3
from pathlib import Path

DB_PATH = Path("src/data/sales.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER,
    product TEXT,
    revenue REAL,
    region TEXT
)
""")

cursor.executemany(
    "INSERT INTO sales (year, product, revenue, region) VALUES (?, ?, ?, ?)",
    [
        (2023, "Drug A", 120.5, "US"),
        (2023, "Drug B", 98.2, "Europe"),
        (2022, "Drug A", 110.1, "US"),
        (2022, "Drug C", 76.4, "Asia"),
    ]
)

conn.commit()
conn.close()

print("sales.db created successfully")
