import os
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.file_agent import run_file_agent
from agents.code_agent import run_code_agent
from agents.db_agent import run_db_agent
from tools.file_tool import read_csv, write_csv, write_txt, read_txt
from tools.db_tool import create_table_from_csv


def create_router():
    system_prompt = """
    You are a Router Agent.

    Your job is to read the user message and decide which agent should handle it.

    Rules:
    - If the user wants to run, execute, or write Python code → reply with: code
    - If the user wants to read, write, create a .txt or .csv file → reply with: file
    - If the user wants to query, search, or ask questions about sales data → reply with: db

    Reply with ONLY one word: code, file, or db
    Nothing else. No explanation.
    """

    model_client = OpenAIChatCompletionClient(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=0.0,
        model_info={
            "provider": "groq",
            "family": "llama",
            "context_length": 8192,
            "vision": False,
            "function_calling": False,
            "json_output": False,
            "structured_output": False,
        },
    )

    return AssistantAgent(
        name="router",
        system_message=system_prompt,
        model_client=model_client,
    )


class Day3Planner:

    def __init__(self):
        self.router = create_router()
        print("[DAY3 PLANNER] Loading sales.csv into SQLite...")
        data = read_csv("data/sales.csv")
        create_table_from_csv(data)
        print("[DAY3 PLANNER] Sales data ready.\n")

    async def route(self, user_message: str) -> str:
        response = await self.router.on_messages(
            [TextMessage(content=user_message, source="user")],
            cancellation_token=None,
        )
        decision = response.chat_message.content.strip().lower()
        print(f"[ROUTER] Decision: {decision}")
        return decision

    async def handle_code(self, user_message: str):
        print("\n[CODE AGENT] Running...")
        result = await run_code_agent(
            data=read_csv("data/sales.csv"),
            task=user_message,
        )
        if result["success"]:
            print("\n[OUTPUT]\n")
            print(result["output"])
        else:
            print(f"\n[ERROR] {result['error']}")

    async def handle_file(self, user_message: str):
        print("\n[FILE AGENT] Running...")

        msg = user_message.lower()

        if "read" in msg and ".csv" in msg:
            filename = self.extract_filename(user_message, ".csv")
            data = read_csv(filename)
            print(f"\n[OUTPUT] {len(data)} rows read from {filename}:")
            for row in data[:5]:
                print(row)

        elif "read" in msg and ".txt" in msg:
            filename = self.extract_filename(user_message, ".txt")
            content = read_txt(filename)
            print(f"\n[OUTPUT] Content of {filename}:\n{content}")

        else:
            result = await run_file_agent(user_message)
            print(f"\n[OUTPUT]\n{result}")

    async def handle_db(self, user_message: str):
        print("\n[DB AGENT] Running...")
        data = read_csv("data/sales.csv")
        result = await run_db_agent(
            data=data,
            task=user_message,
        )
        if result["success"]:
            print(f"\n[SQL] {result['sql']}")
            print(f"\n[OUTPUT]")
            for row in result["results"]:
                print(row)
        else:
            print(f"\n[ERROR] DB query failed.")

    def extract_filename(self, message: str, extension: str) -> str:
        words = message.split()
        for word in words:
            if word.endswith(extension):
                return word
        return f"data/output{extension}"

    async def chat(self):
        print("=== Day 3 Tool Agent ===\n")

        user_input = input("You: ").strip()

        if not user_input:
            print("Please enter a valid query.")
            return

        decision = await self.route(user_input)

        if decision == "code":
            await self.handle_code(user_input)

        elif decision == "file":
            await self.handle_file(user_input)

        elif decision == "db":
            await self.handle_db(user_input)

        else:
            print("[ROUTER] Could not understand request. Please try again.")