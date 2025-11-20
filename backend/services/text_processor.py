"""
Text processing and chunking service.
"""
from typing import List
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from utils.logger import logger
from utils.config import settings


class TextProcessor:
    """Process and chunk text documents."""

    def __init__(self, chunk_size: int | None = None, chunk_overlap: int | None = None):
        self.chunk_size = chunk_size or settings.chunk_size
        self.chunk_overlap = chunk_overlap or settings.chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len,
        )
        logger.info(
            "Initialized TextProcessor: chunk_size=%s, overlap=%s",
            self.chunk_size,
            self.chunk_overlap,
        )

    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s\.\,\!\?\-\(\)\:]", " ", text)
        text = re.sub(r" +", " ", text)
        return text.strip()

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks."""
        chunks = self.splitter.split_documents(documents)
        logger.info("Split %s documents into %s chunks", len(documents), len(chunks))
        return chunks

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """Clean and chunk documents."""
        for doc in documents:
            doc.page_content = self.clean_text(doc.page_content)
        chunks = self.split_documents(documents)
        logger.info("Processed %s documents into %s chunks", len(documents), len(chunks))
        return chunks

