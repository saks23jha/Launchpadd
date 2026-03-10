import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO


def create_researcher():
    system_prompt = """
    You are the Researcher Agent inside NEXUS AI.

    Your role:
    - Receive a specific step or topic to research
    - Produce detailed, factual research notes
    - Cover all relevant facts, concepts, and explanations

    Strict rules:
    - DO NOT summarize or compress information
    - DO NOT write code
    - DO NOT plan or break into steps
    - DO NOT add opinions or recommendations
    - Write raw, detailed research notes only
    - Think of yourself as preparing notes for other agents
    """

    model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.2,
        model_info=MODEL_INFO,
    )

    return AssistantAgent(
        name="researcher",
        system_message=system_prompt,
        model_client=model_client,
    )


async def run_researcher(step: str) -> str:
    """
    Run researcher on a single step and return research notes.
    """
    agent = create_researcher()

    prompt = f"""
    Research the following topic in detail:
    {step}

    Provide comprehensive research notes.
    Cover all relevant facts, concepts, definitions, and explanations.
    """

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    output = response.chat_message.content
    print(f"\n[RESEARCHER] Research completed for: {step[:50]}...")

    return output