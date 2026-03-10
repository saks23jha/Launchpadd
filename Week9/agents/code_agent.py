import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.code_executor import execute_analysis


def create_code_agent():
    system_prompt = """
    You are a Code Agent.

    Your role:
    - Analyze data given to you and generate Python code to find insights
    - Return only clean executable Python code
    - Use print() to output all results

    Strict rules:
    - DO NOT explain the code
    - DO NOT add markdown or code blocks
    - DO NOT read files yourself
    - DO NOT query databases
    - Data is already available as a variable called 'data' (list of dicts)
    - Always use print() to show results
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
        name="code_agent",
        system_message=system_prompt,
        model_client=model_client,
    )

    return agent


async def run_code_agent(data: list[dict], task: str) -> dict:
    """
    Ask the LLM to generate analysis code,
    then execute it using code_executor.
    """

    agent = create_code_agent()

    from autogen_agentchat.messages import TextMessage

    prompt = f"""
    You have access to a variable called 'data' which is a list of dicts.
    Each dict is a row from a CSV file.

    Columns available: {list(data[0].keys())}

    Task: {task}

    Write Python code to complete this task.
    Use only print() to show results.
    Do not use any imports.
    """

    print(f"[CODE AGENT] Requesting code for task: {task}")

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    generated_code = response.chat_message.content
    print(f"[CODE AGENT] Generated code:\n{generated_code}")

    result = execute_analysis(generated_code, data)

    return {
        "task": task,
        "code": generated_code,
        "output": result["output"],
        "success": result["success"],
        "error": result.get("error"),
    }