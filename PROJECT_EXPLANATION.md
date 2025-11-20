# DocBot - Complete Project Explanation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Backend Components](#backend-components)
6. [Frontend Components](#frontend-components)
7. [Data Flow](#data-flow)
8. [API Endpoints](#api-endpoints)
9. [Configuration](#configuration)
10. [How It Works](#how-it-works)

---

## 🎯 Project Overview

### What is DocBot?

**DocBot** is an AI-powered document Q&A system that uses **RAG (Retrieval-Augmented Generation)** to answer questions from your documents.

### Key Features

- 📄 **Multi-format Support**: PDF, DOCX, TXT, Images (PNG/JPG)
- 🔍 **Semantic Search**: Understands meaning, not just keywords
- 💬 **Chat Interface**: Natural language questions
- 📚 **Source Citations**: Shows which documents were used
- 🏠 **Local Embeddings**: Runs on your machine (privacy-focused)
- ⚡ **Fast Queries**: Pre-indexed documents for instant search

### Problem It Solves

**Before DocBot:**
- Manual search through hundreds of documents
- Time-consuming policy lookups
- Scattered information across files
- No contextual understanding

**With DocBot:**
- Instant answers from all documents
- Semantic understanding of questions
- Centralized knowledge base
- Source citations for verification

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│              Next.js 14 Web Application                     │
│  - Chat Interface                                            │
│  - File Upload                                               │
│  - Message Display                                           │
└────────────────────┬─────────────────────────────────────────┘
                     │ HTTP REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    API LAYER (FastAPI)                      │
│  - Document Upload Endpoint                                 │
│  - Query Endpoint                                            │
│  - Health/Status Endpoints                                  │
└────────────────────┬─────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌─────────────┐ ┌──────────┐ ┌──────────┐
│  Document   │ │  Text    │ │  Vector  │
│   Loader    │ │Processor │ │  Store   │
└──────┬──────┘ └────┬─────┘ └────┬─────┘
       │              │            │
       └──────────────┼────────────┘
                      ▼
            ┌─────────────────┐
            │   RAG Agent     │
            │  (Answer Gen)   │
            └────────┬────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│HuggingFace│  │ ChromaDB │  │  Gemini  │
│Embeddings│  │  Vector  │  │    LLM   │
│  (Local) │  │   Store  │  │   (API)  │
└──────────┘  └──────────┘  └──────────┘
```

### Three-Layer Design

1. **Frontend Layer** (Next.js)
   - User interface
   - Chat components
   - File upload UI

2. **API Layer** (FastAPI)
   - REST endpoints
   - Request handling
   - Response formatting

3. **Processing Layer** (Python Services)
   - Document processing
   - Embedding generation
   - RAG pipeline

---

## 🛠️ Technology Stack

### Backend

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Main language | 3.10+ |
| **FastAPI** | Web framework | 0.104.1 |
| **Uvicorn** | ASGI server | 0.24.0 |
| **LangChain** | LLM framework | 0.1.9 |
| **ChromaDB** | Vector database | 0.4.21 |
| **HuggingFace** | Local embeddings | sentence-transformers 2.2.2 |
| **Google Gemini** | LLM for answers | via langchain-google-genai |
| **PyPDF2** | PDF parsing | 3.0.1 |
| **python-docx** | Word doc parsing | 0.8.11 |
| **pytesseract** | Image OCR | 0.3.10 |
| **Pydantic** | Data validation | 2.5.0 |

### Frontend

| Technology | Purpose |
|------------|---------|
| **Next.js 14** | React framework |
| **TypeScript** | Type safety |
| **Tailwind CSS** | Styling |
| **React Hooks** | State management |

### Storage

- **File System**: Original documents (`backend/documents/`)
- **ChromaDB**: Vector embeddings (`backend/chroma_db/`)
- **SQLite**: ChromaDB metadata storage

---

## 📁 Project Structure

```
DocBot/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # FastAPI app & endpoints
│   ├── models/                # Pydantic data models
│   │   ├── document.py        # Document model
│   │   └── response.py        # API response models
│   ├── services/              # Core business logic
│   │   ├── document_loader.py # PDF/DOCX/TXT/Image loading
│   │   ├── text_processor.py  # Text cleaning & chunking
│   │   ├── vector_store.py    # ChromaDB & embeddings
│   │   └── rag_agent.py       # RAG pipeline & answer generation
│   ├── utils/                 # Utilities
│   │   ├── config.py          # Settings & env vars
│   │   └── logger.py          # Logging setup
│   ├── documents/             # Uploaded files storage
│   ├── chroma_db/             # Vector database
│   ├── logs/                  # Application logs
│   ├── .env                   # Environment variables
│   └── requirements.txt       # Python dependencies
│
├── frontend/                  # Next.js frontend
│   ├── app/                   # Next.js app directory
│   │   ├── page.tsx           # Main page
│   │   ├── layout.tsx         # App layout
│   │   └── api/               # API routes
│   ├── components/            # React components
│   │   ├── ChatInterface.tsx  # Main chat UI
│   │   ├── FileUploadArea.tsx # File upload component
│   │   ├── MessageList.tsx    # Message display
│   │   ├── MessageInput.tsx   # Input field
│   │   └── SourceDocuments.tsx # Source citations
│   ├── lib/                   # Utilities
│   │   ├── api.ts             # API client
│   │   ├── types.ts           # TypeScript types
│   │   └── utils.ts           # Helper functions
│   └── store/                 # State management
│       └── chatStore.ts       # Chat state
│
└── docker/                    # Docker configuration
    ├── docker-compose.yml     # Multi-container setup
    ├── Dockerfile.backend     # Backend image
    └── Dockerfile.frontend    # Frontend image
```

---

## 🔧 Backend Components

### 1. **main.py** - FastAPI Application

**Purpose**: Main entry point, defines all API endpoints

**Key Endpoints**:
- `POST /upload` - Upload and index documents
- `POST /query` - Ask questions
- `GET /health` - Health check
- `GET /status` - System status
- `GET /search` - Direct vector search
- `DELETE /documents` - Clear all documents

**Key Features**:
- CORS middleware for frontend access
- Global service instances (loader, processor, vector_store)
- Error handling and logging

### 2. **document_loader.py** - Document Loading Service

**Purpose**: Extract text from various file formats

**Supported Formats**:
- **PDF**: Uses PyPDF2 to extract text from pages
- **DOCX**: Uses python-docx to read paragraphs
- **TXT**: Direct file reading
- **Images**: Uses Tesseract OCR (PNG, JPG, JPEG)

**Key Methods**:
- `load_pdf()` - Extract text from PDF
- `load_docx()` - Extract text from Word docs
- `load_text()` - Read plain text files
- `extract_text_from_image()` - OCR for images
- `load_document()` - Main method that routes to format-specific loaders

**Output**: LangChain `Document` objects with text content and metadata

### 3. **text_processor.py** - Text Processing Service

**Purpose**: Clean and chunk documents for embedding

**Process**:
1. **Text Cleaning**:
   - Remove extra whitespace
   - Normalize special characters
   - Clean formatting

2. **Chunking**:
   - Split documents into chunks (default: 1000 characters)
   - Overlap between chunks (default: 200 characters)
   - Uses `RecursiveCharacterTextSplitter`

**Why Chunking?**:
- Embeddings work better on smaller text pieces
- Allows retrieval of specific sections
- Maintains context with overlap

**Key Methods**:
- `clean_text()` - Normalize text
- `split_documents()` - Chunk documents
- `process_documents()` - Full pipeline

### 4. **vector_store.py** - Vector Database Manager

**Purpose**: Manage embeddings and vector search

**Technology Stack**:
- **Embeddings**: HuggingFace `all-MiniLM-L6-v2` (local, ~80MB)
- **Database**: ChromaDB (local SQLite-based)

**Key Features**:
- **Local Embeddings**: No API calls, runs on your machine
- **Persistent Storage**: Embeddings saved to disk
- **Semantic Search**: Finds similar content by meaning

**Key Methods**:
- `index_documents()` - Generate embeddings and store
- `get_vectorstore()` - Load existing database
- `search()` - Find similar documents
- `search_with_scores()` - Search with similarity scores
- `get_retriever()` - Get LangChain retriever
- `clear_vectorstore()` - Delete all embeddings

**Storage Location**: `backend/chroma_db/`

### 5. **rag_agent.py** - RAG Pipeline

**Purpose**: Generate answers using RAG (Retrieval-Augmented Generation)

**RAG Process**:
1. **Retrieval**: Find relevant document chunks
2. **Augmentation**: Combine question with context
3. **Generation**: Use LLM to generate answer

**Technology**:
- **LLM**: Google Gemini 2.5 Flash
- **Retriever**: ChromaDB vector search

**Key Methods**:
- `retrieve_context()` - Find relevant documents
- `format_context()` - Prepare context for LLM
- `answer_question()` - Complete RAG pipeline

**Prompt Template**:
```
You are a helpful assistant that answers questions about 
organizational policies based only on the provided context.

CONTEXT:
{retrieved_document_chunks}

Question: {user_question}
```

### 6. **config.py** - Configuration Management

**Purpose**: Load and manage application settings

**Sources**:
- `.env` file (environment variables)
- Default values

**Key Settings**:
- Google API key (for Gemini LLM)
- Embedding model name
- LLM model name
- Chunk size and overlap
- File size limits
- Storage paths

### 7. **logger.py** - Logging Setup

**Purpose**: Configure application logging

**Features**:
- File logging (`logs/docbot.log`)
- Console logging
- Configurable log levels

---

## 🎨 Frontend Components

### 1. **ChatInterface.tsx** - Main Chat UI

**Purpose**: Main chat interface component

**Features**:
- Message display
- File upload area
- Input field
- Source document display

### 2. **FileUploadArea.tsx** - File Upload

**Purpose**: Handle document uploads

**Features**:
- Drag & drop support
- Multiple file selection
- File type validation
- Upload progress

### 3. **MessageList.tsx** - Message Display

**Purpose**: Show chat messages

**Features**:
- User messages
- Bot responses
- Timestamps
- Source citations

### 4. **MessageInput.tsx** - Input Field

**Purpose**: Text input for questions

**Features**:
- Enter key to send
- Disabled state during processing
- Character limits

### 5. **SourceDocuments.tsx** - Source Citations

**Purpose**: Display source documents

**Features**:
- List of source files
- Relevance scores
- Document names

### 6. **api.ts** - API Client

**Purpose**: Communicate with backend

**Endpoints Used**:
- `POST /upload` - Upload documents
- `POST /query` - Ask questions
- `GET /health` - Check health
- `GET /status` - Get status

---

## 🔄 Data Flow

### Document Upload Flow

```
1. User uploads files (PDF, DOCX, TXT, Images)
   ↓
2. Frontend sends to POST /upload
   ↓
3. Backend saves files to backend/documents/
   ↓
4. DocumentLoader extracts text:
   - PDF → PyPDF2
   - DOCX → python-docx
   - TXT → Direct read
   - Images → Tesseract OCR
   ↓
5. TextProcessor:
   - Cleans text
   - Splits into chunks (1000 chars, 200 overlap)
   ↓
6. VectorStoreManager:
   - Generates embeddings (HuggingFace)
   - Stores in ChromaDB
   ↓
7. Returns success response
```

### Query Flow

```
1. User types question
   ↓
2. Frontend sends to POST /query?question=...
   ↓
3. RAGAgent.answer_question():
   a. Converts question to embedding
   b. Searches ChromaDB for similar chunks
   c. Retrieves top 5 relevant chunks
   ↓
4. Formats context:
   - Combines question + retrieved chunks
   - Creates prompt for LLM
   ↓
5. Sends to Google Gemini API:
   - Question + Context
   - Gets generated answer
   ↓
6. Returns response:
   - Answer text
   - Source documents
   - Processing time
```

---

## 🌐 API Endpoints

### POST /upload

**Purpose**: Upload and index documents

**Request**:
```http
POST /upload
Content-Type: multipart/form-data

files: [file1.pdf, file2.docx, ...]
```

**Response**:
```json
{
  "status": "success",
  "documents_indexed": 3,
  "chunks_created": 45,
  "embedding_provider": "HuggingFace (sentence-transformers/all-MiniLM-L6-v2)",
  "llm_provider": "Gemini (models/gemini-2.5-flash)"
}
```

### POST /query

**Purpose**: Ask questions about documents

**Request**:
```http
POST /query?question=What is the leave policy?
```

**Response**:
```json
{
  "answer": "According to the employee handbook...",
  "sources": [
    {
      "name": "employee_handbook.pdf",
      "relevance_score": 0.95,
      "chunk_index": 12
    }
  ],
  "chunks_used": 5,
  "model": "models/gemini-2.5-flash",
  "confidence": 0.85,
  "processing_time_ms": 1234
}
```

### GET /health

**Purpose**: Check system health

**Response**:
```json
{
  "status": "ok",
  "embeddings": "HuggingFace (sentence-transformers/all-MiniLM-L6-v2)",
  "llm": "Gemini (models/gemini-2.5-flash)",
  "documents_indexed": 10
}
```

### GET /status

**Purpose**: Get detailed system status

**Response**:
```json
{
  "status": "ready",
  "documents_indexed": true,
  "document_count": 10,
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "llm_model": "models/gemini-2.5-flash",
  "chunk_size": 1000,
  "chunk_overlap": 200,
  "retriever_k": 5,
  "timestamp": "2025-11-21T01:00:00"
}
```

### GET /search

**Purpose**: Direct vector search (without LLM)

**Request**:
```http
GET /search?query=leave policy&k=5
```

**Response**:
```json
{
  "query": "leave policy",
  "results_count": 5,
  "results": [
    {
      "content": "Employees are entitled to...",
      "source": "employee_handbook.pdf",
      "relevance_score": 0.95,
      "metadata": {...}
    }
  ]
}
```

### DELETE /documents

**Purpose**: Clear all indexed documents

**Response**:
```json
{
  "status": "success",
  "message": "All documents cleared",
  "timestamp": "2025-11-21T01:00:00"
}
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Google API (for LLM only)
GOOGLE_API_KEY=your-api-key-here
GOOGLE_LLM_MODEL=models/gemini-2.5-flash

# Embeddings (local)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Storage
DOCUMENTS_DIR=./documents
CHROMA_DB_DIR=./chroma_db
MAX_FILE_SIZE_MB=50
ALLOWED_FILE_TYPES=pdf,docx,txt,png,jpg,jpeg

# RAG Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVER_K=5
TEMPERATURE=0.3

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/docbot.log
```

---

## 🔍 How It Works (Step by Step)

### Step 1: Document Upload

1. User selects files in frontend
2. Files sent to `/upload` endpoint
3. Backend saves files to `documents/` folder
4. Each file processed:
   - Text extracted (format-specific)
   - Text cleaned and normalized
   - Split into chunks
5. Chunks converted to embeddings (HuggingFace)
6. Embeddings stored in ChromaDB
7. Success response returned

### Step 2: Question Answering

1. User types question
2. Question sent to `/query` endpoint
3. RAG pipeline:
   - Question converted to embedding
   - ChromaDB searched for similar chunks
   - Top 5 chunks retrieved
   - Context formatted with question
   - Sent to Gemini API
   - Answer generated
4. Response includes:
   - Generated answer
   - Source documents
   - Processing metrics

### Step 3: Vector Search

**How Semantic Search Works**:

1. **Embedding Generation**:
   - Text → Numerical vector (384 dimensions)
   - Similar text → Similar vectors

2. **Similarity Calculation**:
   - Cosine similarity between vectors
   - Higher score = more similar

3. **Retrieval**:
   - Query embedding compared to all stored embeddings
   - Top K most similar chunks returned

**Example**:
```
Question: "What is the leave policy?"
↓ (Embedding)
[0.12, -0.45, 0.78, ...] (384 numbers)

Document chunks:
- "Employees get 20 days leave" → [0.11, -0.44, 0.79, ...] ✓ Match!
- "Office hours are 9-5" → [0.89, 0.12, -0.33, ...] ✗ Not relevant
```

---

## 📊 Data Storage

### What Gets Stored Where

| Data Type | Location | Format |
|-----------|----------|--------|
| **Original Files** | `backend/documents/` | PDF, DOCX, TXT, Images |
| **Embeddings** | `backend/chroma_db/` | ChromaDB (SQLite + binary) |
| **Metadata** | `backend/chroma_db/chroma.sqlite3` | SQLite database |
| **Logs** | `backend/logs/docbot.log` | Text file |
| **Config** | `backend/.env` | Environment variables |

### ChromaDB Structure

```
chroma_db/
├── chroma.sqlite3          # Metadata database
└── [collection-uuid]/      # Collection folder
    ├── data_level0.bin     # Vector data
    ├── header.bin          # Index header
    ├── length.bin          # Vector lengths
    └── link_lists.bin      # Index links
```

**What's Stored**:
- Document text chunks
- Embedding vectors (384 dimensions each)
- Metadata (source file, file type, etc.)
- Index for fast search

---

## 🚀 Key Features Explained

### 1. RAG (Retrieval-Augmented Generation)

**Why RAG?**
- LLMs can hallucinate (make up answers)
- RAG provides real context from your documents
- Answers are grounded in actual content

**How It Works**:
```
Question → Find Relevant Docs → Add Context → Generate Answer
```

### 2. Local Embeddings

**Why Local?**
- No API quota limits
- Privacy (data stays on your machine)
- No internet needed (after initial download)
- Free to use

**Trade-off**: Slightly slower than API, but more control

### 3. Chunking Strategy

**Why Chunk?**
- Embeddings work better on smaller text
- Allows precise retrieval
- Overlap maintains context

**Example**:
```
Document: "Employees get 20 days leave. They can carry forward..."
↓
Chunk 1: "Employees get 20 days leave. They can carry forward 5 days..."
Chunk 2: "...carry forward 5 days to next year. Leave must be..."
         ↑ Overlap maintains context
```

### 4. Semantic Search

**Why Semantic?**
- Understands meaning, not just keywords
- "leave policy" matches "annual vacation rules"
- Better than keyword search

---

## 🔐 Security & Privacy

### What's Private

✅ **Local Embeddings**: Generated on your machine  
✅ **Document Storage**: Files stored locally  
✅ **Vector Database**: ChromaDB runs locally  
✅ **No Data Sharing**: Documents never sent to embedding API  

### What Uses API

⚠️ **Gemini LLM**: Questions + context sent to Google  
- Only when generating answers
- Context is document chunks (not full files)
- API key required

### Best Practices

- Keep `.env` file secure (don't commit to git)
- Restrict API key permissions in Google Cloud
- Use HTTPS in production
- Validate file uploads (size, type)

---

## 📈 Performance

### Typical Timings

| Operation | Time |
|-----------|------|
| Model Download (first time) | ~30-60 sec |
| Model Load | ~2-5 sec |
| Document Upload (per file) | ~1-5 sec |
| Embedding Generation (per chunk) | ~0.1-0.5 sec |
| Query Processing | ~1-3 sec |
| Answer Generation | ~0.5-2 sec |

### Optimization Tips

1. **Use GPU** (if available):
   ```python
   model_kwargs={"device": "cuda"}
   ```

2. **Smaller Model** (already using fastest):
   - Current: `all-MiniLM-L6-v2` (~80MB)

3. **Batch Processing**: Already optimized

4. **Caching**: Embeddings cached in ChromaDB

---

## 🎓 Learning Resources

### Key Concepts

- **RAG**: Retrieval-Augmented Generation
- **Embeddings**: Numerical representations of text
- **Vector Search**: Finding similar content using math
- **Chunking**: Splitting documents into smaller pieces
- **Semantic Search**: Understanding meaning, not keywords

### Technologies to Learn

- **LangChain**: LLM application framework
- **ChromaDB**: Vector database
- **FastAPI**: Modern Python web framework
- **Next.js**: React framework
- **HuggingFace**: ML model library

---

## 🐛 Troubleshooting

### Common Issues

1. **Tesseract Not Found**: Install Tesseract OCR for images
2. **API Key Invalid**: Check `.env` file
3. **Quota Exceeded**: Enable billing (for embeddings - but you use local now)
4. **Model Download Fails**: Check internet connection
5. **Slow Performance**: Use GPU or smaller model

---

## 📝 Summary

**DocBot** is a complete RAG system that:

1. **Ingests** documents in multiple formats
2. **Processes** text into searchable chunks
3. **Indexes** using local embeddings (HuggingFace)
4. **Stores** in ChromaDB vector database
5. **Retrieves** relevant content for questions
6. **Generates** answers using Gemini LLM
7. **Displays** results with source citations

**Key Innovation**: Local embeddings + Cloud LLM = Privacy + Power

The system is production-ready and can handle real-world document Q&A scenarios!

