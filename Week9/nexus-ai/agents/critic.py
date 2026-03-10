import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO


def create_critic():
    system_prompt = """
    You are the Critic Agent inside NEXUS AI.

    Your role:
    - Review the analysis provided
    - Identify weaknesses, gaps, and flaws
    - Be honest and direct in your criticism

    Output format:
    FLAW 1: <flaw or weakness>
    FLAW 2: <flaw or weakness>
    FLAW 3: <flaw or weakness>
    SUGGESTION: <how to improve overall>

    Strict rules:
    - DO NOT rewrite or improve the content yourself
    - DO NOT add new information
    - DO NOT validate or approve
    - ONLY identify flaws and suggest improvements
    - Be specific, not vague
    - If no flaws found respond with: NO FLAWS FOUND
    """

    model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.3,
        model_info=MODEL_INFO,
    )

    return AssistantAgent(
        name="critic",
        system_message=system_prompt,
        model_client=model_client,
    )


async def run_critic(analysis: str) -> str:
    """
    Critique the analysis and return flaws and suggestions.
    """
    agent = create_critic()

    prompt = f"""
    Review the following analysis and identify all flaws and weaknesses:

    {analysis}

    Be specific and direct in your criticism.
    """

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    output = response.chat_message.content
    print(f"\n[CRITIC] Critique completed.")

    return output