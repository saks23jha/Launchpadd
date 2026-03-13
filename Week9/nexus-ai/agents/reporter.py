import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO


def create_reporter():
    system_prompt = """
    You are the Reporter Agent inside NEXUS AI.

    First understand what type of query was asked, then write the most appropriate report.

    You must intelligently detect the query type and respond accordingly:

    - If it's about a PIPELINE → write code flow explanation
    - If it's about PLANNING or STRATEGY → write a structured business plan
    - If it's about ARCHITECTURE or TECHNICAL DESIGN → write a technical document
    - If it's about CODE or ALGORITHM → show the code and explain it
    - For EVERYTHING ELSE → write a concise summary report

    Always use proper markdown formatting with headers.
    Always be detailed, specific, and useful.
    Never reference internal agents or processing steps.
    You are the only output the user sees.
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


async def run_reporter(
    user_query: str,
    validated_output: str,
    is_pipeline: bool = False
) -> str:
    agent = create_reporter()

    prompt = f"""
User Query: {user_query}

Content to report on:
{validated_output[:3000]}

Instructions:
- Read the user query carefully
- Understand what type of output is most useful
- Write the most appropriate, detailed, and well-structured report
- Use proper markdown headers and formatting
- Be specific, actionable, and clear
- Do NOT mention internal agents or processing steps
"""

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    output = response.chat_message.content
    print(f"\n[REPORTER] Report generated.")

    return output