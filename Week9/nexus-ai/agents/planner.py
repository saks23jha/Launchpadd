import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO


def create_planner():
    system_prompt = """
    You are the Planner Agent inside NEXUS AI.

    Your role:
    - Receive the user query
    - Break it down into clear, ordered steps
    - Each step must be specific and actionable
    - Steps will be executed by other agents

    Output format — always respond like this:
    STEP 1: <what needs to be done>
    STEP 2: <what needs to be done>
    STEP 3: <what needs to be done>
    ...and so on

    Strict rules:
    - DO NOT execute any steps yourself
    - DO NOT write code
    - DO NOT do research
    - ONLY break the query into steps
    - Always output at least 3 steps
    """

    model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.2,
        model_info=MODEL_INFO,
    )

    return AssistantAgent(
        name="planner",
        system_message=system_prompt,
        model_client=model_client,
    )


async def run_planner(user_query: str) -> list[str]:
    """
    Run planner and return list of steps.
    """
    agent = create_planner()

    response = await agent.on_messages(
        [TextMessage(content=user_query, source="orchestrator")],
        cancellation_token=None,
    )

    raw_output = response.chat_message.content
    print(f"\n[PLANNER] Steps generated:\n{raw_output}")

    # Parse steps into list
    steps = []
    for line in raw_output.strip().split("\n"):
        line = line.strip()
        if line.upper().startswith("STEP"):
            # Extract just the description after "STEP N:"
            parts = line.split(":", 1)
            if len(parts) == 2:
                steps.append(parts[1].strip())

    return steps
