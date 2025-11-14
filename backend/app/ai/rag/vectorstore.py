"""
Vector store for similarity search using embeddings.
Provides in-memory vector storage and cosine similarity search.
"""
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from app.ai.rag.embeddings import embeddings_handler
from app.core.logging import get_logger

logger = get_logger(__name__)


class VectorStore:
    """
    In-memory vector store for similarity search.
    Stores embeddings and performs cosine similarity calculations.
    """
    
    def __init__(self):
        """Initialize the vector store."""
        self.vectors: List[np.ndarray] = []
        self.metadata: List[Dict[str, Any]] = []
        self.ids: List[str] = []
    
    def add_vectors(
        self,
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
        ids: List[str]
    ):
        """
        Add vectors to the store.
        
        Args:
            vectors: List of embedding vectors
            metadata: List of metadata dictionaries (one per vector)
            ids: List of unique IDs (one per vector)
        """
        if len(vectors) != len(metadata) or len(vectors) != len(ids):
            raise ValueError("vectors, metadata, and ids must have the same length")
        
        for vector, meta, vector_id in zip(vectors, metadata, ids):
            if vector is None:
                logger.warning(f"Skipping None vector for id {vector_id}")
                continue
            
            self.vectors.append(np.array(vector))
            self.metadata.append(meta)
            self.ids.append(vector_id)
        
        logger.info(f"Added {len(vectors)} vectors to store (total: {len(self.vectors)})")
    
    def add_vector(
        self,
        vector: List[float],
        metadata: Dict[str, Any],
        vector_id: str
    ):
        """
        Add a single vector to the store.
        
        Args:
            vector: Embedding vector
            metadata: Metadata dictionary
            vector_id: Unique ID
        """
        if vector is None:
            logger.warning(f"Skipping None vector for id {vector_id}")
            return
        
        self.vectors.append(np.array(vector))
        self.metadata.append(metadata)
        self.ids.append(vector_id)
    
    def similarity_search(
        self,
        query_vector: List[float],
        k: int = 10,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Dict[str, Any], float, str]]:
        """
        Search for similar vectors using cosine similarity.
        
        Args:
            query_vector: Query embedding vector
            k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of (metadata, similarity_score, id) tuples, sorted by score
        """
        if not self.vectors:
            logger.warning("Vector store is empty")
            return []
        
        if query_vector is None:
            logger.error("Query vector is None")
            return []
        
        # Convert query to numpy array
        query_np = np.array(query_vector)
        
        # Calculate cosine similarities
        similarities = []
        for i, vector in enumerate(self.vectors):
            # Apply metadata filters if provided
            if filter_metadata:
                match = all(
                    self.metadata[i].get(key) == value
                    for key, value in filter_metadata.items()
                )
                if not match:
                    continue
            
            # Cosine similarity
            similarity = self._cosine_similarity(query_np, vector)
            similarities.append((self.metadata[i], similarity, self.ids[i], i))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k results (metadata, score, id)
        results = [(meta, score, vector_id) for meta, score, vector_id, _ in similarities[:k]]
        
        logger.debug(f"Found {len(results)} similar vectors (requested: {k})")
        return results
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score (0-1)
        """
        # Handle zero vectors
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(vec1, vec2) / (norm1 * norm2)
        
        # Ensure result is in [0, 1] range
        # (cosine similarity is in [-1, 1], we map to [0, 1])
        return float((similarity + 1) / 2)
    
    def get_by_id(self, vector_id: str) -> Optional[Tuple[np.ndarray, Dict[str, Any]]]:
        """
        Get a vector and its metadata by ID.
        
        Args:
            vector_id: Vector ID
            
        Returns:
            (vector, metadata) tuple or None if not found
        """
        try:
            idx = self.ids.index(vector_id)
            return self.vectors[idx], self.metadata[idx]
        except ValueError:
            return None
    
    def remove_by_id(self, vector_id: str) -> bool:
        """
        Remove a vector by ID.
        
        Args:
            vector_id: Vector ID
            
        Returns:
            True if removed, False if not found
        """
        try:
            idx = self.ids.index(vector_id)
            del self.vectors[idx]
            del self.metadata[idx]
            del self.ids[idx]
            logger.debug(f"Removed vector {vector_id}")
            return True
        except ValueError:
            return False
    
    def clear(self):
        """Clear all vectors from the store."""
        self.vectors = []
        self.metadata = []
        self.ids = []
        logger.info("Vector store cleared")
    
    def size(self) -> int:
        """Get the number of vectors in the store."""
        return len(self.vectors)
    
    def update_metadata(self, vector_id: str, metadata: Dict[str, Any]) -> bool:
        """
        Update metadata for a vector.
        
        Args:
            vector_id: Vector ID
            metadata: New metadata
            
        Returns:
            True if updated, False if not found
        """
        try:
            idx = self.ids.index(vector_id)
            self.metadata[idx] = metadata
            return True
        except ValueError:
            return False


class JobVectorStore:
    """
    Specialized vector store for job postings.
    Manages job embeddings and similarity search.
    """
    
    def __init__(self):
        """Initialize the job vector store."""
        self.store = VectorStore()
        self.embeddings = embeddings_handler
    
    async def add_job(self, job: Dict[str, Any]) -> bool:
        """
        Add a job to the vector store.
        
        Args:
            job: Job dictionary with details
            
        Returns:
            True if added successfully
        """
        job_id = str(job.get('id', job.get('_id')))
        
        # Create embedding
        embedding = await self.embeddings.create_job_embedding(job)
        if not embedding:
            logger.error(f"Failed to create embedding for job {job_id}")
            return False
        
        # Add to store
        self.store.add_vector(
            vector=embedding,
            metadata=job,
            vector_id=job_id
        )
        
        logger.debug(f"Added job {job_id} to vector store")
        return True
    
    async def add_jobs_batch(self, jobs: List[Dict[str, Any]]) -> int:
        """
        Add multiple jobs to the vector store.
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            Number of jobs added successfully
        """
        if not jobs:
            return 0
        
        # Create embeddings for all jobs
        embedding_texts = [self.embeddings.create_job_embedding_text(job) for job in jobs]
        embeddings = await self.embeddings.create_embeddings_batch(embedding_texts)
        
        # Add to store
        vectors = []
        metadata = []
        ids = []
        
        for job, embedding in zip(jobs, embeddings):
            if embedding:
                job_id = str(job.get('id', job.get('_id')))
                vectors.append(embedding)
                metadata.append(job)
                ids.append(job_id)
        
        if vectors:
            self.store.add_vectors(vectors, metadata, ids)
        
        logger.info(f"Added {len(vectors)}/{len(jobs)} jobs to vector store")
        return len(vectors)
    
    async def find_similar_jobs(
        self,
        user_profile: Dict[str, Any],
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Find jobs similar to a user profile.
        
        Args:
            user_profile: User profile dictionary
            k: Number of results
            filters: Optional metadata filters
            
        Returns:
            List of (job, similarity_score) tuples
        """
        # Create user profile embedding
        embedding = await self.embeddings.create_user_profile_embedding(user_profile)
        if not embedding:
            logger.error("Failed to create user profile embedding")
            return []
        
        # Search for similar jobs
        results = self.store.similarity_search(
            query_vector=embedding,
            k=k,
            filter_metadata=filters
        )
        
        # Return (job, score) tuples
        return [(metadata, score) for metadata, score, _ in results]
    
    def clear(self):
        """Clear all jobs from the store."""
        self.store.clear()
    
    def size(self) -> int:
        """Get the number of jobs in the store."""
        return self.store.size()


# Global job vector store instance
job_vector_store = JobVectorStore()

