"""
DocBot - FastAPI backend for document ingestion and question answering.
"""
from datetime import datetime
import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List

# Disable ChromaDB telemetry to suppress warnings
os.environ["ANONYMIZED_TELEMETRY"] = "False"

from models.response import (
    UploadResponse,
    QueryResponse,
    HealthResponse,
    SourceDocument,
)
from services.document_loader import DocumentLoader
from services.text_processor import TextProcessor
from services.vector_store import VectorStoreManager
from services.rag_agent import RAGAgent
from utils.config import settings
from utils.logger import logger

app = FastAPI(
    title="DocBot API",
    description="AI-powered chatbot for organizational policies and rule books",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.documents_dir, exist_ok=True)
os.makedirs(settings.chroma_db_dir, exist_ok=True)

loader = DocumentLoader()
processor = TextProcessor()
vector_store = VectorStoreManager()
rag_agent = None


@app.on_event("startup")
async def startup_event():
    logger.info("Starting DocBot API")
    try:
        vector_store.get_vectorstore()
    except Exception as exc:
        logger.warning("Unable to load existing vectorstore: %s", exc)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    try:
        vs = vector_store.get_vectorstore()
        documents_count = 0
        if vs and hasattr(vs, "_collection"):
            documents_count = vs._collection.count()
        return HealthResponse(
            status="ok",
            embeddings=f"HuggingFace ({settings.embedding_model})",
            llm=f"Gemini ({settings.google_llm_model})",
            documents_indexed=documents_count,
        )
    except Exception as exc:
        logger.error("Health check failed: %s", exc)
        return HealthResponse(
            status="degraded",
            embeddings=f"HuggingFace ({settings.embedding_model})",
            llm=f"Gemini ({settings.google_llm_model})",
            documents_indexed=0,
        )


@app.get("/status", tags=["Health"])
async def get_status():
    try:
        vs = vector_store.get_vectorstore()
        is_indexed = vs is not None
        document_count = vs._collection.count() if is_indexed and hasattr(vs, "_collection") else 0
        return {
            "status": "ready" if is_indexed else "empty",
            "documents_indexed": is_indexed,
            "document_count": document_count,
            "embedding_model": settings.embedding_model,
            "llm_model": settings.google_llm_model,
            "chunk_size": settings.chunk_size,
            "chunk_overlap": settings.chunk_overlap,
            "retriever_k": settings.retriever_k,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as exc:
        logger.error("Status check failed: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/upload", response_model=UploadResponse, tags=["Documents"])
async def upload_documents(files: List[UploadFile] = File(...)):
    global rag_agent
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    saved_files: List[str] = []
    for file in files:
        file_ext = (file.filename or "").split(".")[-1].lower()
        if file_ext not in settings.allowed_extensions:
            logger.warning("Unsupported file extension: %s", file.filename)
            continue

        file_content = await file.read()
        file_size = len(file_content)
        if file_size > settings.max_file_size_bytes:
            logger.warning("File exceeds size limit: %s", file.filename)
            continue

        file_path = os.path.join(settings.documents_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(file_content)
        saved_files.append(file_path)
        logger.info("Saved file %s (%s bytes)", file.filename, file_size)

    if not saved_files:
        raise HTTPException(status_code=400, detail="No valid files were provided")

    documents = []
    for path in saved_files:
        try:
            documents.append(loader.load_document(path))
        except Exception as exc:
            logger.error("Failed to load %s: %s", path, exc)
    if not documents:
        raise HTTPException(status_code=400, detail="Failed to extract content from uploaded files")

    chunks = processor.process_documents(documents)
    if not chunks:
        raise HTTPException(status_code=400, detail="Failed to process documents")

    vector_store.index_documents(chunks)
    retriever = vector_store.get_retriever()
    rag_agent = RAGAgent(retriever)

    return UploadResponse(
        status="success",
        documents_indexed=len(documents),
        chunks_created=len(chunks),
        embedding_provider=f"HuggingFace ({settings.embedding_model})",
        llm_provider=f"Gemini ({settings.google_llm_model})",
    )


@app.delete("/documents", tags=["Documents"])
async def clear_documents():
    global rag_agent
    vector_store.clear_vectorstore()
    if os.path.exists(settings.documents_dir):
        for file in os.listdir(settings.documents_dir):
            file_path = os.path.join(settings.documents_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    rag_agent = None
    return {
        "status": "success",
        "message": "All documents cleared",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def query_documents(question: str = Query(..., min_length=1, max_length=1000)):
    global rag_agent
    if not rag_agent:
        raise HTTPException(status_code=400, detail="No documents indexed yet. Please upload documents first.")

    result = rag_agent.answer_question(question)
    source_docs = [
        SourceDocument(
            name=source["name"],
            relevance_score=source.get("relevance_score"),
            chunk_index=source.get("chunk_index"),
        )
        for source in result.get("sources", [])
    ]
    return QueryResponse(
        answer=result["answer"],
        sources=source_docs,
        chunks_used=result["chunks_used"],
        model=result["model"],
        confidence=result.get("confidence", 0.85),
        processing_time_ms=result["processing_time_ms"],
    )


@app.get("/search", tags=["Search"])
async def search_documents(query: str = Query(..., min_length=1), k: int = Query(5, ge=1, le=20)):
    results = vector_store.search_with_scores(query, k=k)
    payload = []
    for doc, score in results:
        payload.append(
            {
                "content": doc.page_content[:500],
                "source": doc.metadata.get("source", "Unknown"),
                "relevance_score": 1 - score,
                "metadata": doc.metadata,
            }
        )
    return {"query": query, "results_count": len(payload), "results": payload}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error("HTTP Exception: %s - %s", exc.status_code, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error("Unexpected error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat(),
        },
    )


@app.get("/", tags=["Info"])
async def root():
    return {
        "name": "DocBot API",
        "version": "1.0.0",
        "description": "AI-powered chatbot for organizational policies",
        "docs": "/docs",
        "health": "/health",
        "status": "/status",
    }


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting DocBot API on %s:%s", settings.host, settings.port)
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )

