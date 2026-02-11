from src.memory.memory_store import add_message, get_memory
from src.evaluation.rag_eval import evaluate_answer

def ask_text(question: str):
    add_message("user", question)

    answer = f"Answer generated for: {question}"

    add_message("assistant", answer)

    return {
        "answer": answer,
        "memory": get_memory(),
        "evaluation": evaluate_answer(question, answer)
    }
