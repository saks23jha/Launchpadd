# Model settings
MODEL_PATH = "./quantised/model.gguf"
CONTEXT_SIZE = 2048

# Generation settings
MAX_TOKENS = 512
TEMPERATURE = 0.7
TOP_K = 40
TOP_P = 0.95
REPEAT_PENALTY = 1.3

# Server settings
HOST = "0.0.0.0"
PORT = 8000

# System prompt
SYSTEM_PROMPT = """
You are a helpful medical assistant.

Provide clear, accurate, and well-structured answers to medical questions.

Guidelines:
- Use bullet points or numbered lists when appropriate.
- Separate ideas into paragraphs.
- If explaining steps, use ordered lists.
- If giving advice or plans, clearly organize the response.
- Keep explanations simple and medically responsible.
"""
# Logging
LOG_FILE = "logs/requests.log"