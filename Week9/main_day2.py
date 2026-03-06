import asyncio
from dotenv import load_dotenv

load_dotenv()

from orchestrator.planner import Planner


async def main():
    print("\n=== Week 9 | Day 2 : Planner–Executor System ===\n")

    user_query = input("Enter your question: ").strip()

    if not user_query:
        print("Error: Query cannot be empty.")
        return

    planner = Planner()

    try:
        final_answer = await planner.run(user_query)

        print("\n=== FINAL APPROVED ANSWER ===\n")
        print(final_answer)

    except Exception as e:
        print("\nExecution failed:")
        print(str(e))


if __name__ == "__main__":
    asyncio.run(main())