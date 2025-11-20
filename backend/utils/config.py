"""
Configuration management for DocBot application.
"""
from typing import List
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file from the backend directory
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / ".env"

# Try to load .env file
if env_path.exists():
    load_dotenv(env_path, override=True)
else:
    import warnings
    warnings.warn(f".env file not found at {env_path}. Please create it by copying env.example")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google API Configuration (for LLM only, embeddings are now local)
    google_api_key: str
    google_llm_model: str = "models/gemini-2.5-flash"
    google_embedding_model: str | None = None  # Deprecated - kept for backward compatibility
    
    # Embedding Configuration (local HuggingFace model)
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"  # Fast, good quality, ~80MB

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Storage Configuration
    documents_dir: str = "./documents"
    chroma_db_dir: str = "./chroma_db"
    max_file_size_mb: int = 50
    allowed_file_types: str = "pdf,docx,txt,png,jpg,jpeg"

    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retriever_k: int = 5
    temperature: float = 0.3

    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "./logs/docbot.log"

    class Config:
        env_file = str(env_path) if env_path.exists() else ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file (like old GOOGLE_EMBEDDING_MODEL)

    @property
    def allowed_extensions(self) -> List[str]:
        """Return list of allowed file extensions."""
        return self.allowed_file_types.split(",")

    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size to bytes."""
        return self.max_file_size_mb * 1024 * 1024


settings = Settings()  # type: ignore

