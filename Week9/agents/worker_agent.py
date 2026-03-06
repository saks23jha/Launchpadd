import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


def create_worker_agent():
    """
    Worker Agent (Executor)

    Responsibilities:
    - Execute a single task assigned by the Planner
    - Produce task-specific output
    - Remain stateless and reusable

    Constraints:
    - No planning
    - No validation
    - No reflection
    """

    system_prompt = """
    You are a Worker Agent.

    Your role:
    - Execute the given task exactly as described.
    - Focus only on the task provided in the message.

    Strict rules:
    - DO NOT plan or break tasks into subtasks.
    - DO NOT validate correctness.
    - DO NOT reflect on or improve answers.
    - DO NOT assume future steps.
    - Return only the task result.

    You are an execution unit in a larger orchestration system.
    """

    model_client = OpenAIChatCompletionClient(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=0.3,
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
        name="worker_agent",
        system_message=system_prompt,
        model_client=model_client,
    )

    # Memory window kept small to reinforce stateless execution
    agent.memory_window = 5

    return agent