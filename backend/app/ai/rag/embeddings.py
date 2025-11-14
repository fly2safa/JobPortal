"""
Embedding utilities for RAG system using OpenAI and fallback models.
Provides text-to-vector conversion for semantic search.
"""
from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings using OpenAI or fallback models.
    """
    
    def __init__(self, use_openai: bool = True):
        """
        Initialize embedding service.
        
        Args:
            use_openai: If True, use OpenAI embeddings; otherwise use HuggingFace
        """
        self.use_openai = use_openai and bool(settings.OPENAI_API_KEY)
        
        if self.use_openai:
            try:
                # Use OpenAI text-embedding-3-small (as per spec)
                self.embeddings = OpenAIEmbeddings(
                    model="text-embedding-3-small",
                    openai_api_key=settings.OPENAI_API_KEY
                )
                logger.info("Initialized OpenAI embeddings (text-embedding-3-small)")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI embeddings: {e}. Falling back to HuggingFace.")
                self.use_openai = False
        
        if not self.use_openai:
            # Fallback to open-source model (all-MiniLM-L6-v2 as per spec)
            try:
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )
                logger.info("Initialized HuggingFace embeddings (all-MiniLM-L6-v2)")
            except Exception as e:
                logger.error(f"Failed to initialize HuggingFace embeddings: {e}")
                raise
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            List of floats representing the embedding vector
        """
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            Dimension of embedding vectors
        """
        if self.use_openai:
            return 1536  # text-embedding-3-small dimension
        else:
            return 384  # all-MiniLM-L6-v2 dimension


# Global embedding service instance
embedding_service = EmbeddingService()

