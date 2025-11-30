import re
from typing import List

def clean_text(text: str)->str:
    text = re.sub(r'\s+', ' ',text)
    return text.strip()

def split_into_chunks(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Splits text into chunks of `chunk_size` tokens with overlap.
    Assumes ~1 token per word for simplicity.
    """
    text = clean_text(text)
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks