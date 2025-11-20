# DocBot Storage Guide

## What Gets Stored and Where

DocBot stores data in **4 main locations**:

---

## 1. 📄 **Uploaded Documents** 
**Location:** `backend/documents/`

### What's Stored:
- Original files you upload (PDF, DOCX, TXT, images)
- Files are saved with their original names

### How to Check:
```powershell
# Navigate to backend folder
cd backend

# List all uploaded documents
dir documents

# Or use PowerShell
Get-ChildItem documents
```

### What You'll See:
```
documents/
  ├── employee_handbook.pdf
  ├── leave_policy.docx
  ├── policy.txt
  └── screenshot.png
```

### Configuration:
- **Path:** `DOCUMENTS_DIR=./documents` (in `.env`)
- **Max Size:** `MAX_FILE_SIZE_MB=50` (50MB per file)

---

## 2. 🗄️ **Vector Embeddings (ChromaDB)**
**Location:** `backend/chroma_db/`

### What's Stored:
- **Text embeddings** (numerical vectors representing document text)
- **Document chunks** (text split into searchable pieces)
- **Metadata** (source file names, file types, etc.)
- **Index files** (for fast searching)

### How to Check:
```powershell
# List ChromaDB files
dir chroma_db

# Check database file
dir chroma_db\chroma.sqlite3
```

### What You'll See:
```
chroma_db/
  ├── chroma.sqlite3          # Main database file
  └── [uuid]/                 # Collection folder
      ├── data_level0.bin     # Vector data
      ├── header.bin
      ├── length.bin
      └── link_lists.bin
```

### Check via API:
```powershell
# Get status (shows document count)
curl http://localhost:8000/status

# Or visit in browser:
# http://localhost:8000/status
```

### Configuration:
- **Path:** `CHROMA_DB_DIR=./chroma_db` (in `.env`)

---

## 3. 🔑 **API Key (Configuration)**
**Location:** `backend/.env`

### What's Stored:
- Google API key for Gemini LLM
- Other configuration settings

### How to Check:
```powershell
# View .env file (be careful - contains sensitive data)
type .env

# Or check if it exists
Test-Path .env
```

### What You'll See:
```
GOOGLE_API_KEY=AIzaSy...
GOOGLE_LLM_MODEL=models/gemini-2.5-flash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
...
```

**⚠️ Security:** Never commit `.env` to git!

---

## 4. 📝 **Logs**
**Location:** `backend/logs/docbot.log`

### What's Stored:
- Application logs
- Error messages
- Processing information

### How to Check:
```powershell
# View recent logs
Get-Content logs\docbot.log -Tail 50

# Or open in notepad
notepad logs\docbot.log
```

### Configuration:
- **Path:** `LOG_FILE=./logs/docbot.log` (in `.env`)
- **Level:** `LOG_LEVEL=INFO` (in `.env`)

---

## Quick Verification Commands

### Check if documents are stored:
```powershell
cd backend
dir documents
```

### Check if embeddings are indexed:
```powershell
# Via API
curl http://localhost:8000/status

# Or check ChromaDB folder
dir chroma_db
```

### Check document count:
```powershell
# Count files in documents folder
(Get-ChildItem documents).Count

# Or use API
curl http://localhost:8000/health
```

---

## What's NOT Stored

- ❌ **API keys in database** - Only in `.env` file
- ❌ **User sessions** - No user authentication
- ❌ **Chat history** - Not persisted (only in memory)
- ❌ **Original file content in ChromaDB** - Only embeddings and metadata

---

## Storage Sizes

| Item | Typical Size | Location |
|------|-------------|----------|
| Uploaded PDF | 1-5 MB | `documents/` |
| Uploaded DOCX | 100-500 KB | `documents/` |
| ChromaDB (per 1000 chunks) | ~10-50 MB | `chroma_db/` |
| Log file | 1-10 MB | `logs/` |
| .env file | <1 KB | `backend/` |

---

## Clearing Storage

### Delete all documents:
```powershell
# Via API
curl -X DELETE http://localhost:8000/documents

# Or manually
Remove-Item documents\* -Recurse
Remove-Item chroma_db\* -Recurse
```

### Clear logs:
```powershell
Clear-Content logs\docbot.log
```

---

## Backup Recommendations

**Important files to backup:**
1. `chroma_db/` - Your indexed documents (embeddings)
2. `documents/` - Original uploaded files
3. `.env` - Configuration (keep secure!)

**Not critical:**
- `logs/` - Can be regenerated
- `__pycache__/` - Python cache (can be deleted)

