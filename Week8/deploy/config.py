# Model settings
MODEL_PATH = "./quantised/model.gguf"
CONTEXT_SIZE = 512

# Generation settings
MAX_TOKENS = 200
TEMPERATURE = 0.7
TOP_K = 40
TOP_P = 0.95
REPEAT_PENALTY = 1.3

# Server settings
HOST = "0.0.0.0"
PORT = 8000

# System prompt
SYSTEM_PROMPT = "You are a helpful medical assistant. Answer the patient's questions based on their description."

# Logging
LOG_FILE = "logs/requests.log"