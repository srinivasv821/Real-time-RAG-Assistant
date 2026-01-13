import os
import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-3-8b-instruct"

def cloud_answer(query: str, context: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Real-time-RAG-Assistant"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Use the provided document context if relevant. "
                    "If the answer is not in the documents, answer using general knowledge. "
                    "If unsure, say 'I don't know'."
                )
            },
            {
                "role": "user",
                "content": f"""
Document Context:
{context}

Question:
{query}
"""
            }
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }

    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()

    return resp.json()["choices"][0]["message"]["content"].strip()
