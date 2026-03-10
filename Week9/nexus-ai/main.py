import asyncio
import sys
sys.path.append("..")

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

from orchestrator import NexusOrchestrator


async def main():
    print("=" * 60)
    print("  NEXUS AI — Autonomous Multi-Agent System")
    print("  Type your query below. Type 'exit' to quit.")
    print("=" * 60)

    orchestrator = NexusOrchestrator()

    while True:
        try:
            print()
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("\nGoodbye! NEXUS AI shutting down.")
                break

            final_report = await orchestrator.run(user_input)

            print("\n" + "=" * 60)
            print("  NEXUS AI — FINAL REPORT")
            print("=" * 60)
            print(final_report)
            print("=" * 60)

        except KeyboardInterrupt:
            print("\n\nGoodbye! NEXUS AI shutting down.")
            break

        except Exception as e:
            print(f"\n[NEXUS ERROR] {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())