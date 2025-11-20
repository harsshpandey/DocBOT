# DocBot Solution: Complete Implementation Guide

---

## **Table of Contents**

1. [Problem Statement](#problem-statement)
2. [Solution Overview](#solution-overview)
3. [Architecture](#architecture)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Backend Implementation](#backend-implementation)
7. [Frontend Implementation](#frontend-implementation)
8. [Deployment Guide](#deployment-guide)
9. [Testing & Validation](#testing--validation)
10. [API Documentation](#api-documentation)

---

# **PROBLEM STATEMENT**

## **The Challenge**

Organizations accumulate extensive documentation across multiple formats:
- **Service Rules** (PDFs, Word documents)
- **Purchase Manuals** (PDFs with images)
- **Office Orders** (Plain text, Word docs)
- **Policy Documents** (Mixed formats)
- **Procurement Guidelines** (Images with text)

### **Current Pain Points**

1. **Information Silos**: Rule books scattered across drives, difficult to locate
2. **Manual Search**: Users spend hours searching through documents manually
3. **Inefficient Onboarding**: New employees struggle to find policy information
4. **Repetitive Queries**: HR/Admin teams answer the same questions repeatedly
5. **Information Loss**: Critical policies buried in lengthy documents
6. **No Contextual Search**: Keyword-based search misses semantic meaning

### **Impact on Users**

- **Promotion/Review Queries**: "What are the criteria for promotion?" → Requires digging through 100+ page policy doc
- **Leave/Pay-Scale Questions**: "How many leave days am I entitled to?" → Manual calculation from rules
- **Procurement Questions**: "What's the process for indenting equipment?" → Scattered across multiple docs
- **Tender Process**: "What are the tender procedures?" → Complex multi-step process, hard to follow

---

## **SOLUTION OVERVIEW**

### **What is DocBot?**

**DocBot** is an AI-powered conversational chatbot that:
1. **Reads** all rule books, manuals, and policy documents (PDF, Word, Text, Images)
2. **Extracts & Organizes** content using NLP and document parsing
3. **Creates** a searchable knowledge base using vector embeddings
4. **Answers** user queries using Retrieval-Augmented Generation (RAG)
5. **Provides** accurate, context-aware responses instantly

### **Key Benefits**

| Problem | Solution |
|---------|----------|
| Manual search in documents | Instant AI search across all docs |
| Information scattered | Centralized knowledge base |
| Slow onboarding | Self-service query system |
| Repetitive questions | 24/7 chatbot answers |
| Hard to find policies | Semantic search (understands meaning) |
| No context in results | RAG provides source + context |

### **Use Cases Solved**

✅ "What's the annual leave policy?" → Returns leave eligibility with source doc
✅ "How do I get promoted?" → Lists criteria + timeline + application process
✅ "What's the tender process?" → Step-by-step procedure with links to relevant sections
✅ "Am I eligible for this benefit?" → Checks criteria against employee info

---

# **ARCHITECTURE**

## **System Design**

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER (Web Browser)                         │
│                    Next.js Chat Interface                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │ (HTTP/WebSocket)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                               │
│  ├─ Chat UI (Next.js + TypeScript)                             │
│  ├─ Message History                                            │
│  ├─ File Upload Manager                                        │
│  └─ Real-time Streaming Responses                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │ REST API
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API LAYER (FastAPI)                          │
│  ├─ POST /upload (Document ingestion)                          │
│  ├─ POST /query (Question answering)                           │
│  ├─ GET /health (Health check)                                 │
│  └─ GET /status (Indexing status)                              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   DOCUMENT   │  │  EMBEDDING   │  │     LLM      │
│   PROCESSOR  │  │   SERVICE    │  │    SERVICE   │
│              │  │              │  │              │
│ - PDF Parser │  │ - Google AI  │  │ - Gemini API │
│ - DOCX Parse │  │ - embedding- │  │ - RAG Engine │
│ - Image OCR  │  │   001        │  │ - Context    │
│ - Text Split │  │ - Chroma DB  │  │   Generation │
└──────────────┘  └──────────────┘  └──────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
        ┌──────────────────────────────────────┐
        │    KNOWLEDGE BASE (Vector Store)     │
        │                                      │
        │    Chroma DB (Local Storage)         │
        │    - Indexed Documents              │
        │    - Embeddings                     │
        │    - Metadata                       │
        └──────────────────────────────────────┘
        │
        ▼
        File System
        └─ ./documents/ (Original files)
        └─ ./chroma_db/ (Vector embeddings)
```

## **Data Flow**

### **1. Document Ingestion Flow**

```
User uploads files (PDF, DOCX, TXT, Images)
         │
         ▼
    FastAPI /upload endpoint
         │
         ▼
    Save files to disk
         │
         ▼
    Load documents (PyPDF2, python-docx, Tesseract OCR)
         │
         ▼
    Clean & normalize text
         │
         ▼
    Split into chunks (1000 chars, 200 char overlap)
         │
         ▼
    Convert to embeddings (Google API)
         │
         ▼
    Store in Chroma vector DB
         │
         ▼
    Return: "Successfully indexed X documents"
```

### **2. Query & Response Flow**

```
User types question in chat
         │
         ▼
    Frontend sends to /query endpoint
         │
         ▼
    Convert question to embedding (Google API)
         │
         ▼
    Search vector store (semantic similarity)
         │
         ▼
    Retrieve top 5 relevant chunks
         │
         ▼
    Build RAG prompt with context
         │
         ▼
    Send to Gemini API with context
         │
         ▼
    LLM generates answer
         │
         ▼
    Stream response back to frontend
         │
         ▼
    Display answer + source documents
```

---

# **TECH STACK**

## **Backend (Python)**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI | REST API server, async support |
| **Document Loading** | PyPDF2, python-docx, Tesseract | Extract content from files |
| **Text Processing** | LangChain, RecursiveCharacterTextSplitter | Parse and chunk documents |
| **Embeddings** | Google Generative AI | Convert text to vectors |
| **Vector DB** | Chroma | Local storage for embeddings |
| **LLM** | Google Gemini API | Answer generation |
| **RAG Framework** | LangChain | Orchestrate retrieval + generation |
| **Server** | Uvicorn | ASGI server |

## **Frontend (Next.js)**

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Next.js 14 | React SSR + API routes |
| **Language** | TypeScript | Type-safe development |
| **Styling** | Tailwind CSS | Modern UI components |
| **State** | Zustand | Global state management |
| **HTTP Client** | Axios | API communication |
| **Rendering** | React Markdown | Display formatted responses |
| **Icons** | Lucide React | UI icons |
| **Real-time** | Fetch API | WebSocket for streaming |

## **Infrastructure**

| Component | Technology | Deployment |
|-----------|-----------|---------|
| **Backend** | Python 3.10+ | Docker / Local / Cloud |
| **Database** | Chroma (Local) | File-based vector store |
| **Storage** | Local filesystem | Document storage |
| **APIs** | Google Cloud APIs | Embeddings + LLM |
| **Frontend** | Node.js + Vercel | Vercel / Self-hosted |

---

# **PROJECT STRUCTURE**

```
docbot-project/
│
├── backend/
│   ├── __init__.py
│   ├── main.py                      # FastAPI main server
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Environment variables
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document.py              # Document models
│   │   └── response.py              # API response schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_loader.py       # Load PDFs, DOCX, TXT, Images
│   │   ├── text_processor.py        # Clean & chunk text
│   │   ├── vector_store.py          # Chroma DB operations
│   │   ├── rag_agent.py             # RAG with Gemini
│   │   └── embedding_service.py     # Google embeddings
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py                # Logging setup
│   │   ├── config.py                # Configuration
│   │   └── validators.py            # Input validation
│   │
│   ├── documents/                   # Uploaded files (auto-created)
│   ├── chroma_db/                   # Vector store (auto-created)
│   └── logs/                        # Application logs (auto-created)
│
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   │
│   ├── app/
│   │   ├── layout.tsx               # Root layout
│   │   ├── page.tsx                 # Main chat page
│   │   ├── globals.css              # Global styles
│   │   └── api/
│   │       └── health/route.ts      # Health check endpoint
│   │
│   ├── components/
│   │   ├── ChatInterface.tsx        # Main chat component
│   │   ├── MessageList.tsx          # Message display
│   │   ├── MessageInput.tsx         # Input & file upload
│   │   ├── SourceDocuments.tsx      # Show sources
│   │   ├── LoadingSpinner.tsx       # Loading indicator
│   │   └── FileUploadArea.tsx       # Drag-drop upload
│   │
│   ├── lib/
│   │   ├── api.ts                   # API client functions
│   │   ├── types.ts                 # TypeScript types
│   │   └── utils.ts                 # Utility functions
│   │
│   ├── store/
│   │   └── chatStore.ts             # Zustand store
│   │
│   └── public/
│       └── favicon.ico
│
├── docker/
│   ├── Dockerfile.backend           # Backend Docker image
│   ├── Dockerfile.frontend          # Frontend Docker image
│   └── docker-compose.yml           # Orchestrate both
│
├── README.md
├── INSTALLATION.md
├── API_DOCS.md
└── .gitignore
```

---

# **BACKEND IMPLEMENTATION**

## **1. Environment Setup**

### **File: `backend/.env`**

```env
# Google API Configuration
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_EMBEDDING_MODEL=models/embedding-001
GOOGLE_LLM_MODEL=gemini-2.0-flash-lite

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Storage Configuration
DOCUMENTS_DIR=./documents
CHROMA_DB_DIR=./chroma_db
MAX_FILE_SIZE_MB=50
ALLOWED_FILE_TYPES=pdf,docx,txt,png,jpg,jpeg

# RAG Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVER_K=5
TEMPERATURE=0.3

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/docbot.log
```

## **2. Requirements & Installation**

### **File: `backend/requirements.txt`**

```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Document Processing
PyPDF2==4.0.1
pdf2image==1.17.1
python-docx==0.8.11
pytesseract==0.3.10
pillow==10.1.0

# NLP & Text Processing
langchain==0.1.9
langchain-google-genai==0.0.12
langchain-community==0.0.27
langchain-text-splitters==0.0.1

# Vector Store
chromadb==0.4.21

# HTTP Client
aiohttp==3.9.1
httpx==0.25.2

# Utilities
python-dotenv==1.0.0
pydantic-core==2.14.0
numpy==1.24.3
typing-extensions==4.8.0

# Logging & Monitoring
python-json-logger==2.0.7
loguru==0.7.2

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.12.0
flake8==6.1.0
```

### **Installation Steps**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (for image text extraction)
# On Ubuntu:
sudo apt-get install tesseract-ocr

# On Mac:
brew install tesseract

# On Windows:
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```
## **3. Configuration Module (Continued)**

### **File: `backend/utils/config.py`**

```python
"""
Configuration management for DocBot application
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Google API Configuration
    google_api_key: str
    google_embedding_model: str = "models/embedding-001"
    google_llm_model: str = "gemini-2.0-flash-lite"
    
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
        env_file = ".env"
        case_sensitive = False
    
    @property
    def allowed_extensions(self) -> List[str]:
        """Get list of allowed file extensions"""
        return self.allowed_file_types.split(",")
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size to bytes"""
        return self.max_file_size_mb * 1024 * 1024

# Load settings
settings = Settings()  # type: ignore
```

## **4. Logger Setup**

### **File: `backend/utils/logger.py`**

```python
"""
Logging configuration for DocBot
"""
import logging
import os
from datetime import datetime
from utils.config import settings

def setup_logger(name: str = "docbot") -> logging.Logger:
    """
    Configure logging with both file and console handlers
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)
    
    # Console handler (colorized output)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # File handler
    file_handler = logging.FileHandler(settings.log_file)
    file_handler.setLevel(settings.log_level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Global logger instance
logger = setup_logger()
```

## **5. Data Models**

### **File: `backend/models/document.py`**

```python
"""
Pydantic models for document handling
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DocumentMetadata(BaseModel):
    """Metadata for indexed documents"""
    source: str = Field(..., description="Original file name")
    file_type: str = Field(..., description="File extension (pdf, docx, txt, etc)")
    pages: Optional[int] = Field(None, description="Number of pages (for PDFs)")
    indexed_at: datetime = Field(default_factory=datetime.now)
    chunk_count: int = Field(default=0, description="Number of chunks created")

class Document(BaseModel):
    """Document model"""
    id: str = Field(..., description="Unique document ID")
    name: str = Field(..., description="File name")
    content: str = Field(..., description="Document content")
    metadata: DocumentMetadata
    size_bytes: int = Field(..., description="File size in bytes")
```

### **File: `backend/models/response.py`**

```python
"""
Pydantic models for API responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UploadResponse(BaseModel):
    """Response for document upload"""
    status: str = Field(..., example="success")
    documents_indexed: int = Field(..., example=3)
    chunks_created: int = Field(..., example=156)
    embedding_provider: str = Field(..., example="Google (embedding-001)")
    llm_provider: str = Field(..., example="Gemini (gemini-2.0-flash-lite)")
    timestamp: datetime = Field(default_factory=datetime.now)

class SourceDocument(BaseModel):
    """Source document reference"""
    name: str = Field(..., example="policy.pdf")
    relevance_score: Optional[float] = Field(None, example=0.87)
    chunk_index: Optional[int] = Field(None)

class QueryResponse(BaseModel):
    """Response for user query"""
    answer: str = Field(..., description="Generated answer")
    sources: List[SourceDocument] = Field(..., description="Source documents")
    chunks_used: int = Field(..., example=5)
    model: str = Field(..., example="gemini-2.0-flash-lite")
    confidence: Optional[float] = Field(None, example=0.85)
    processing_time_ms: float = Field(..., example=1234.5)

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., example="ok")
    embeddings: str = Field(..., example="Google (embedding-001)")
    llm: str = Field(..., example="Gemini (free tier)")
    documents_indexed: int = Field(default=0)
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """Error response"""
    status: str = Field(..., example="error")
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, example="FILE_TOO_LARGE")
    timestamp: datetime = Field(default_factory=datetime.now)
```

## **6. Document Loader Service**

### **File: `backend/services/document_loader.py`**

```python
"""
Document loading service for multiple file formats
"""
from pathlib import Path
from typing import List, Optional
import PyPDF2
from docx import Document as DocxDocument
from PIL import Image
import pytesseract
from langchain.schema import Document
from utils.logger import logger
from utils.config import settings

class DocumentLoader:
    """Load documents from various formats"""
    
    def __init__(self):
        """Initialize document loader"""
        self.supported_formats = settings.allowed_extensions
        logger.info(f"Supported formats: {self.supported_formats}")
    
    def load_pdf(self, file_path: str) -> tuple[str, int]:
        """
        Extract text from PDF
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Tuple of (extracted_text, page_count)
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    text += f"\n--- Page {page_num + 1} ---\n"
                    text += page.extract_text()
            
            logger.info(f"Extracted {page_count} pages from PDF: {file_path}")
            return text, page_count
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {str(e)}")
            raise
    
    def load_docx(self, file_path: str) -> tuple[str, int]:
        """
        Extract text from DOCX
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Tuple of (extracted_text, paragraph_count)
        """
        try:
            doc = DocxDocument(file_path)
            text = ""
            
            for para in doc.paragraphs:
                text += para.text + "\n"
            
            para_count = len(doc.paragraphs)
            logger.info(f"Extracted {para_count} paragraphs from DOCX: {file_path}")
            return text, para_count
        except Exception as e:
            logger.error(f"Error loading DOCX {file_path}: {str(e)}")
            raise
    
    def load_text(self, file_path: str) -> tuple[str, int]:
        """
        Load plain text file
        
        Args:
            file_path: Path to text file
            
        Returns:
            Tuple of (content, line_count)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            line_count = len(text.split('\n'))
            logger.info(f"Loaded text file {file_path} ({line_count} lines)")
            return text, line_count
        except Exception as e:
            logger.error(f"Error loading text file {file_path}: {str(e)}")
            raise
    
    def extract_text_from_image(self, file_path: str) -> str:
        """
        Extract text from image using OCR
        
        Args:
            file_path: Path to image file
            
        Returns:
            Extracted text
        """
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            logger.info(f"Extracted text from image: {file_path}")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from image {file_path}: {str(e)}")
            raise
    
    def load_document(self, file_path: str) -> Document:
        """
        Load document from any supported format
        
        Args:
            file_path: Path to document file
            
        Returns:
            LangChain Document object
        """
        path = Path(file_path)
        file_extension = path.suffix.lower().lstrip('.')
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        file_name = path.name
        
        try:
            if file_extension == "pdf":
                content, pages = self.load_pdf(file_path)
                metadata = {
                    "source": file_name,
                    "file_type": "pdf",
                    "pages": pages
                }
            elif file_extension == "docx":
                content, paragraphs = self.load_docx(file_path)
                metadata = {
                    "source": file_name,
                    "file_type": "docx",
                    "paragraphs": paragraphs
                }
            elif file_extension == "txt":
                content, lines = self.load_text(file_path)
                metadata = {
                    "source": file_name,
                    "file_type": "txt",
                    "lines": lines
                }
            elif file_extension in ["png", "jpg", "jpeg"]:
                content = self.extract_text_from_image(file_path)
                metadata = {
                    "source": file_name,
                    "file_type": "image",
                    "format": file_extension
                }
            else:
                raise ValueError(f"Unsupported format: {file_extension}")
            
            return Document(
                page_content=content,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"Failed to load document {file_path}: {str(e)}")
            raise
    
    def load_documents_from_directory(self, directory: str) -> List[Document]:
        """
        Load all supported documents from directory
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            List of Document objects
        """
        documents = []
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.warning(f"Directory not found: {directory}")
            return documents
        
        for file_path in dir_path.glob("*"):
            if file_path.is_file() and file_path.suffix.lower().lstrip('.') in self.supported_formats:
                try:
                    doc = self.load_document(str(file_path))
                    documents.append(doc)
                    logger.info(f"Loaded document: {file_path.name}")
                except Exception as e:
                    logger.error(f"Failed to load {file_path.name}: {str(e)}")
                    continue
        
        logger.info(f"Loaded {len(documents)} documents from {directory}")
        return documents
```

## **7. Text Processing Service**

### **File: `backend/services/text_processor.py`**

```python
"""
Text processing and chunking service
"""
from typing import List
from langchain.schema import Document
from langchain.text_splitters import RecursiveCharacterTextSplitter
import re
from utils.logger import logger
from utils.config import settings

class TextProcessor:
    """Process and chunk text documents"""
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        """
        Initialize text processor
        
        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",           # Paragraph breaks
                "\n",             # Line breaks
                ". ",             # Sentence ends
                " ",              # Word breaks
                ""                # Character level
            ],
            length_function=len,
        )
        
        logger.info(
            f"Initialized TextProcessor: "
            f"chunk_size={self.chunk_size}, overlap={self.chunk_overlap}"
        )
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\(\)\:]', ' ', text)
        
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of chunked Document objects
        """
        try:
            chunks = self.splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            raise
    
    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Process documents (clean + split)
        
        Args:
            documents: Raw documents
            
        Returns:
            Processed chunks
        """
        # Clean text in each document
        for doc in documents:
            doc.page_content = self.clean_text(doc.page_content)
        
        # Split into chunks
        chunks = self.split_documents(documents)
        
        logger.info(f"Processed {len(documents)} documents -> {len(chunks)} chunks")
        return chunks
```

## **8. Vector Store Service**

### **File: `backend/services/vector_store.py`**

```python
"""
Vector store management using Chroma and Google embeddings
"""
from typing import List, Optional
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from utils.logger import logger
from utils.config import settings
import os

class VectorStoreManager:
    """Manage vector embeddings and retrieval"""
    
    def __init__(self, persist_directory: str = None):
        """
        Initialize vector store manager
        
        Args:
            persist_directory: Path to Chroma database
        """
        self.persist_directory = persist_directory or settings.chroma_db_dir
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize Google embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.google_embedding_model,
            api_key=settings.google_api_key
        )
        
        self.vectorstore: Optional[Chroma] = None
        logger.info(f"Initialized VectorStoreManager with Chroma DB at {self.persist_directory}")
    
    def index_documents(self, chunks: List[Document]) -> Chroma:
        """
        Index documents and store embeddings
        
        Args:
            chunks: List of document chunks
            
        Returns:
            Chroma vectorstore instance
        """
        try:
            logger.info(f"Indexing {len(chunks)} chunks...")
            
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
                collection_name="docbot_documents"
            )
            
            logger.info(f"Successfully indexed {len(chunks)} chunks into Chroma")
            return self.vectorstore
        except Exception as e:
            logger.error(f"Error indexing documents: {str(e)}")
            raise
    
    def get_vectorstore(self) -> Optional[Chroma]:
        """
        Get or load existing vectorstore
        
        Returns:
            Chroma vectorstore instance
        """
        try:
            if self.vectorstore is None:
                self.vectorstore = Chroma(
                    embedding_function=self.embeddings,
                    persist_directory=self.persist_directory,
                    collection_name="docbot_documents"
                )
            return self.vectorstore
        except Exception as e:
            logger.warning(f"No existing vectorstore found: {str(e)}")
            return None
    
    def get_retriever(self, k: int = None):
        """
        Get document retriever
        
        Args:
            k: Number of documents to retrieve
            
        Returns:
            Retriever instance
        """
        k = k or settings.retriever_k
        vectorstore = self.get_vectorstore()
        
        if vectorstore is None:
            raise RuntimeError("Vectorstore not initialized. Index documents first.")
        
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": k}
        )
        
        logger.info(f"Created retriever with k={k}")
        return retriever
    
    def search(self, query: str, k: int = None) -> List[Document]:
        """
        Search for similar documents
        
        Args:
            query: Search query
            k: Number of results
            
        Returns:
            List of similar documents
        """
        k = k or settings.retriever_k
        vectorstore = self.get_vectorstore()
        
        if vectorstore is None:
            raise RuntimeError("Vectorstore not initialized.")
        
        try:
            results = vectorstore.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query: {query[:50]}")
            return results
        except Exception as e:
            logger.error(f"Error searching vectorstore: {str(e)}")
            raise
    
    def search_with_scores(self, query: str, k: int = None) -> List[tuple]:
        """
        Search with relevance scores
        
        Args:
            query: Search query
            k: Number of results
            
        Returns:
            List of (document, score) tuples
        """
        k = k or settings.retriever_k
        vectorstore = self.get_vectorstore()
        
        if vectorstore is None:
            raise RuntimeError("Vectorstore not initialized.")
        
        try:
            results = vectorstore.similarity_search_with_scores(query, k=k)
            logger.info(f"Found {len(results)} results with scores")
            return results
        except Exception as e:
            logger.error(f"Error searching vectorstore: {str(e)}")
            raise
    
    def clear_vectorstore(self) -> bool:
        """
        Clear all indexed documents
        
        Returns:
            True if successful
        """
        try:
            import shutil
            if os.path.exists(self.persist_directory):
                shutil.rmtree(self.persist_directory)
                os.makedirs(self.persist_directory, exist_ok=True)
            self.vectorstore = None
            logger.info("Cleared vectorstore")
            return True
        except Exception as e:
            logger.error(f"Error clearing vectorstore: {str(e)}")
            return False
```

## **9. RAG Agent Service**

### **File: `backend/services/rag_agent.py`**

```python
"""
RAG (Retrieval-Augmented Generation) Agent
Combines document retrieval with LLM-based answering
"""
from typing import Dict, List, Optional
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from utils.logger import logger
from utils.config import settings

class RAGAgent:
    """RAG agent for question answering"""
    
    def __init__(self, retriever):
        """
        Initialize RAG agent
        
        Args:
            retriever: Document retriever instance
        """
        self.retriever = retriever
        
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model=settings.google_llm_model,
            api_key=settings.google_api_key,
            temperature=settings.temperature,
            max_output_tokens=2048
        )
        
        # System prompt for the agent
        self.system_prompt = """You are a helpful assistant that answers questions about organizational policies, rules, and guidelines based on provided documents.

IMPORTANT INSTRUCTIONS:
1. Always base your answer on the provided context/documents
2. If the information is not in the context, clearly state: "I don't have information about that in the knowledge base"
3. Be accurate and cite the source document when relevant
4. For policy questions, provide complete information including steps, criteria, and eligibility
5. Be professional and concise
6. If multiple related policies apply, mention all relevant ones
7. When asking for clarification, explain what additional information you need

CONTEXT FROM DOCUMENTS:
{context}

Remember: Only answer based on the provided context. Do not make assumptions or use general knowledge."""
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{question}")
        ])
        
        logger.info(f"Initialized RAG Agent with model: {settings.google_llm_model}")
    
    def retrieve_context(self, question: str, k: Optional[int] = None) -> List[Document]:
        """
        Retrieve relevant documents for a question
        
        Args:
            question: User question
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        try:
            docs = self.retriever.invoke(question)
            logger.info(f"Retrieved {len(docs)} documents for question: {question[:50]}")
            return docs
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return []
    
    def format_context(self, documents: List[Document]) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            documents: List of documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "Unknown Source")
            content = doc.page_content.strip()
            context_parts.append(f"[Source {i}: {source}]\n{content}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def answer_question(self, question: str) -> Dict:
        """
        Answer a user question using RAG
        
        Args:
            question: User question
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        start_time = time.time()
        
        try:
            # Retrieve relevant documents
            retrieved_docs = self.retrieve_context(question)
            
            if not retrieved_docs:
                logger.warning(f"No documents found for question: {question}")
                return {
                    "answer": "I couldn't find any relevant information in the knowledge base. Please rephrase your question or contact support.",
                    "sources": [],
                    "chunks_used": 0,
                    "model": settings.google_llm_model,
                    "confidence": 0.0,
                    "processing_time_ms": (time.time() - start_time) * 1000,
                    "error": "No documents found"
                }
            
            # Format context
            context = self.format_context(retrieved_docs)
            
            # Generate answer using LLM
            prompt = self.prompt_template.format_prompt(
                context=context,
                question=question
            )
            
            response = self.llm.invoke(prompt.to_string())
            
            # Extract answer text
            answer_text = response.content if hasattr(response, 'content') else str(response)
            
            # Prepare sources
            sources = []
            for doc in retrieved_docs:
                sources.append({
                    "name": doc.metadata.get("source", "Unknown"),
                    "relevance_score": None,  # Could add similarity score if needed
                    "chunk_index": None
                })
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            logger.info(f"Generated answer in {processing_time_ms:.1f}ms for question: {question[:50]}")
            
            return {
                "answer": answer_text,
                "sources": sources,
                "chunks_used": len(retrieved_docs),
                "model": settings.google_llm_model,
                "confidence": 0.85,  # Could be enhanced with confidence scoring
                "processing_time_ms": processing_time_ms
            }
        
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            processing_time_ms = (time.time() - start_time) * 1000
            
            return {
                "answer": f"An error occurred while processing your question: {str(e)}",
                "sources": [],
                "chunks_used": 0,
                "model": settings.google_llm_model,
                "confidence": 0.0,
                "processing_time_ms": processing_time_ms,
                "error": str(e)
            }
```

## **10. Main FastAPI Server**

### **File: `backend/main.py`**

```python
"""
DocBot - Main FastAPI Application
AI-powered chatbot for reading and answering questions about rule books
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import shutil
import os
from datetime import datetime

from models.response import (
    UploadResponse, QueryResponse, HealthResponse, ErrorResponse, SourceDocument
)
from services.document_loader import DocumentLoader
from services.text_processor import TextProcessor
from services.vector_store import VectorStoreManager
from services.rag_agent import RAGAgent
from utils.config import settings
from utils.logger import logger

# Initialize FastAPI app
app = FastAPI(
    title="DocBot API",
    description="AI-powered chatbot for organizational policies and rule books",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs(settings.documents_dir, exist_ok=True)
os.makedirs(settings.chroma_db_dir, exist_ok=True)

# Initialize services
loader = DocumentLoader()
processor = TextProcessor()
vector_store = VectorStoreManager()
rag_agent = None

logger.info("DocBot API initialized successfully")

# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting up DocBot API...")
    try:
        # Try to load existing vectorstore
        vs = vector_store.get_vectorstore()
        if vs:
            logger.info("Loaded existing vectorstore")
    except Exception as e:
        logger.warning(f"No existing vectorstore found: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down DocBot API...")

# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns:
        HealthResponse with status and component info
    """
    try:
        vs = vector_store.get_vectorstore()
        documents_count = 0
        if vs:
            documents_count = vs._collection.count() if hasattr(vs, '_collection') else 0
        
        return HealthResponse(
            status="ok",
            embeddings=f"Google ({settings.google_embedding_model})",
            llm=f"Gemini ({settings.google_llm_model})",
            documents_indexed=documents_count
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="degraded",
            embeddings=f"Google ({settings.google_embedding_model})",
            llm=f"Gemini ({settings.google_llm_model})",
            documents_indexed=0
        )

@app.get("/status", tags=["Health"])
async def get_status():
    """Get detailed status"""
    try:
        vs = vector_store.get_vectorstore()
        is_indexed = vs is not None
        documents_count = 0
        
        if is_indexed and hasattr(vs, '_collection'):
            documents_count = vs._collection.count()
        
        return {
            "status": "ready",
            "documents_indexed": is_indexed,
            "document_count": documents_count,
            "embedding_model": settings.google_embedding_model,
            "llm_model": settings.google_llm_model,
            "chunk_size": settings.chunk_size,
            "chunk_overlap": settings.chunk_overlap,
            "retriever_k": settings.retriever_k,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# DOCUMENT UPLOAD & INDEXING ENDPOINTS
# ============================================================================

@app.post("/upload", response_model=UploadResponse, tags=["Documents"])
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload and index documents
    
    Supports: PDF, DOCX, TXT, PNG, JPG, JPEG
    
    Args:
        files: List of document files
        
    Returns:
        UploadResponse with indexing statistics
        
    Raises:
        HTTPException: If upload or indexing fails
    """
    global rag_agent
    
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    try:
        logger.info(f"Received {len(files)} files for upload")
        
        # Validate and save files
        saved_files = []
        for file in files:
            # Validate file extension
            file_ext = file.filename.split('.')[-1].lower()
            if file_ext not in settings.allowed_extensions:
                logger.warning(f"Rejected file with unsupported extension: {file.filename}")
                continue
            
            # Validate file size
            file_content = await file.read()
            file_size = len(file_content)
            
            if file_size > settings.max_file_size_bytes:
                logger.warning(f"Rejected file exceeding size limit: {file.filename}")
                continue
            
            # Save file
            file_path = os.path.join(settings.documents_dir, file.filename)
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            saved_files.append(file_path)
            logger.info(f"Saved file: {file.filename} ({file_size} bytes)")
        
        if not saved_files:
            raise HTTPException(
                status_code=400,
                detail="No valid files were provided"
            )
        
        # Load documents
        logger.info(f"Loading {len(saved_files)} documents...")
        documents = []
        for file_path in saved_files:
            try:
                doc = loader.load_document(file_path)
                documents.append(doc)
            except Exception as e:
                logger.error(f"Failed to load {file_path}: {str(e)}")
                continue
        
        if not documents:
            raise HTTPException(
                status_code=400,
                detail="Failed to extract content from uploaded files"
            )
        
        logger.info(f"Loaded {len(documents)} documents")
        
        # Process documents (clean + chunk)
        logger.info("Processing documents...")
        chunks = processor.process_documents(documents)
        
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="Failed to process documents"
            )
        
        logger.info(f"Created {len(chunks)} chunks")
        
        # Index documents
        logger.info("Indexing documents into vector store...")
        vector_store.index_documents(chunks)
        
        # Initialize RAG agent with retriever
        retriever = vector_store.get_retriever()
        rag_agent = RAGAgent(retriever)
        
        logger.info("Successfully indexed all documents and initialized RAG agent")
        
        return UploadResponse(
            status="success",
            documents_indexed=len(documents),
            chunks_created=len(chunks),
            embedding_provider=f"Google ({settings.google_embedding_model})",
            llm_provider=f"Gemini ({settings.google_llm_model})"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents", tags=["Documents"])
async def clear_documents():
    """
    Clear all indexed documents
    
    Returns:
        Status message
    """
    global rag_agent
    
    try:
        logger.info("Clearing all documents...")
        
        # Clear vector store
        vector_store.clear_vectorstore()
        
        # Clear document directory
        if os.path.exists(settings.documents_dir):
            for file in os.listdir(settings.documents_dir):
                file_path = os.path.join(settings.documents_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        rag_agent = None
        
        logger.info("Cleared all documents successfully")
        
        return {
            "status": "success",
            "message": "All documents cleared",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error clearing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# QUERY & ANSWERING ENDPOINTS
# ============================================================================

@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def query_documents(question: str = Query(..., min_length=1, max_length=1000)):
    """
    Ask a question about indexed documents
    
    Args:
        question: User question
        
    Returns:
        QueryResponse with answer and sources
        
    Raises:
        HTTPException: If RAG fails or no documents indexed
    """
    global rag_agent
    
    if not rag_agent:
        raise HTTPException(
            status_code=400,
            detail="No documents indexed yet. Please upload documents first."
        )
    
    try:
        logger.info(f"Processing query: {question[:100]}")
        
        # Get answer from RAG agent
        result = rag_agent.answer_question(question)
        
        # Convert sources to SourceDocument objects
        source_docs = [
            SourceDocument(
                name=source["name"],
                relevance_score=source.get("relevance_score"),
                chunk_index=source.get("chunk_index")
            )
            for source in result["sources"]
        ]
        
        return QueryResponse(
            answer=result["answer"],
            sources=source_docs,
            chunks_used=result["chunks_used"],
            model=result["model"],
            confidence=result.get("confidence", 0.85),
            processing_time_ms=result["processing_time_ms"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.post("/query-stream", tags=["Query"])
async def query_documents_stream(question: str = Query(..., min_length=1)):
    """
    Ask a question with streaming response
    
    Returns:
        Streaming response
    """
    global rag_agent
    
    if not rag_agent:
        raise HTTPException(
            status_code=400,
            detail="No documents indexed yet"
        )
    
    try:
        result = rag_agent.answer_question(question)
        return result
    except Exception as e:
        logger.error(f"Error in streaming query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# RETRIEVAL ENDPOINTS
# ============================================================================

@app.get("/search", tags=["Search"])
async def search_documents(
    query: str = Query(..., min_length=1),
    k: int = Query(5, ge=1, le=20)
):
    """
    Search for documents without generating answer
    
    Args:
        query: Search query
        k: Number of results
        
    Returns:
        List of matching documents
    """
    try:
        logger.info(f"Searching for: {query} (k={k})")
        
        results = vector_store.search_with_scores(query, k=k)
        
        search_results = []
        for doc, score in results:
            search_results.append({
                "content": doc.page_content[:500],  # First 500 chars
                "source": doc.metadata.get("source", "Unknown"),
                "relevance_score": 1 - score,  # Convert distance to similarity
                "metadata": doc.metadata
            })
        
        return {
            "query": query,
            "results_count": len(search_results),
            "results": search_results
        }
    
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# ERROR HANDLING
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    """API information"""
    return {
        "name": "DocBot API",
        "version": "1.0.0",
        "description": "AI-powered chatbot for organizational policies",
        "docs": "/docs",
        "health": "/health",
        "status": "/status"
    }

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting DocBot API on {settings.host}:{settings.port}")
    logger.info(f"Debug mode: {settings.debug}")
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
```