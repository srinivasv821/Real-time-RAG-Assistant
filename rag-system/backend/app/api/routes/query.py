from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chroma_service import similarity_search
from app.services.llm_service import generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    doc_id: int | None = None
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: list

@router.post("/query", response_model=QueryResponse)
def query_document(req: QueryRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

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

    answer = generate_answer(req.query, chunks)

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
