from chromadb import PersistentClient
import os

def get_chroma_client():
    persist_dir = os.getenv("CHROMA_DB_DIR", "./chroma_db")
    return PersistentClient(path=persist_dir)

def get_or_create_collection(name="rag_docs"):
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"}
    )

 