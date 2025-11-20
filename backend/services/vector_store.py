"""
Vector store management using Chroma and local HuggingFace embeddings.
"""
from typing import List, Optional, Tuple
import os
import shutil
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from utils.logger import logger
from utils.config import settings


class VectorStoreManager:
    """Manage vector embeddings and retrieval."""

    def __init__(self, persist_directory: str | None = None):
        self.persist_directory = persist_directory or settings.chroma_db_dir
        os.makedirs(self.persist_directory, exist_ok=True)
        # Use local HuggingFace embeddings (no API key needed, runs locally)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"device": "cpu"},  # Use "cuda" if you have GPU
            encode_kwargs={"normalize_embeddings": True},  # Better for similarity search
        )
        self.vectorstore: Optional[Chroma] = None
        logger.info("Initialized VectorStoreManager with %s at %s", settings.embedding_model, self.persist_directory)

    def index_documents(self, chunks: List[Document]) -> Chroma:
        """Index documents and store embeddings."""
        logger.info("Indexing %s chunks", len(chunks))
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name="docbot_documents",
        )
        logger.info("Indexed %s chunks into Chroma", len(chunks))
        return self.vectorstore

    def get_vectorstore(self) -> Optional[Chroma]:
        """Return existing vector store or load from disk."""
        if self.vectorstore is None:
            try:
                self.vectorstore = Chroma(
                    embedding_function=self.embeddings,
                    persist_directory=self.persist_directory,
                    collection_name="docbot_documents",
                )
            except Exception as exc:
                logger.warning("Failed to load vectorstore: %s", exc)
                self.vectorstore = None
        return self.vectorstore

    def get_retriever(self, k: int | None = None):
        """Get a retriever for indexed documents."""
        k = k or settings.retriever_k
        vectorstore = self.get_vectorstore()
        if vectorstore is None:
            raise RuntimeError("Vectorstore not initialized. Index documents first.")
        retriever = vectorstore.as_retriever(search_kwargs={"k": k})
        logger.info("Created retriever with k=%s", k)
        return retriever

    def search(self, query: str, k: int | None = None) -> List[Document]:
        """Search for similar documents."""
        k = k or settings.retriever_k
        vectorstore = self.get_vectorstore()
        if vectorstore is None:
            raise RuntimeError("Vectorstore not initialized.")
        results = vectorstore.similarity_search(query, k=k)
        logger.info("Found %s similar documents for query", len(results))
        return results

    def search_with_scores(self, query: str, k: int | None = None) -> List[Tuple[Document, float]]:
        """Search for documents with similarity scores."""
        k = k or settings.retriever_k
        vectorstore = self.get_vectorstore()
        if vectorstore is None:
            raise RuntimeError("Vectorstore not initialized.")
        results = vectorstore.similarity_search_with_scores(query, k=k)
        logger.info("Found %s results with scores", len(results))
        return results

    def clear_vectorstore(self) -> bool:
        """Delete all indexed embeddings."""
        try:
            if os.path.exists(self.persist_directory):
                shutil.rmtree(self.persist_directory)
            os.makedirs(self.persist_directory, exist_ok=True)
            self.vectorstore = None
            logger.info("Cleared vectorstore")
            return True
        except Exception as exc:
            logger.error("Error clearing vectorstore: %s", exc)
            return False

