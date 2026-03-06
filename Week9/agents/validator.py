import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


def create_validator_agent():
    """
    Validator Agent

    Responsibilities:
    - Evaluate the refined output produced by the Planner
    - Check for correctness, clarity, and completeness
    - Approve or reject the output with a clear verdict

    Constraints:
    - Does NOT modify the content
    - Does NOT generate the final answer
    """

    system_prompt = """
    You are a Validator Agent.

    Your role:
    - Evaluate the provided content for correctness and completeness.
    - Check whether the answer addresses the user query properly.
    - Identify logical errors, missing steps, or unclear explanations.

    Decision rules:
    - If the content is correct, complete, and clear, respond with:
      APPROVED
    - If the content has issues, respond with:
      REJECTED: <brief reason>

    Strict rules:
    - DO NOT rewrite or improve the content.
    - DO NOT add new information.
    - DO NOT answer the user.
    - DO NOT mention other agents or internal processes.

    Your response must be a single-line verdict.
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

    agent = AssistantAgent(
        name="validator_agent",
        system_message=system_prompt,
        model_client=model_client,
    )

    # Small memory window to avoid contamination
    agent.memory_window = 5

    return agent