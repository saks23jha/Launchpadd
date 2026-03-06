import csv
import os
from typing import List, Dict, Any


class FileAgent:
    """
    File Agent

    Responsibilities:
    - Read .txt files
    - Read .csv files
    - Write .txt files
    - Write .csv files

    This agent performs NO reasoning.
    It only executes filesystem operations.
    """

    
    # Read Text File

    def read_txt(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    
    # Write Text File

    def write_txt(self, file_path: str, content: str) -> None:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)


    # Read CSV File

    def read_csv(self, file_path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)


    # Write CSV File
    
    def write_csv(self, file_path: str, rows: List[Dict[str, Any]]) -> None:
        if not rows:
            raise ValueError("CSV write failed: no data provided")

        fieldnames = rows[0].keys()

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)