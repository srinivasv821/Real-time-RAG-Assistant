from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from fastapi import status
import os, shutil
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.db import crud_document
from app.services.doc_parser import extract_text_from_pdf
from app.db.models.document import Document
from termcolor import colored

router = APIRouter()

# Ensure uploads dir exists
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def process_document_background(doc_id: int, filepath: str):
    db = SessionLocal()
    print(colored("Inside BGG task", "green"))
    try:
        print(colored("try statement", "green"))
        text = extract_text_from_pdf(filepath)
        doc = db.query(Document).get(doc_id)
        if doc:
            doc.content = text
            db.commit()
    finally:
        db.close()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    uploaded_by: str = None,
    db: Session = Depends(get_db)
):  
    print(colored("CAME - 1", "green"))
    # Basic validation
    if not file.filename.lower().endswith((".pdf", ".docx", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF/DOCX/TXT allowed for now")
    print(colored("CAME - 2", "green"))
    # Save file
    dest_path = os.path.join(UPLOAD_DIR, f"{os.urandom(8).hex()}_{file.filename}")
    try:
        with open(dest_path, "wb") as out_file:
            shutil.copyfileobj(file.file, out_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to write file: {e}")
    finally:
        file.file.close()

    size_bytes = os.path.getsize(dest_path)
    print(colored("CAME - 3", "green"))
    # create DB record (content empty for now; will be filled in background)
    doc = crud_document.create_document(
        db=db,
        filename=file.filename,
        filepath=dest_path,
        size_bytes=size_bytes,
        uploaded_by=uploaded_by
    )

    # Kick background task to extract text (and later trigger chunk+embed)
    print(colored("CAME - 4", "green"))
    background_tasks.add_task(process_document_background, doc.id, dest_path)
    print(colored("CAME - 5", "green"))
    return {"doc_id": doc.id, "filename": doc.filename, "uploaded_at": str(doc.uploaded_at)}
