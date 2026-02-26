from llama_cpp import Llama
import config

# Global model variable (caching)
model = None

def load_model():
    global model
    if model is None:
        print("Loading model...")
        model = Llama(
            model_path=config.MODEL_PATH,
            n_ctx=config.CONTEXT_SIZE,
            verbose=False
        )
        print("Model loaded ")
    return model