from fastapi import FastAPI
from pydantic import BaseModel

from src.deployment.ask import ask_text
from src.deployment.ask_image import ask_image, explain_image
from src.deployment.ask_sql import ask_sql

app = FastAPI(title="Multimodal RAG Capstone")


class Question(BaseModel):
    question: str


class ImageQuery(BaseModel):
    query: str


class ImageExplain(BaseModel):
    image_path: str


# ---------- TEXT ----------
@app.post("/ask")
def ask_endpoint(req: Question):
    return ask_text(req.question)


# ---------- IMAGE ----------
@app.post("/ask-image")
def ask_image_endpoint(req: ImageQuery):
    return ask_image(req.query)


@app.post("/ask-image/explain")
def explain_image_endpoint(req: ImageExplain):
    return explain_image(req.image_path)


# ---------- SQL ----------
@app.post("/ask-sql")
def ask_sql_endpoint(req: Question):
    return ask_sql(req.question)
