# Environment Variables Setup Guide

## Quick Setup

1. **Copy the example file:**
   ```powershell
   cd backend
   copy env.example .env
   ```

2. **Edit `.env` file** and replace `your-google-api-key-here` with your actual Google API key.

## Required Configuration

### `GOOGLE_API_KEY` (REQUIRED)
- **What it is:** Your Google Generative AI API key
- **How to get it:**
  1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
  2. Sign in with your Google account
  3. Click "Create API Key"
  4. Copy the key and paste it in `.env`
- **Example:** `GOOGLE_API_KEY=AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567`

**⚠️ IMPORTANT:** This key is used for both:
- **Embeddings** (converting text to vectors for search)
- **Gemini LLM** (generating answers to questions)

## Optional Settings (with defaults)

### Google AI Models
- `GOOGLE_EMBEDDING_MODEL=models/embedding-001` - Model for text embeddings
- `GOOGLE_LLM_MODEL=gemini-2.0-flash-lite` - Model for generating answers

### Server Configuration
- `HOST=0.0.0.0` - Server host (0.0.0.0 allows external connections)
- `PORT=8000` - Server port
- `DEBUG=False` - Enable debug mode (set to `True` for development)

### Storage Configuration
- `DOCUMENTS_DIR=./documents` - Where uploaded files are stored
- `CHROMA_DB_DIR=./chroma_db` - Where vector database is stored
- `MAX_FILE_SIZE_MB=50` - Maximum file size in megabytes
- `ALLOWED_FILE_TYPES=pdf,docx,txt,png,jpg,jpeg` - Supported file formats

### RAG (Retrieval-Augmented Generation) Configuration
- `CHUNK_SIZE=1000` - Size of text chunks (characters) for processing
- `CHUNK_OVERLAP=200` - Overlap between chunks (helps maintain context)
- `RETRIEVER_K=5` - Number of document chunks to retrieve per query
- `TEMPERATURE=0.3` - LLM creativity (0.0 = deterministic, 1.0 = creative)

### Logging
- `LOG_LEVEL=INFO` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE=./logs/docbot.log` - Log file path

## Example `.env` File

```env
# Google API Configuration (REQUIRED - replace with your actual key)
GOOGLE_API_KEY=AIzaSyAbCdEfGhIjKlMnOpQrStUvWxYz1234567
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

## Security Notes

- **Never commit `.env` to version control** (it should be in `.gitignore`)
- **Keep your API key secret** - don't share it publicly
- The `.env` file is automatically loaded by the application when it starts

