from src.pipelines.sql_pipeline import run_sql_qa
from src.memory.memory_store import add_message, get_memory
from src.evaluation.rag_eval import evaluate_answer

def ask_sql(question: str):
    add_message("user", question)

    cols, rows = run_sql_qa(question)

    answer = {
        "columns": cols,
        "rows": rows
    }

    add_message("assistant", str(answer))

    return {
        "answer": answer,
        "memory": get_memory(),
        "evaluation": evaluate_answer(question, str(answer))
    }
