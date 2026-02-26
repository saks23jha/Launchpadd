from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import uuid
import logging
import os
from model_loader import load_model
import config

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# FastAPI app
app = FastAPI()

# Load model
model = load_model()

# Medical keywords
MEDICAL_KEYWORDS = ["pain", "cold","fever", "doctor", "medicine", "symptoms", "disease", "treatment", "hospital", "health", "blood", "heart", "diabetes", "infection", "headache", "stomach", "cancer", "surgery", "prescription", "diagnosis", "injury"]

# ── Request Models ──
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = config.MAX_TOKENS
    temperature: Optional[float] = config.TEMPERATURE
    top_k: Optional[int] = config.TOP_K
    top_p: Optional[float] = config.TOP_P

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []
    max_tokens: Optional[int] = config.MAX_TOKENS
    temperature: Optional[float] = config.TEMPERATURE
    top_k: Optional[int] = config.TOP_K
    top_p: Optional[float] = config.TOP_P

# ── POST /generate ──
@app.post("/generate")
def generate(request: GenerateRequest):
    request_id = str(uuid.uuid4())

    # Medical keyword check
    if not any(word in request.prompt.lower() for word in MEDICAL_KEYWORDS):
        return {"request_id": request_id, "response": "I can only answer medical questions!"}

    prompt = f"<|system|>\n{config.SYSTEM_PROMPT}</s>\n<|user|>\n{request.prompt}</s>\n<|assistant|>"
    output = model(
        prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_k=request.top_k,
        top_p=request.top_p,
        repeat_penalty=config.REPEAT_PENALTY
    )
    response = output["choices"][0]["text"].strip()
    logging.info(f"request_id={request_id} | endpoint=/generate | prompt={request.prompt} | response={response}")
    return {"request_id": request_id, "response": response}

# ── POST /chat ──
@app.post("/chat")
def chat(request: ChatRequest):
    request_id = str(uuid.uuid4())

    # Medical keyword check
    if not any(word in request.message.lower() for word in MEDICAL_KEYWORDS):
        return {"request_id": request_id, "response": "I can only answer medical questions!", "history": request.history}

    # Build conversation history
    conversation = f"<|system|>\n{config.SYSTEM_PROMPT}</s>\n"
    for turn in request.history:
        conversation += f"<|user|>\n{turn['user']}</s>\n<|assistant|>\n{turn['assistant']}</s>\n"
    conversation += f"<|user|>\n{request.message}</s>\n<|assistant|>"

    output = model(
        conversation,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_k=request.top_k,
        top_p=request.top_p,
        repeat_penalty=config.REPEAT_PENALTY
    )
    response = output["choices"][0]["text"].strip()
    logging.info(f"request_id={request_id} | endpoint=/chat | message={request.message} | response={response}")
    return {"request_id": request_id, "response": response, "history": request.history + [{"user": request.message, "assistant": response}]}

# ── Run ──
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)