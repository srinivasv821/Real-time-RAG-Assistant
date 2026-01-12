from typing import List
from app.services.chunker import split_into_chunks
from app.services.embedding_service import embed_text
from app.services.chroma_service import get_collection
from app.db.session import SessionLocal
from app.db.models.document import Document

def process_document(doc_id: int, text: str):
    db = SessionLocal()
    try:
        # 1) Split into chunks
        chunks = split_into_chunks(text)

        if len(chunks) == 0:
            print("No chunks found!")
            return

        # 2) Generate embeddings
        vectors = [embed_text(chunk) for chunk in chunks]

        # 3) Store in ChromaDB
        collection = get_collection("rag_docs")

        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]

        metadata = [{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]

        collection.add(
            ids=ids,
            documents=chunks,
            embeddings=vectors,
            metadatas=metadata
        )

        # 4) Update Postgres
        doc = db.query(Document).get(doc_id)
        if doc:
            doc.processed = True
            db.commit()

        print(f"[RAG PIPELINE] Document {doc_id} processed. Chunks: {len(chunks)}")

    except Exception as e:
        print("[RAG PIPELINE ERROR]", e)

    finally:
        db.close()
