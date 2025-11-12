"""
Embeddings handler for RAG system.
Manages creation and caching of text embeddings for jobs and user profiles.
"""
from typing import List, Optional, Dict, Any
import hashlib
import json
from app.ai.providers.openai_client import openai_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmbeddingsHandler:
    """
    Handles creation and management of text embeddings.
    Uses OpenAI's text-embedding-3-small model.
    """
    
    def __init__(self):
        """Initialize the embeddings handler."""
        self.client = openai_client
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dim = 1536  # Dimension for text-embedding-3-small
        self._cache: Dict[str, List[float]] = {}
    
    @property
    def is_available(self) -> bool:
        """Check if embeddings are available."""
        return self.client.is_available
    
    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key for the text."""
        return hashlib.md5(text.encode()).hexdigest()
    
    async def create_embedding(
        self,
        text: str,
        use_cache: bool = True
    ) -> Optional[List[float]]:
        """
        Create an embedding for the given text.
        
        Args:
            text: Text to embed
            use_cache: Whether to use cached embeddings
            
        Returns:
            Embedding vector or None if unavailable
        """
        if not self.is_available:
            logger.error("Embeddings not available - OpenAI client not configured")
            return None
        
        # Check cache
        if use_cache:
            cache_key = self._get_cache_key(text)
            if cache_key in self._cache:
                logger.debug("Using cached embedding")
                return self._cache[cache_key]
        
        # Create embedding
        embedding = await self.client.create_embedding_async(
            text=text,
            model=self.embedding_model
        )
        
        # Cache result
        if embedding and use_cache:
            cache_key = self._get_cache_key(text)
            self._cache[cache_key] = embedding
        
        return embedding
    
    async def create_embeddings_batch(
        self,
        texts: List[str],
        use_cache: bool = True
    ) -> List[Optional[List[float]]]:
        """
        Create embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            use_cache: Whether to use cached embeddings
            
        Returns:
            List of embedding vectors
        """
        if not self.is_available:
            logger.error("Embeddings not available")
            return [None] * len(texts)
        
        # Separate cached and uncached texts
        results: List[Optional[List[float]]] = [None] * len(texts)
        uncached_indices = []
        uncached_texts = []
        
        for i, text in enumerate(texts):
            if use_cache:
                cache_key = self._get_cache_key(text)
                if cache_key in self._cache:
                    results[i] = self._cache[cache_key]
                    continue
            
            uncached_indices.append(i)
            uncached_texts.append(text)
        
        # Create embeddings for uncached texts
        if uncached_texts:
            embeddings = await self.client.create_embeddings_batch_async(
                texts=uncached_texts,
                model=self.embedding_model
            )
            
            if embeddings:
                for idx, embedding in zip(uncached_indices, embeddings):
                    results[idx] = embedding
                    
                    # Cache result
                    if use_cache:
                        cache_key = self._get_cache_key(uncached_texts[uncached_indices.index(idx)])
                        self._cache[cache_key] = embedding
        
        return results
    
    def create_job_embedding_text(self, job: Dict[str, Any]) -> str:
        """
        Create a text representation of a job for embedding.
        
        Args:
            job: Job dictionary with details
            
        Returns:
            Formatted text for embedding
        """
        parts = []
        
        # Title and company (most important)
        parts.append(f"Job Title: {job.get('title', '')}")
        parts.append(f"Company: {job.get('company_name', '')}")
        
        # Skills
        if job.get('skills'):
            skills_text = ", ".join(job['skills'])
            parts.append(f"Required Skills: {skills_text}")
        
        # Experience level
        if job.get('experience_level'):
            parts.append(f"Experience Level: {job['experience_level']}")
        
        # Location
        if job.get('location'):
            parts.append(f"Location: {job['location']}")
        
        if job.get('is_remote'):
            parts.append("Remote Work: Available")
        
        # Job type
        if job.get('job_type'):
            parts.append(f"Job Type: {job['job_type']}")
        
        # Description (truncated)
        if job.get('description'):
            desc = job['description'][:500]  # Limit length
            parts.append(f"Description: {desc}")
        
        # Requirements (truncated)
        if job.get('requirements'):
            req = job['requirements'][:300]  # Limit length
            parts.append(f"Requirements: {req}")
        
        return "\n".join(parts)
    
    def create_user_profile_embedding_text(self, user: Dict[str, Any]) -> str:
        """
        Create a text representation of a user profile for embedding.
        
        Args:
            user: User dictionary with profile details
            
        Returns:
            Formatted text for embedding
        """
        parts = []
        
        # Skills (most important for matching)
        if user.get('skills'):
            skills_text = ", ".join(user['skills'])
            parts.append(f"Skills: {skills_text}")
        
        # Experience
        if user.get('experience_years') is not None:
            parts.append(f"Years of Experience: {user['experience_years']}")
        
        # Education
        if user.get('education'):
            parts.append(f"Education: {user['education']}")
        
        # Bio
        if user.get('bio'):
            bio = user['bio'][:500]  # Limit length
            parts.append(f"Professional Summary: {bio}")
        
        # Job title
        if user.get('job_title'):
            parts.append(f"Current/Desired Role: {user['job_title']}")
        
        # Location
        if user.get('location'):
            parts.append(f"Location: {user['location']}")
        
        return "\n".join(parts)
    
    async def create_job_embedding(self, job: Dict[str, Any]) -> Optional[List[float]]:
        """
        Create an embedding for a job posting.
        
        Args:
            job: Job dictionary
            
        Returns:
            Embedding vector or None
        """
        text = self.create_job_embedding_text(job)
        return await self.create_embedding(text)
    
    async def create_user_profile_embedding(self, user: Dict[str, Any]) -> Optional[List[float]]:
        """
        Create an embedding for a user profile.
        
        Args:
            user: User dictionary
            
        Returns:
            Embedding vector or None
        """
        text = self.create_user_profile_embedding_text(user)
        return await self.create_embedding(text)
    
    def clear_cache(self):
        """Clear the embedding cache."""
        self._cache.clear()
        logger.info("Embedding cache cleared")
    
    def get_cache_size(self) -> int:
        """Get the number of cached embeddings."""
        return len(self._cache)


# Global embeddings handler instance
embeddings_handler = EmbeddingsHandler()

