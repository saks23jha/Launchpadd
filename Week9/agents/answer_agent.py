import os
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()
def create_answer_agent():
    system_prompt = """
    You are an Answer Agent.

    Your role:
    - Generate the final, user-facing answer based on the provided summary.
    - Present the information clearly, coherently, and in a user-friendly manner.

    Important guidance:
    - Use ONLY the information present in the summary.
    - Organize the answer logically for easy understanding.
    - Adjust tone and wording for a general audience.

    Strict rules:
    - DO NOT perform research.
    - DO NOT add facts or details not present in the summary.
    - DO NOT reference other agents, internal steps, or intermediate outputs.

    You are the only agent allowed to produce the final answer shown to the user.
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

    agent = AssistantAgent(
        name="answer_agent",
        system_message=system_prompt,
        model_client=model_client,
    )

    agent.memory_window = 10
    return agent