"""
Embeddings module for generating vector embeddings from text.

This module provides a unified interface for generating embeddings using:
1. OpenAI text-embedding-3-small (primary)
2. HuggingFace sentence-transformers (fallback)

The embeddings are used for semantic search in job recommendations and candidate matching.
"""

from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmbeddingsProvider:
    """
    Provides embeddings with automatic fallback between OpenAI and HuggingFace.
    """
    
    def __init__(self):
        self._openai_embeddings: Optional[OpenAIEmbeddings] = None
        self._huggingface_embeddings: Optional[HuggingFaceEmbeddings] = None
        self._current_provider: Optional[str] = None
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize embeddings providers based on available API keys."""
        # Try OpenAI first (primary provider)
        if settings.OPENAI_API_KEY:
            try:
                self._openai_embeddings = OpenAIEmbeddings(
                    model="text-embedding-3-small",
                    openai_api_key=settings.OPENAI_API_KEY
                )
                self._current_provider = "openai"
                logger.info("✅ Initialized OpenAI embeddings (text-embedding-3-small)")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize OpenAI embeddings: {e}")
        
        # Initialize HuggingFace as fallback
        try:
            self._huggingface_embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",  # Fast, efficient model
                model_kwargs={'device': 'cpu'},  # Use CPU for compatibility
                encode_kwargs={'normalize_embeddings': True}
            )
            if not self._current_provider:
                self._current_provider = "huggingface"
                logger.info("✅ Using HuggingFace embeddings (all-MiniLM-L6-v2) as primary")
        except Exception as e:
            logger.error(f"❌ Failed to initialize HuggingFace embeddings: {e}")
            if not self._current_provider:
                raise RuntimeError("No embedding provider available")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of documents.
        
        Args:
            texts: List of text documents to embed
            
        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        if not texts:
            return []
        
        # Try OpenAI first
        if self._openai_embeddings:
            try:
                embeddings = self._openai_embeddings.embed_documents(texts)
                logger.debug(f"Generated {len(embeddings)} embeddings using OpenAI")
                return embeddings
            except Exception as e:
                logger.warning(f"⚠️ OpenAI embeddings failed, falling back to HuggingFace: {e}")
        
        # Fallback to HuggingFace
        if self._huggingface_embeddings:
            try:
                embeddings = self._huggingface_embeddings.embed_documents(texts)
                logger.debug(f"Generated {len(embeddings)} embeddings using HuggingFace")
                return embeddings
            except Exception as e:
                logger.error(f"❌ HuggingFace embeddings failed: {e}")
                raise
        
        raise RuntimeError("No embedding provider available")
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query text.
        
        Args:
            text: Query text to embed
            
        Returns:
            Embedding vector (list of floats)
        """
        if not text:
            raise ValueError("Text cannot be empty")
        
        # Try OpenAI first
        if self._openai_embeddings:
            try:
                embedding = self._openai_embeddings.embed_query(text)
                logger.debug(f"Generated query embedding using OpenAI")
                return embedding
            except Exception as e:
                logger.warning(f"⚠️ OpenAI embeddings failed, falling back to HuggingFace: {e}")
        
        # Fallback to HuggingFace
        if self._huggingface_embeddings:
            try:
                embedding = self._huggingface_embeddings.embed_query(text)
                logger.debug(f"Generated query embedding using HuggingFace")
                return embedding
            except Exception as e:
                logger.error(f"❌ HuggingFace embeddings failed: {e}")
                raise
        
        raise RuntimeError("No embedding provider available")
    
    def get_current_provider(self) -> str:
        """Get the name of the current primary embedding provider."""
        return self._current_provider or "none"


# Global embeddings instance
_embeddings_provider: Optional[EmbeddingsProvider] = None


def get_embeddings() -> EmbeddingsProvider:
    """
    Get the global embeddings provider instance.
    
    Returns:
        EmbeddingsProvider instance
    """
    global _embeddings_provider
    if _embeddings_provider is None:
        _embeddings_provider = EmbeddingsProvider()
    return _embeddings_provider

