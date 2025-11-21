# DocBot

DocBot is an AI-powered knowledge assistant that ingests organizational documents and answers policy or process questions through a Retrieval-Augmented Generation (RAG) pipeline.

## Project Layout

- `backend/` – FastAPI service for ingestion, vector indexing (Chroma + Google embeddings), and Gemini-powered answers.
- `frontend/` – Next.js 14 chat interface with file uploads, streaming responses, and source citations.
- `docker/` – Dockerfiles and `docker-compose` for local orchestration.

## Getting Started

1. **Backend**
   ```bash
   cd backend
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   cp env.example .env  # fill in Google API key
   uvicorn main:app --reload
   ```

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Usage**
   - Upload PDFs, DOCX, TXT, or images through the chat UI or via `POST /upload`.
   - Ask questions via the chat UI or `POST /query?question=...`.
   - Health endpoints: `/health`, `/status`.

Refer to `INSTALLATION.md` and `API_DOCS.md` for detailed guidance.

📊 Project Presentation

You can view the complete project PPT here:
https://www.canva.com/design/DAG5SVp2RDk/KbFAXPyBxr_SQhv1mLUexQ/edit?utm_content=DAG5SVp2RDk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton