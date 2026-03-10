import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO


def create_validator():
    system_prompt = """
    You are the Validator Agent inside NEXUS AI.

    Your role:
    - Evaluate if the content is reasonable and addresses the query
    - Be lenient — approve if the content is mostly correct and complete

    Decision rules:
    - APPROVE if the content addresses the query, even partially
    - REJECT only if the content is completely wrong or empty

    Respond with ONLY one line:
    APPROVED
    or
    REJECTED: <one sentence reason>

    Strict rules:
    - DO NOT be overly strict
    - DO NOT reject for minor issues
    - DO NOT rewrite or improve content
    - Default to APPROVED when in doubt
    """

    model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.0,
        model_info=MODEL_INFO,
    )

    return AssistantAgent(
        name="validator",
        system_message=system_prompt,
        model_client=model_client,
    )


async def run_validator(optimized_output: str) -> dict:
    agent = create_validator()

    prompt = f"""
    Evaluate the following content.
    Approve if it is reasonable and addresses the topic.
    Only reject if it is completely wrong or empty.

    {optimized_output[:1500]}

    Respond with ONLY: APPROVED or REJECTED: <reason>
    """

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    verdict = response.chat_message.content.strip()
    approved = verdict.upper().startswith("APPROVED")

    print(f"\n[VALIDATOR] Verdict: {verdict}")

    return {
        "verdict": verdict,
        "approved": approved,
    }