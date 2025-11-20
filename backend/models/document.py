"""
Pydantic models for document handling.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    source: str = Field(..., description="Original file name")
    file_type: str = Field(..., description="File extension")
    pages: Optional[int] = Field(None, description="Page count for PDFs")
    paragraphs: Optional[int] = Field(None, description="Paragraph count for DOCX")
    lines: Optional[int] = Field(None, description="Line count for TXT")
    indexed_at: datetime = Field(default_factory=datetime.now)
    chunk_count: int = Field(default=0, description="Number of generated chunks")


class Document(BaseModel):
    id: str = Field(..., description="Unique document ID")
    name: str = Field(..., description="Document name")
    content: str = Field(..., description="Document text content")
    metadata: DocumentMetadata
    size_bytes: int = Field(..., description="File size in bytes")

