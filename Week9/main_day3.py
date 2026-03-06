import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, PROJECT_ROOT)

from tools.file_agent import FileAgent
from tools.code_executor import CodeExecutor
from tools.db_agent import DBAgent


class Day3Orchestrator:

    def __init__(self):
        self.file_agent = FileAgent()
        self.code_executor = CodeExecutor()
        self.db_agent = DBAgent("testing/day3.db")

    def run(self, user_query: str):

        print("\n[ORCHESTRATOR] Received query:")
        print(user_query)

        query_lower = user_query.strip().lower()

        # 1️SQL MODE
        if query_lower.startswith(("select", "insert", "create", "update", "delete")):
            print("\n[ORCHESTRATOR] Routing to DBAgent (SQL Mode)...")
            result = self.db_agent.execute(user_query)
            print("\n=== SQL RESULT ===")
            print(result)
            return
        
        # 2️ PYTHON CODE MODE

        if (
            user_query.strip().startswith("print")
            or "=" in user_query
            or "for " in user_query
        ):
            print("\n[ORCHESTRATOR] Routing to CodeExecutor (Python Mode)...")
            result = self.code_executor.run(user_query)
            print("\n=== PYTHON RESULT ===")
            print(result)
            return

        
        # 3️ CSV ANALYSIS MODE 
        if "sales.csv" in query_lower:
            print("\n[ORCHESTRATOR] Running CSV Analysis Flow...")

            sales_data = self.file_agent.read_csv("testing/sales.csv")

            analysis_code = f"""
data = {sales_data}

for row in data:
    row['price'] = int(row['price'])
    row['quantity'] = int(row['quantity'])
    row['revenue'] = row['price'] * row['quantity']

total_revenue = sum(item['revenue'] for item in data)
total_units = sum(item['quantity'] for item in data)
average_price = sum(item['price'] for item in data) / len(data)

top_product = max(data, key=lambda x: x['revenue'])
lowest_product = min(data, key=lambda x: x['revenue'])

print("Insight 1: Total Revenue =", total_revenue)
print("Insight 2: Total Units Sold =", total_units)
print("Insight 3: Average Price =", round(average_price, 2))
print("Insight 4: Top Revenue Product =", top_product['product'])
print("Insight 5: Lowest Revenue Product =", lowest_product['product'])
"""

            result = self.code_executor.run(analysis_code)

            print("\n=== TOP 5 INSIGHTS ===")
            print(result)

            # Store insights into DB
            for line in result.split("\n"):
                if line.strip():
                    self.db_agent.execute(
                        f"INSERT INTO insights (title, value) VALUES ('CSV Insight', '{line}')"
                    )

            return

        print("\n[ORCHESTRATOR] Unsupported query type.")


def main():
    print("=== Week 9 | Day 3 Tool-Chain System ===")
    user_query = input("\nUser: ")

    orchestrator = Day3Orchestrator()
    orchestrator.run(user_query)


if __name__ == "__main__":
    main()