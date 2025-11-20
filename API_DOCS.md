# DocBot API Documentation

## Base URL

```
http://localhost:8000
```

## Endpoints

### `GET /health`
Returns component status.

### `GET /status`
Detailed configuration and document counts.

### `POST /upload`
Multipart form upload of documents.

- Field name: `files`
- Supports: pdf, docx, txt, png, jpg, jpeg

Response:
```json
{
  "status": "success",
  "documents_indexed": 2,
  "chunks_created": 78,
  "embedding_provider": "Google (models/embedding-001)",
  "llm_provider": "Gemini (gemini-2.0-flash-lite)",
  "timestamp": "2025-01-01T12:00:00.000Z"
}
```

### `POST /query?question=...`
Answer a question using RAG.

Response:
```json
{
  "answer": "You are entitled to 30 days of annual leave...",
  "sources": [
    { "name": "leave_policy.pdf", "relevance_score": 0.86 }
  ],
  "chunks_used": 5,
  "model": "gemini-2.0-flash-lite",
  "confidence": 0.85,
  "processing_time_ms": 1043.2
}
```

### `GET /search?query=...&k=5`
Retrieve relevant chunks without generating an answer.

### `DELETE /documents`
Clear stored documents and embeddings.

## Error Responses

Errors follow:

```json
{
  "status": "error",
  "message": "Human-readable detail",
  "timestamp": "ISO8601"
}
```

