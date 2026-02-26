
import torch, time, os
from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from llama_cpp import Llama

# Config
BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
FINETUNED_MODEL = "/content/quantized/model-fp16" if os.path.exists("/content") else "./quantised/model-fp16"
GGUF_MODEL = "/content/quantized/model.gguf" if os.path.exists("/content") else "./quantised/model.gguf"
PROMPT = """<|system|>
If you are a doctor, please answer the medical questions based on the patient description.</s>
<|user|>
I have been feeling very thirsty and urinating frequently. What could be wrong?</s>
<|assistant|>"""

BATCH_PROMPTS = ["What is diabetes?", "What are symptoms of high blood pressure?", "How to treat fever?"]
MULTI_PROMPTS = ["What is insulin?", "What causes high cholesterol?", "How to control blood sugar?", "What are symptoms of heart attack?", "How to reduce stress?"]

# # Load HuggingFace Model
# def load_model(path):
#     model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float16, device_map="auto")
def load_model(path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(path, dtype=torch.float16, device_map=device)
    tokenizer = AutoTokenizer.from_pretrained(path)
    tokenizer.pad_token = tokenizer.eos_token
    return model, tokenizer

# Generate response
def generate(model, tokenizer, prompt, max_tokens=100):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    input_len = inputs["input_ids"].shape[1]
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=max_tokens, repetition_penalty=1.3, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(output[0][input_len:], skip_special_tokens=True).strip(), len(output[0][input_len:])

# # Benchmark
# def benchmark(name, model, tokenizer):
#     print(f"\n=== Benchmark: {name} ===")
#     torch.cuda.reset_peak_memory_stats()
#     start = time.time()
#     response, num_tokens = generate(model, tokenizer, PROMPT)
#     latency = round(time.time() - start, 2)
#     print(f"Latency: {latency}s | Tokens/sec: {round(num_tokens/latency, 2)} | VRAM: {round(torch.cuda.max_memory_allocated()/1e9, 2)}GB")
#     print(f"Response: {response}")
# Benchmark
def benchmark(name, model, tokenizer):
    print(f"\n=== Benchmark: {name} ===")
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    start = time.time()
    response, num_tokens = generate(model, tokenizer, PROMPT)
    latency = round(time.time() - start, 2)
    vram = round(torch.cuda.max_memory_allocated() / 1e9, 2) if torch.cuda.is_available() else 0.0
    print(f"Latency: {latency}s | Tokens/sec: {round(num_tokens/latency, 2)} | VRAM: {vram}GB")
    print(f"Response: {response}")

def benchmark_gguf(gguf):
    print("\n=== Benchmark: GGUF ===")
    start = time.time()
    out = gguf(PROMPT, max_tokens=100, repeat_penalty=1.3)
    latency = round(time.time() - start, 2)
    print(f"Latency: {latency}s | Tokens/sec: {round(out['usage']['completion_tokens']/latency, 2)}")
    print(f"Response: {out['choices'][0]['text'].strip()}")

# Streaming
def streaming(name, model, tokenizer):
    print(f"\n=== Streaming: {name} ===")
    inputs = tokenizer(PROMPT, return_tensors="pt").to(model.device)
    streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
    with torch.no_grad():
        model.generate(**inputs, max_new_tokens=100, repetition_penalty=1.3, pad_token_id=tokenizer.eos_token_id, streamer=streamer)

def streaming_gguf(gguf):
    print("\n=== Streaming: GGUF ===")
    for chunk in gguf(PROMPT, max_tokens=100, repeat_penalty=1.3, stream=True):
        print(chunk["choices"][0]["text"], end="", flush=True)
    print()

# Batch Inference
def batch_inference(name, model, tokenizer):
    print(f"\n=== Batch Inference: {name} ===")
    inputs = tokenizer(BATCH_PROMPTS, return_tensors="pt", padding=True, truncation=True).to(model.device)
    start = time.time()
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=50, repetition_penalty=1.3, pad_token_id=tokenizer.eos_token_id)
    print(f"Batch time: {round(time.time()-start, 2)}s")
    for i, out in enumerate(outputs):
        print(f"Q{i+1}: {BATCH_PROMPTS[i]} -> {tokenizer.decode(out, skip_special_tokens=True)}")

def batch_inference_gguf(gguf):
    print("\n=== Batch Inference: GGUF ===")
    start = time.time()
    for i, p in enumerate(BATCH_PROMPTS):
        print(f"Q{i+1}: {p} -> {gguf(f'Question: {p} Answer:', max_tokens=50, repeat_penalty=1.3)['choices'][0]['text'].strip()}")
    print(f"Batch time: {round(time.time()-start, 2)}s")

# Multi-prompt Test
def multi_prompt_test(name, model, tokenizer):
    print(f"\n=== Multi-prompt: {name} ===")
    for i, p in enumerate(MULTI_PROMPTS):
        response, _ = generate(model, tokenizer, p, max_tokens=50)
        print(f"Q{i+1}: {p} -> {response}")

def multi_prompt_test_gguf(gguf):
    print("\n=== Multi-prompt: GGUF ===")
    for i, p in enumerate(MULTI_PROMPTS):
        print(f"Q{i+1}: {p} -> {gguf(f'Question: {p} Answer:', max_tokens=50, repeat_penalty=1.3)['choices'][0]['text'].strip()}")

# Main
if __name__ == "__main__":
    # Base Model
    base_model, base_tokenizer = load_model(BASE_MODEL)
    benchmark("Base Model", base_model, base_tokenizer)
    streaming("Base Model", base_model, base_tokenizer)
    batch_inference("Base Model", base_model, base_tokenizer)
    multi_prompt_test("Base Model", base_model, base_tokenizer)

    # Fine-tuned Model
    ft_model, ft_tokenizer = load_model(FINETUNED_MODEL)
    benchmark("Fine-tuned Model", ft_model, ft_tokenizer)
    streaming("Fine-tuned Model", ft_model, ft_tokenizer)
    batch_inference("Fine-tuned Model", ft_model, ft_tokenizer)
    multi_prompt_test("Fine-tuned Model", ft_model, ft_tokenizer)

    # GGUF Model
    gguf = Llama(model_path=GGUF_MODEL, n_ctx=512, verbose=False)
    benchmark_gguf(gguf)
    streaming_gguf(gguf)
    batch_inference_gguf(gguf)
    multi_prompt_test_gguf(gguf)
    del gguf

    print("\nAll done ")
