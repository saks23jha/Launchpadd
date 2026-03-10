import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()

from orchestrator.day3_planner import Day3Planner


async def main():
    planner = Day3Planner()
    await planner.chat()


if __name__ == "__main__":
    asyncio.run(main())
    sys.exit(0)