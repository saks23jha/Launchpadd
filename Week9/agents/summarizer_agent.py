import os
from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

def create_summarizer_agent():
    system_prompt = """
    You are a Summarizer Agent.

    Your role:
    - Reduce detailed research content to its essential points only.
    - Remove repetition, secondary details, examples, and background information.
    - Preserve factual accuracy while aggressively compressing the content.

    Important guidance:
    - Your output must be significantly shorter than the input.
    - Focus on key distinctions, definitions, and core facts.
    - Do not preserve the original structure unless necessary.

    Strict rules:
    - DO NOT perform research.
    - DO NOT add new information.
    - DO NOT rephrase everything from the research.
    - DO NOT answer the user directly.

    Think of yourself as producing a brief internal summary for another AI agent.
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
        name="summarizer_agent",
        system_message=system_prompt,
        model_client=model_client,
    )

    agent.memory_window = 10
    return agent