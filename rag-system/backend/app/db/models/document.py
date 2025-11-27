from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.session import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    uploaded_by = Column(String, nullable=True)  # username or user id
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(Text, nullable=True)  # extracted full text
    size_bytes = Column(Integer, nullable=True)
    processed = Column(Boolean, default=False)  # set True after chunk+embed
    extra_metadata = Column(Text, nullable=True)  # JSON string if required
