import os
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.file_tool import read_csv, write_csv, write_txt, read_txt, get_file_summary


def create_file_agent():
    system_prompt = """
    You are a File Agent.

    Your role:
    - Generate data when asked to write a CSV or TXT file
    - Return data in clean Python list of dicts format for CSV
    - Return plain text for TXT files

    For CSV requests:
    - Return ONLY a Python list of dicts, nothing else
    - No explanation, no markdown, no code blocks
    - Example: [{"name": "Alice", "age": "20"}, {"name": "Bob", "age": "22"}]

    For TXT requests:
    - Return ONLY the plain text content
    - No explanation, no markdown

    Strict rules:
    - DO NOT add any explanation
    - DO NOT wrap in code blocks
    - Return ONLY the raw data
    """

    model_client = OpenAIChatCompletionClient(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=0.2,
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
        name="file_agent",
        system_message=system_prompt,
        model_client=model_client,
    )


async def run_file_agent(user_message: str) -> str:
    """
    Handles write requests — LLM generates data, tool writes the file.
    """
    import ast

    agent = create_file_agent()
    msg = user_message.lower()

    # --- Write CSV ---
    if ".csv" in msg:
        # Extract filename
        words = user_message.split()
        filename = next((w for w in words if w.endswith(".csv")), "data/output.csv")

        prompt = f"""
        {user_message}

        Return ONLY a Python list of dicts.
        No explanation. No markdown. No code blocks.
        Just the raw list like: [{{"col1": "val1"}}, ...]
        """

        response = await agent.on_messages(
            [TextMessage(content=prompt, source="orchestrator")],
            cancellation_token=None,
        )

        raw = response.chat_message.content.strip()
        print(f"[FILE AGENT] LLM returned:\n{raw}")

        try:
            data = ast.literal_eval(raw)
            write_csv(filename, data)
            return f"CSV file written to {filename} with {len(data)} rows."
        except Exception as e:
            return f"Failed to parse LLM output as CSV data: {e}"

    # --- Write TXT ---
    elif ".txt" in msg:
        words = user_message.split()
        filename = next((w for w in words if w.endswith(".txt")), "data/output.txt")

        response = await agent.on_messages(
            [TextMessage(content=user_message, source="orchestrator")],
            cancellation_token=None,
        )

        content = response.chat_message.content.strip()
        write_txt(filename, content)
        return f"TXT file written to {filename}."

    else:
        return "Please specify a .csv or .txt filename in your request."
