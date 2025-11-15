"""
OpenAI API client for AI-powered features.
Provides a centralized client for OpenAI API interactions.
"""
from typing import Optional, List, Dict, Any
from openai import OpenAI, AsyncOpenAI
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class OpenAIClient:
    """
    Wrapper for OpenAI API client with error handling and logging.
    Supports both synchronous and asynchronous operations.
    """
    
    def __init__(self):
        """Initialize OpenAI clients."""
        if not settings.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not configured. AI features will be disabled.")
            self._client = None
            self._async_client = None
        else:
            self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self._async_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info("OpenAI client initialized successfully")
    
    @property
    def is_available(self) -> bool:
        """Check if OpenAI client is available."""
        return self._client is not None
    
    def create_embedding(
        self,
        text: str,
        model: str = "text-embedding-3-small"
    ) -> Optional[List[float]]:
        """
        Create an embedding for the given text using OpenAI's embedding model.
        
        Args:
            text: Text to embed
            model: Embedding model to use (default: text-embedding-3-small)
            
        Returns:
            Embedding vector as list of floats, or None if unavailable
        """
        if not self.is_available:
            logger.error("OpenAI client not available")
            return None
        
        try:
            logger.debug(f"Creating embedding for text (length: {len(text)})")
            response = self._client.embeddings.create(
                input=text,
                model=model
            )
            embedding = response.data[0].embedding
            logger.debug(f"Embedding created successfully (dimension: {len(embedding)})")
            return embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            return None
    
    async def create_embedding_async(
        self,
        text: str,
        model: str = "text-embedding-3-small"
    ) -> Optional[List[float]]:
        """
        Async version of create_embedding.
        
        Args:
            text: Text to embed
            model: Embedding model to use
            
        Returns:
            Embedding vector as list of floats, or None if unavailable
        """
        if not self.is_available:
            logger.error("OpenAI client not available")
            return None
        
        try:
            logger.debug(f"Creating embedding async for text (length: {len(text)})")
            response = await self._async_client.embeddings.create(
                input=text,
                model=model
            )
            embedding = response.data[0].embedding
            logger.debug(f"Embedding created successfully (dimension: {len(embedding)})")
            return embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            return None
    
    def create_embeddings_batch(
        self,
        texts: List[str],
        model: str = "text-embedding-3-small"
    ) -> Optional[List[List[float]]]:
        """
        Create embeddings for multiple texts in a single API call.
        
        Args:
            texts: List of texts to embed
            model: Embedding model to use
            
        Returns:
            List of embedding vectors, or None if unavailable
        """
        if not self.is_available:
            logger.error("OpenAI client not available")
            return None
        
        try:
            logger.debug(f"Creating batch embeddings for {len(texts)} texts")
            response = self._client.embeddings.create(
                input=texts,
                model=model
            )
            embeddings = [item.embedding for item in response.data]
            logger.debug(f"Batch embeddings created successfully")
            return embeddings
        except Exception as e:
            logger.error(f"Error creating batch embeddings: {str(e)}")
            return None
    
    async def create_embeddings_batch_async(
        self,
        texts: List[str],
        model: str = "text-embedding-3-small"
    ) -> Optional[List[List[float]]]:
        """
        Async version of create_embeddings_batch.
        
        Args:
            texts: List of texts to embed
            model: Embedding model to use
            
        Returns:
            List of embedding vectors, or None if unavailable
        """
        if not self.is_available:
            logger.error("OpenAI client not available")
            return None
        
        try:
            logger.debug(f"Creating batch embeddings async for {len(texts)} texts")
            response = await self._async_client.embeddings.create(
                input=texts,
                model=model
            )
            embeddings = [item.embedding for item in response.data]
            logger.debug(f"Batch embeddings created successfully")
            return embeddings
        except Exception as e:
            logger.error(f"Error creating batch embeddings: {str(e)}")
            return None
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Optional[str]:
        """
        Create a chat completion using OpenAI's chat model.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model: Chat model to use (default: gpt-4o-mini)
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional arguments for the API
            
        Returns:
            Generated text response, or None if unavailable
        """
        if not self.is_available:
            logger.error("OpenAI client not available")
            return None
        
        try:
            logger.debug(f"Creating chat completion with {len(messages)} messages")
            response = self._client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            content = response.choices[0].message.content
            logger.debug("Chat completion created successfully")
            return content
        except Exception as e:
            logger.error(f"Error creating chat completion: {str(e)}")
            return None
    
    async def chat_completion_async(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Optional[str]:
        """
        Async version of chat_completion.
        
        Args:
            messages: List of message dictionaries
            model: Chat model to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional arguments
            
        Returns:
            Generated text response, or None if unavailable
        """
        if not self.is_available:
            logger.error("OpenAI client not available")
            return None
        
        try:
            logger.debug(f"Creating chat completion async with {len(messages)} messages")
            response = await self._async_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            content = response.choices[0].message.content
            logger.debug("Chat completion created successfully")
            return content
        except Exception as e:
            logger.error(f"Error creating chat completion: {str(e)}")
            return None


# Global OpenAI client instance
openai_client = OpenAIClient()

