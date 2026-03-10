import csv
import os


def read_csv(filepath: str) -> list[dict]:
    """
    Read a CSV file and return a list of row dictionaries.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [dict(row) for row in reader]

    print(f"[FILE TOOL] Read {len(rows)} rows from {filepath}")
    return rows


def write_csv(filepath: str, data: list[dict], fieldnames: list[str] = None):
    """
    Write a list of dictionaries to a CSV file.
    """
    if not data:
        raise ValueError("No data to write.")

    if fieldnames is None:
        fieldnames = list(data[0].keys())

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"[FILE TOOL] Written {len(data)} rows to {filepath}")


def read_txt(filepath: str) -> str:
    """
    Read a plain text file and return its content.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"[FILE TOOL] Read text file: {filepath}")
    return content


def write_txt(filepath: str, content: str):
    """
    Write a string to a plain text file.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[FILE TOOL] Written text file: {filepath}")


def get_file_summary(filepath: str) -> dict:
    """
    Return basic metadata about a CSV file.
    """
    rows = read_csv(filepath)

    if not rows:
        return {"rows": 0, "columns": [], "filepath": filepath}

    return {
        "filepath": filepath,
        "rows": len(rows),
        "columns": list(rows[0].keys()),
        "sample": rows[:3],
    }