from sqlalchemy.orm import Session
from app.db.models.document import Document
from typing import Optional
from termcolor import colored

def create_document(db: Session, filename: str, filepath: str, size_bytes: int, uploaded_by: Optional[str]=None, content: Optional[str]=None, extra_metadata: Optional[str]=None):
    doc = Document(
        filename=filename,
        filepath=filepath,
        size_bytes=size_bytes,
        uploaded_by=uploaded_by,
        content=content or "",
        extra_metadata=extra_metadata
    )
    print(colored("SUB CAME - 1", "red"))
    db.add(doc)
    print(colored("SUB CAME - 2", "red"))
    db.commit()
    print(colored("SUB CAME - 3", "red"))
    db.refresh(doc)
    print(colored("SUB CAME - 4", "red"))
    return doc

def mark_processed(db: Session, doc_id: int):
    doc = db.query(Document).get(doc_id)
    if doc:
        doc.processed = True
        db.commit()
        db.refresh(doc)
    return doc

def get_document(db: Session, doc_id: int):
    return db.query(Document).filter(Document.id == doc_id).first()
