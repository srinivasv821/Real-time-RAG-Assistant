import os
from chromadb import PersistentClient
from app.services.embedding_service import embed_text

_CLIENT = None

def get_client():
    global _CLIENT
    if _CLIENT is None:
        persist_dir = os.getenv("CHROMA_DB_DIR", "./chroma_db")
        os.makedirs(persist_dir, exist_ok=True)
        _CLIENT = PersistentClient(path=persist_dir)
    return _CLIENT

def get_collection(name: str = "documents"):
    client = get_client()
    return client.get_or_create_collection(name=name)

def similarity_search(
    query: str,
    top_k: int = 5,
    collection_name: str = "rag_docs"
):
    collection = get_collection(collection_name)

    # 🔑 IMPORTANT: embed query with SAME model (Instructor-XL)
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })

    return chunks
