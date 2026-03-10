import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# Load .env first
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

# Now read API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Initialize Groq client
client = Groq(api_key=api_key)

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

    # Safety cleanup
    sql = sql.split("\n")[0]

    return sql