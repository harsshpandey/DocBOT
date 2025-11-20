# Installation Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- Google Generative AI API key (Embeddings + Gemini)
- Tesseract OCR (for image ingestion)

## Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp env.example .env
```

Update `.env` with your Google API credentials and optional tuning parameters.

Run local server:

```bash
uvicorn main:app --reload
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Set the backend API base URL in `frontend/lib/api.ts` if running on a custom host or port.

## Docker

```bash
docker compose up --build
```

This starts both backend (`http://localhost:8000`) and frontend (`http://localhost:3000`).

## Testing

Backend tests:

```bash
cd backend
pytest
```

Frontend lint/tests (when added):

```bash
cd frontend
npm run lint
```

