# text extraction utilities
from pdfminer.high_level import extract_text
from typing import Optional
import os

def extract_text_from_pdf(path: str) -> str:
    """
    Extracts text from a PDF using pdfminer.six.
    Returns empty string on error.
    """
    try:
        text = extract_text(path)
        return text or ""
    except Exception as e:
        # log the error in production
        print(f"[doc_parser] pdf extraction error for {path}: {e}")
        return ""
