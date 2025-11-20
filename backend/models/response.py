"""
Pydantic models for API responses.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    status: str = Field(..., example="success")
    documents_indexed: int = Field(..., example=3)
    chunks_created: int = Field(..., example=156)
    embedding_provider: str = Field(..., example="Google (embedding-001)")
    llm_provider: str = Field(..., example="Gemini (gemini-2.0-flash-lite)")
    timestamp: datetime = Field(default_factory=datetime.now)


class SourceDocument(BaseModel):
    name: str = Field(..., example="policy.pdf")
    relevance_score: Optional[float] = Field(None, example=0.87)
    chunk_index: Optional[int] = Field(None)


class QueryResponse(BaseModel):
    answer: str = Field(..., description="Generated answer")
    sources: List[SourceDocument] = Field(..., description="Source documents")
    chunks_used: int = Field(..., example=5)
    model: str = Field(..., example="gemini-2.0-flash-lite")
    confidence: Optional[float] = Field(None, example=0.85)
    processing_time_ms: float = Field(..., example=1234.5)


class HealthResponse(BaseModel):
    status: str = Field(..., example="ok")
    embeddings: str = Field(..., example="Google (embedding-001)")
    llm: str = Field(..., example="Gemini (free tier)")
    documents_indexed: int = Field(default=0)
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    status: str = Field(..., example="error")
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, example="FILE_TOO_LARGE")
    timestamp: datetime = Field(default_factory=datetime.now)

