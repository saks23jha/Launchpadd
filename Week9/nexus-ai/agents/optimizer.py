import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO


def create_optimizer():
    system_prompt = """
    You are the Optimizer Agent inside NEXUS AI.

    Your role:
    - Receive the original analysis and the critic's feedback
    - Improve the analysis based on the critic's suggestions
    - Fix all identified flaws and gaps
    - Produce a better, stronger version of the analysis

    Strict rules:
    - DO NOT ignore any criticism
    - DO NOT add completely new topics
    - DO NOT write code
    - Base improvements strictly on critic feedback
    - Keep the same structured format as the original analysis
    - Output must be noticeably better than the original
    """

    model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.3,
        model_info=MODEL_INFO,
    )

    return AssistantAgent(
        name="optimizer",
        system_message=system_prompt,
        model_client=model_client,
    )


async def run_optimizer(analysis: str, critique: str) -> str:
    """
    Improve the analysis based on critic feedback.
    """
    agent = create_optimizer()

    prompt = f"""
    You have been given an analysis and a critique of that analysis.

    Original Analysis:
    {analysis}

    Critic Feedback:
    {critique}

    Now produce an improved version of the analysis.
    Fix all the flaws identified by the critic.
    Keep the same structured format.
    """

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    output = response.chat_message.content
    print(f"\n[OPTIMIZER] Optimization completed.")

    return output