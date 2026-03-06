import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from tools.db_agent import DBAgent


def main():
    db_path = "testing/test.db"
    db = DBAgent(db_path)

    print("---- Creating table ----")
    print(
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER
            )
            """
        )
    )

    print("\n---- Inserting data ----")
    print(db.execute("INSERT INTO users (name, age) VALUES ('Alice', 25)"))
    print(db.execute("INSERT INTO users (name, age) VALUES ('Bob', 30)"))

    print("\n---- Fetching data ----")
    rows = db.execute("SELECT * FROM users")
    print(rows)


if __name__ == "__main__":
    main()