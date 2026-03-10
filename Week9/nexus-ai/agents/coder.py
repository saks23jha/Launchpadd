import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO
from tools.code_executor import execute_python


def create_coder():
    system_prompt = """
    You are the Coder Agent inside NEXUS AI.

    Your role:
    - Write clean Python code to solve the given task
    - Use print() to output all results
    - Keep code simple and readable

    Strict rules:
    - DO NOT explain the code
    - DO NOT add markdown or code blocks
    - DO NOT import external libraries except standard Python
    - Return ONLY raw executable Python code
    - Always use print() to show results
    - Data is available as a variable called 'data' if needed
    """

    model_client = OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=API_KEY,
        base_url=BASE_URL,
        temperature=0.2,
        model_info=MODEL_INFO,
    )

    return AssistantAgent(
        name="coder",
        system_message=system_prompt,
        model_client=model_client,
    )


async def run_coder(task: str, context: str = "", data: list[dict] = None) -> dict:
    """
    Generate and execute Python code for the given task.
    """
    agent = create_coder()

    prompt = f"""
    Task: {task}

    Context:
    {context}

    Write Python code to complete this task.
    Use only print() to show results.
    Do not use any imports.
    """

    if data:
        prompt += f"\nData is available as variable 'data' (list of dicts). Columns: {list(data[0].keys())}"

    print(f"\n[CODER] Generating code for: {task[:50]}...")

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    generated_code = response.chat_message.content.strip()
    print(f"\n[CODER] Generated code:\n{generated_code}")

    # Execute the generated code
    if data:
        from tools.code_executor import execute_analysis
        result = execute_analysis(generated_code, data)
    else:
        result = execute_python(generated_code)

    if result["success"]:
        print(f"\n[CODER] Execution successful:\n{result['output']}")
    else:
        print(f"\n[CODER] Execution failed:\n{result['error']}")

    return {
        "task": task,
        "code": generated_code,
        "output": result["output"],
        "success": result["success"],
        "error": result.get("error"),
    }