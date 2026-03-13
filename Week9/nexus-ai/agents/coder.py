import os
import sys
sys.path.append("..")

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from config import MODEL_NAME, API_KEY, BASE_URL, MODEL_INFO
from tools.code_executor import execute_python, execute_analysis


def create_coder():
    system_prompt = """
    You are a Code Agent inside NEXUS AI.

    Your role:
    - Write clean, complete, working Python code
    - Use print() to output all results

    For PIPELINE requests:
    - Understand what type of pipeline is being requested
    - Identify ALL necessary steps for that specific pipeline type
    - Implement every step completely and correctly
    - ONLY use numbers or quantities explicitly mentioned in the task
    - If no quantity is mentioned, use exactly 5 sample items
    - The code must be completely self-contained

    For DATA ANALYSIS requests:
    - Data is already loaded in a variable called 'data' (list of dicts)
    - NEVER redefine or hardcode the 'data' variable
    - Always use the existing 'data' variable directly

    CRITICAL rules:
    - DO NOT add markdown or code blocks
    - DO NOT add ``` anywhere in your response
    - ALL comments MUST start with # symbol
    - NEVER write plain English sentences without # prefix
    - Return ONLY raw executable Python code
    - Always use print() to show results
    - No external libraries — standard Python only
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


def clean_generated_code(generated_code: str) -> str:
    """
    Post-process generated code to fix common issues:
    1. Remove markdown code blocks
    2. Comment out unused imports
    3. Fix plain English sentences missing # prefix
    """

    # -------------------------
    # Step 1: Strip markdown blocks
    # -------------------------
    lines = generated_code.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            continue
        cleaned_lines.append(line)
    generated_code = "\n".join(cleaned_lines).strip()

    # -------------------------
    # Step 2: Comment out unused imports
    # -------------------------
    code_lines = generated_code.split("\n")
    import_lines = {}

    for i, line in enumerate(code_lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            try:
                module = stripped.replace("import ", "").split(" as ")[-1].strip().split(".")[0]
                import_lines[i] = (line, module)
            except Exception:
                pass

    # Check which imports are actually used
    used_names = set()
    for i, line in enumerate(code_lines):
        for idx, (imp_line, module) in import_lines.items():
            if i != idx and module in line:
                used_names.add(module)

    # Comment out unused imports
    step2_lines = []
    for i, line in enumerate(code_lines):
        if i in import_lines:
            module = import_lines[i][1]
            if module not in used_names:
                line = f"# {line.strip()}  # unused import"
        step2_lines.append(line)

    # -------------------------
    # Step 3: Fix plain English sentences missing #
    # -------------------------
    python_starters = (
        "#", "import", "from", "def ", "class ", "for ",
        "if ", "elif ", "else", "try", "except", "finally",
        "return", "print", "with ", "while ", "yield",
        "raise", "pass", "break", "continue", "@",
        "\"\"\"", "'''", "0", "1", "2", "3", "4",
        "5", "6", "7", "8", "9", "[", "{", "(", "-",
    )

    final_lines = []
    for line in step2_lines:
        stripped = line.strip()
        if (
            stripped
            and not any(stripped.startswith(s) for s in python_starters)
            and "=" not in stripped
            and "(" not in stripped
            and ":" not in stripped
            and stripped.endswith(".")
        ):
            line = "# " + stripped
        final_lines.append(line)

    return "\n".join(final_lines).strip()


async def run_coder(task: str, context: str = "", data: list[dict] = None) -> dict:
    agent = create_coder()

    is_pipeline = "pipeline" in task.lower()

    if is_pipeline:
        prompt = f"""
You are writing a complete, self-contained Python pipeline.

Task: {task}

Instructions:
- Understand what type of pipeline is being requested
- Identify ALL the necessary steps for THIS specific pipeline
- Implement each step completely and correctly
- IMPORTANT: Only use numbers or quantities explicitly mentioned in the task
- If no quantity is mentioned, use exactly 5 sample items only — never more
- If task says "50k documents", simulate 50k using a loop
- If task says "chunking pipeline" with no number, use exactly 5 sample documents
- Each step must print its progress and output clearly
- The code must be completely self-contained — no external libraries
- Do NOT add markdown or code blocks
- Do NOT add ``` anywhere
- ALL comments MUST start with # symbol
- NEVER write plain English sentences without # prefix
- Return ONLY raw Python code

Examples of pipeline steps by type:
- RAG pipeline → document loading, chunking, embedding, vector store, retrieval, generation
- ETL pipeline → extract, transform, load, validate
- Chunking pipeline → load, preprocess, chunk, store, validate
- Data pipeline → ingest, clean, transform, aggregate, export
- NLP pipeline → load, tokenize, clean, vectorize, classify
- Training pipeline → load data, preprocess, train, evaluate, save model

Now identify the correct steps for: {task}
Then implement ALL of them completely in Python.

Context for reference:
{context[:300]}
"""

    elif data:
        prompt = f"""
You have access to a variable called 'data' which is a list of dicts loaded from a real CSV file.

Columns: {list(data[0].keys())}
Total rows: {len(data)}
Sample rows: {data[:3]}

Task: {task}

IMPORTANT:
- Use the 'data' variable directly — it is already loaded with {len(data)} real rows
- DO NOT create or hardcode any new data
- DO NOT redefine the 'data' variable
- Use only print() to show results
- Do not use any imports
- Do NOT add markdown or code blocks
- Do NOT add ``` anywhere
- ALL comments MUST start with # symbol
- NEVER write plain English sentences without # prefix
- Write clean Python code only
"""

    else:
        prompt = f"""
Task: {task}

Context:
{context[:300]}

Write complete working Python code to accomplish this task.
Use only print() to show results.
Do not use any imports unless absolutely necessary.
Do NOT add markdown or code blocks.
Do NOT add ``` anywhere.
ALL comments MUST start with # symbol.
NEVER write plain English sentences without # prefix.
Return ONLY raw executable Python code.
"""

    print(f"\n[CODER] Generating code for: {task[:50]}...")

    response = await agent.on_messages(
        [TextMessage(content=prompt, source="orchestrator")],
        cancellation_token=None,
    )

    generated_code = response.chat_message.content.strip()

    # Clean the generated code
    generated_code = clean_generated_code(generated_code)

    print(f"\n[CODER] Generated code:\n{generated_code}")

    # Execute the code
    if data and not is_pipeline:
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
        "is_pipeline": is_pipeline,
    }