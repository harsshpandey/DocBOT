"""
Retrieval-Augmented Generation (RAG) agent.
"""
from typing import Dict, List, Optional
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from utils.config import settings
from utils.logger import logger


class RAGAgent:
    """RAG agent combining retrieval with Gemini generation."""

    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = ChatGoogleGenerativeAI(
            model=settings.google_llm_model,
            api_key=settings.google_api_key,
            temperature=settings.temperature,
            max_output_tokens=2048,
        )
        self.system_prompt = """You are a helpful assistant that answers questions about organizational policies, rules, and guidelines based only on the provided context.

Instructions:
1. Base every answer strictly on the supplied context.
2. If information is missing, reply with: "I don't have information about that in the knowledge base."
3. Cite source document names when appropriate.
4. Provide clear steps, eligibility, and policy notes when relevant.
5. Keep responses professional and concise.

CONTEXT:
{context}
"""
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_prompt),
                ("human", "{question}"),
            ]
        )
        logger.info("Initialized RAG Agent with model %s", settings.google_llm_model)

    def retrieve_context(self, question: str) -> List[Document]:
        """Retrieve relevant documents for a question."""
        documents = self.retriever.invoke(question)
        logger.info("Retrieved %s documents for question", len(documents))
        return documents

    def format_context(self, documents: List[Document]) -> str:
        """Format retrieved documents into a single context string."""
        parts = []
        for idx, doc in enumerate(documents, 1):
            source = doc.metadata.get("source", "Unknown Source")
            content = doc.page_content.strip()
            parts.append(f"[Source {idx}: {source}]\n{content}")
        return "\n\n---\n\n".join(parts)

    def answer_question(self, question: str) -> Dict:
        """Answer a question using RAG pipeline."""
        start = time.time()
        try:
            documents = self.retrieve_context(question)
            if not documents:
                return {
                    "answer": "I couldn't find any relevant information in the knowledge base.",
                    "sources": [],
                    "chunks_used": 0,
                    "model": settings.google_llm_model,
                    "confidence": 0.0,
                    "processing_time_ms": (time.time() - start) * 1000,
                    "error": "No documents found",
                }

            context = self.format_context(documents)
            prompt = self.prompt_template.format_prompt(context=context, question=question)
            response = self.llm.invoke(prompt.to_string())
            answer_text = getattr(response, "content", str(response))

            sources = [
                {
                    "name": doc.metadata.get("source", "Unknown"),
                    "relevance_score": None,
                    "chunk_index": None,
                }
                for doc in documents
            ]

            processing_time = (time.time() - start) * 1000
            return {
                "answer": answer_text,
                "sources": sources,
                "chunks_used": len(documents),
                "model": settings.google_llm_model,
                "confidence": 0.85,
                "processing_time_ms": processing_time,
            }
        except Exception as exc:
            logger.error("Error answering question: %s", exc)
            processing_time = (time.time() - start) * 1000
            return {
                "answer": f"An error occurred while processing your question: {exc}",
                "sources": [],
                "chunks_used": 0,
                "model": settings.google_llm_model,
                "confidence": 0.0,
                "processing_time_ms": processing_time,
                "error": str(exc),
            }

