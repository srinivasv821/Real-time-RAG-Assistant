from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chroma_service import similarity_search
from app.services.llm_service import generate_answer        # local (Ollama)
from app.services.cloud_llm_service import cloud_answer     # Groq (free cloud)


router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    mode: str = "private"  # "private" | "web"
    doc_id: int | None = None
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: list


def build_context(chunks: list, max_chars: int = 4000) -> str:
    context_parts = []
    used = 0

    for c in chunks:
        part = (
            f"[Document {c['metadata']['doc_id']}, "
            f"Chunk {c['metadata']['chunk_index']}]\n"
            f"{c['text']}"
        )
        if used + len(part) > max_chars:
            break
        context_parts.append(part)
        used += len(part)

    return "\n\n---\n\n".join(context_parts)


@router.post("/query", response_model=QueryResponse)
def query_document(req: QueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # 1️⃣ Retrieve chunks from Chroma
    chunks = similarity_search(req.query, req.top_k)

    # Optional: filter by document ID
    if req.doc_id is not None:
        chunks = [
            c for c in chunks
            if c["metadata"].get("doc_id") == req.doc_id
        ]

    if not chunks:
        return {
            "answer": "I don't know. The document does not contain relevant information.",
            "sources": []
        }

    # 2️⃣ PRIVATE MODE → local LLaMA (Ollama)
    if req.mode == "private":
        answer = generate_answer(req.query, chunks)

    # 3️⃣ WEB MODE → cloud LLM (Groq)
    elif req.mode == "web":
        context = build_context(chunks)
        answer = cloud_answer(req.query, context)

    else:
        raise HTTPException(status_code=400, detail="Invalid mode")

    # 4️⃣ Sources (same for both modes)
    sources = [
        {
            "doc_id": c["metadata"]["doc_id"],
            "chunk_index": c["metadata"]["chunk_index"]
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "sources": sources
    }
