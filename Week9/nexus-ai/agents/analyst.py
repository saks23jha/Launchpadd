import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO


def create_analyst():
    system_prompt = """
    You are the Analyst Agent inside NEXUS AI.

    Your role:
    - Analyze the research notes and code outputs provided
    - Extract key insights, patterns, and conclusions
    - Present findings in a clear and structured way

    Output format:
    INSIGHT 1: <insight>
    INSIGHT 2: <insight>
    INSIGHT 3: <insight>
    CONCLUSION: <overall conclusion>

    Strict rules:
    - DO NOT write code
    - DO NOT do research
    - DO NOT plan steps
    - ONLY analyze what is given to you
    - Base analysis strictly on provided content
    - Do not add outside knowledge
    """

    model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.2,
        model_info=MODEL_INFO,
    )

    return AssistantAgent(
        name="analyst",
        system_message=system_prompt,
        model_client=model_client,
    )


async def run_analyst(research: str, code_output: str = "") -> str:
    """
    Analyze research notes and code output.
    Returns structured insights and conclusion.
    """
    agent = create_analyst()

    prompt = f"""
    Analyze the following content and extract key insights:

    Research Notes:
    {research}
    """

    if code_output:
        prompt += f"""
    Code Execution Output:
    {code_output}
    """

    prompt += """
    Provide structured insights and a clear conclusion.
    """

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    output = response.chat_message.content
    print(f"\n[ANALYST] Analysis completed.")

    return output