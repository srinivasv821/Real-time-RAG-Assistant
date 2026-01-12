import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"  # or llama3.1:3b

SYSTEM_PROMPT = """
You are a helpful assistant.
Answer ONLY using the provided document context.
If the answer is not present in the context, say "I don't know".
Do not hallucinate.
"""

def generate_answer(query: str, context_chunks: list) -> str:
    context_text = "\n\n".join(
        f"[Chunk {i}] {c['text']}"
        for i, c in enumerate(context_chunks)
    )

    prompt = f"""
Context:
{context_text}

Question:
{query}

Answer:
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": SYSTEM_PROMPT + "\n" + prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    return response.json()["response"].strip()
