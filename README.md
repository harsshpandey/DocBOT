<div align="center">

# 📚 DocBot

AI-powered knowledge assistant that ingests organizational documents and answers policy/process questions using a Retrieval-Augmented Generation (RAG) pipeline.

<br />

<a href="#quickstart"><img alt="Made with FastAPI" src="https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white"></a>
<a href="#frontend-nextjs"><img alt="Next.js" src="https://img.shields.io/badge/Frontend-Next.js-000000?logo=nextdotjs&logoColor=white"></a>
<a href="#environment-variables"><img alt="ChromaDB" src="https://img.shields.io/badge/Vector%20DB-Chroma-3E7AD6"></a>
<a href="#environment-variables"><img alt="Embeddings" src="https://img.shields.io/badge/Embeddings-SentenceTransformers-FF6F00"></a>
<a href="#api"><img alt="API" src="https://img.shields.io/badge/API-OpenAPI%20%2F%20Swagger-85EA2D?logo=swagger&logoColor=white"></a>

<br />

</div>

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture (High Level)](#architecture-high-level)
- [Screenshots](#screenshots)
- [Quickstart](#quickstart)
- [Environment Variables](#environment-variables)
- [Run With Docker](#run-with-docker)
- [API](#api)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Demo / Presentation](#demo--presentation)
- [Contributing](#contributing)

## Features

- **Document ingestion**: PDF, DOCX, TXT, PNG/JPG via UI or API.
- **Local embeddings**: HuggingFace sentence-transformers (no API key required for embeddings).
- **Vector store**: ChromaDB for fast, persistent similarity search.
- **LLM answers**: Google Gemini for generation with cited sources.
- **Web UI**: Next.js chat with uploads, streaming, and source citations.
- **Health & search**: `/health`, `/status`, `/search` endpoints.

## Tech Stack

- **Backend**: FastAPI, LangChain, ChromaDB, Sentence-Transformers, Gemini
- **Frontend**: Next.js 14, React 18, TailwindCSS, Zustand
- **Infra/Dev**: Docker, Docker Compose, Uvicorn

## Architecture (High Level)

1. User uploads documents via UI or `POST /upload`.
2. Backend extracts text, chunks content, computes embeddings, and indexes in ChromaDB.
3. User asks a question via UI or `POST /query`.
4. Retriever returns top-k chunks; Gemini generates an answer with citations.

## Screenshots

> Add your UI screenshots or GIFs here for a visual overview.

```text
docs/
└─ screenshots/
   ├─ chat.png
   └─ upload.png
```

## Quickstart

See `INSTALLATION.md` for detailed platform-specific dependencies (e.g., Poppler/Tesseract for PDF/OCR). Below is a concise setup.

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+
- Optional (for OCR/PDF images): Tesseract OCR and Poppler (see `INSTALLATION.md`)

### Backend (FastAPI)

- Windows (PowerShell):
  ```powershell
  cd backend
  py -3 -m venv .venv
  .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  copy env.example .env  # then edit .env to set GOOGLE_API_KEY, etc.
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

- macOS/Linux (bash):
  ```bash
  cd backend
  python3 -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  cp env.example .env  # then edit .env to set GOOGLE_API_KEY, etc.
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Frontend defaults to http://localhost:3000 and expects the backend at http://localhost:8000.

## Environment Variables

Configure `backend/.env` based on `backend/env.example`:

- `GOOGLE_API_KEY` – Required for Gemini LLM.
- `GOOGLE_LLM_MODEL` – e.g., `models/gemini-2.5-flash`.
- `EMBEDDING_MODEL` – e.g., `sentence-transformers/all-MiniLM-L6-v2`.
- Storage and server settings: `DOCUMENTS_DIR`, `CHROMA_DB_DIR`, `HOST`, `PORT`, etc.

## Run With Docker

From the repository root:

```bash
docker compose -f docker/docker-compose.yml up --build
```

- Backend: http://localhost:8000 (FastAPI docs at `/docs`)
- Frontend: http://localhost:3000

## API

<details>
<summary><b>Endpoints overview</b></summary>

- Swagger UI: `GET /docs`
- Health: `GET /health`, `GET /status`
- Upload: `POST /upload` (multipart files[])
- Query: `POST /query?question=...`
- Search: `GET /search?query=...&k=5`

</details>

For request/response shapes and examples, see `API_DOCS.md`.

## Project Structure

```
DocBot/
├─ backend/            # FastAPI app, services, models, utils
├─ frontend/           # Next.js 14 app (chat UI)
├─ docker/             # Dockerfiles & docker-compose
├─ INSTALLATION.md     # Detailed environment setup
├─ API_DOCS.md         # API usage and examples
├─ PRD.md              # Product Requirements Document
└─ README.md
```

## Usage

- Upload PDFs/DOCX/TXT/PNG/JPG via the UI or `POST /upload`.
- Ask questions in the UI or call `POST /query`.
- Inspect system state via `/health` and `/status`.

## Demo / Presentation

PPT: https://www.canva.com/design/DAG5SVp2RDk/KbFAXPyBxr_SQhv1mLUexQ/edit?utm_content=DAG5SVp2RDk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## Contributing

1. Fork and create a feature branch.
2. Run linters/tests:
   - Backend: `black . && flake8 && pytest`
   - Frontend: `npm run lint`
3. Open a PR with a clear description.
