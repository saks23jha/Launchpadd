import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient


def create_research_agent():
    system_prompt = """
    You are a Research Agent.

    Your role:
    - Produce exhaustive and detailed research notes about the given topic.
    - Capture all relevant facts, comparisons, definitions, and explanations.
    - Include background information, characteristics, and distinctions where applicable.

    Important guidance:
    - Write raw research notes, not a polished explanation.
    - It is acceptable to be verbose and slightly repetitive if it improves completeness.
    - Do not optimize for readability or conciseness.

    Strict rules:
    - DO NOT summarize or compress information.
    - DO NOT simplify content for end users.
    - DO NOT answer the user directly.
    - DO NOT add opinions, recommendations, or conclusions.

    Think of yourself as preparing background notes for another AI agent.
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
        name="research_agent",
        system_message=system_prompt,
        model_client=model_client,
    )

    agent.memory_window = 10
    return agent