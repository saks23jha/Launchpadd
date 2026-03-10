import os
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from tools.db_tool import create_table_from_csv, run_query, get_table_info


def create_db_agent():
    system_prompt = """
    You are a DB Agent.

    Your role:
    - Write SQL queries to extract insights from a SQLite database
    - The table name is always 'sales'
    - Return only clean executable SQL queries

    Strict rules:
    - DO NOT explain the query
    - DO NOT add markdown or code blocks
    - DO NOT read files yourself
    - DO NOT run Python code
    - Return only a single SQL SELECT statement
    - Always use the table name 'sales'
    """

    model_client = OpenAIChatCompletionClient(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
        temperature=0.1,
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
        name="db_agent",
        system_message=system_prompt,
        model_client=model_client,
    )

    return agent


async def run_db_agent(data: list[dict], task: str) -> dict:
    """
    Load CSV data into SQLite, ask LLM to generate SQL,
    then execute the query and return results.
    """

    # Step 1: Load CSV data into SQLite
    print(f"[DB AGENT] Loading data into SQLite table 'sales'")
    create_table_from_csv(data)

    # Step 2: Get table info to give LLM context
    table_info = get_table_info()

    agent = create_db_agent()

    from autogen_agentchat.messages import TextMessage

    prompt = f"""
    You have access to a SQLite table called 'sales'.

    Columns: {table_info['columns']}
    Row count: {table_info['row_count']}
    Sample rows: {table_info['sample']}

    Task: {task}

    Write a single SQL SELECT query to complete this task.
    Return only the SQL query, nothing else.
    """

    print(f"[DB AGENT] Requesting SQL for task: {task}")

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    generated_sql = response.chat_message.content.strip()
    print(f"[DB AGENT] Generated SQL:\n{generated_sql}")

    # Step 3: Execute the SQL query
    results = run_query(generated_sql)

    return {
        "task": task,
        "sql": generated_sql,
        "results": results,
        "success": True,
    }