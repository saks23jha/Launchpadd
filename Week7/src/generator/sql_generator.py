import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL_NAME = "llama-3.1-8b-instant"



def generate_sql(question: str, schema: str) -> str:
    prompt = f"""
You are an expert SQL generator.

Database schema:
{schema}

Rules:
- Generate ONLY a valid SQLite SELECT query
- Do NOT explain anything
- Do NOT use markdown
- Do NOT add comments

Question:
{question}

SQL:
""".strip()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You generate SQL queries for SQLite databases."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()
    sql = sql.split("\n")[0]  # safety

    return sql
