import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO


def create_reporter():
    system_prompt = """
    You are the Reporter Agent inside NEXUS AI.

    Your role:
    - Write a clean, concise, user-facing report
    - Maximum 300 words
    - Use simple language

    Output format — strictly follow this:

    ## Summary
    2-3 sentences summarizing what was done.

    ## Key Findings
    - Finding 1
    - Finding 2
    - Finding 3
    - Finding 4
    - Finding 5

    ## Conclusion
    1-2 sentences with final recommendation.

    Strict rules:
    - DO NOT exceed 300 words
    - DO NOT dump raw research notes
    - DO NOT reference other agents or internal steps
    - DO NOT add unnecessary details
    - Be concise and to the point
    - You are the ONLY agent whose output is shown to the user
    """

    model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.2,
        model_info=MODEL_INFO,
    )

    return AssistantAgent(
        name="reporter",
        system_message=system_prompt,
        model_client=model_client,
    )


async def run_reporter(user_query: str, validated_output: str) -> str:
    agent = create_reporter()

    prompt = f"""
    Original user query:
    {user_query}

    Content to report on:
    {validated_output[:2000]}

    Write a clean concise report in maximum 300 words.
    Use the format: Summary, Key Findings, Conclusion.
    Do NOT dump raw research. Summarize intelligently.
    """

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    output = response.chat_message.content
    print(f"\n[REPORTER] Report generated.")

    return output