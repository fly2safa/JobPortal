"""
Vector store module using ChromaDB for semantic search.

This module provides vector storage and similarity search for:
1. Job postings - for job recommendations to job seekers
2. User profiles - for candidate matching for employers

Uses ChromaDB as the vector database with embeddings from OpenAI or HuggingFace.
"""

from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from app.ai.rag.embeddings import get_embeddings
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class VectorStore:
    """
    Manages vector storage and similarity search using ChromaDB.
    """
    
    def __init__(self):
        self.embeddings = get_embeddings()
        self.client: Optional[chromadb.Client] = None
        self.jobs_collection: Optional[chromadb.Collection] = None
        self.profiles_collection: Optional[chromadb.Collection] = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize ChromaDB client and collections."""
        try:
            # Initialize ChromaDB client (in-memory for development, persistent for production)
            chroma_settings = Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
            
            # Use persistent storage if CHROMADB_PATH is set, otherwise in-memory
            chromadb_path = getattr(settings, 'CHROMADB_PATH', None)
            if chromadb_path:
                self.client = chromadb.PersistentClient(path=chromadb_path, settings=chroma_settings)
                logger.info(f"✅ Initialized ChromaDB with persistent storage at {chromadb_path}")
            else:
                self.client = chromadb.Client(chroma_settings)
                logger.info("✅ Initialized ChromaDB with in-memory storage")
            
            # Get or create collections
            self.jobs_collection = self.client.get_or_create_collection(
                name="job_postings",
                metadata={"description": "Job postings for semantic search and recommendations"}
            )
            
            self.profiles_collection = self.client.get_or_create_collection(
                name="user_profiles",
                metadata={"description": "User profiles for candidate matching"}
            )
            
            logger.info(f"✅ ChromaDB collections ready: jobs={self.jobs_collection.count()}, profiles={self.profiles_collection.count()}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize ChromaDB: {e}")
            raise
    
    def add_job(self, job_id: str, job_data: Dict[str, Any]) -> bool:
        """
        Add or update a job posting in the vector store.
        
        Args:
            job_id: Unique job identifier
            job_data: Job data dictionary containing title, description, skills, etc.
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a rich text representation for embedding
            job_text = self._create_job_text(job_data)
            
            # Generate embedding
            embedding = self.embeddings.embed_query(job_text)
            
            # Store in ChromaDB
            self.jobs_collection.upsert(
                ids=[job_id],
                embeddings=[embedding],
                documents=[job_text],
                metadatas=[{
                    "job_id": job_id,
                    "title": job_data.get("title", ""),
                    "company": job_data.get("company_name", ""),
                    "location": job_data.get("location", ""),
                    "skills": ",".join(job_data.get("skills", [])),
                    "experience_level": job_data.get("experience_level", ""),
                }]
            )
            
            logger.debug(f"Added job {job_id} to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add job {job_id} to vector store: {e}")
            return False
    
    def add_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """
        Add or update a user profile in the vector store.
        
        Args:
            user_id: Unique user identifier
            profile_data: User profile data containing skills, experience, education, etc.
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a rich text representation for embedding
            profile_text = self._create_profile_text(profile_data)
            
            # Generate embedding
            embedding = self.embeddings.embed_query(profile_text)
            
            # Store in ChromaDB
            self.profiles_collection.upsert(
                ids=[user_id],
                embeddings=[embedding],
                documents=[profile_text],
                metadatas=[{
                    "user_id": user_id,
                    "name": profile_data.get("full_name", ""),
                    "email": profile_data.get("email", ""),
                    "skills": ",".join(profile_data.get("skills", [])),
                    "experience_years": str(profile_data.get("experience_years", 0)),
                }]
            )
            
            logger.debug(f"Added profile {user_id} to vector store")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add profile {user_id} to vector store: {e}")
            return False
    
    def search_jobs(self, query_text: str, n_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar jobs using semantic similarity.
        
        Args:
            query_text: Query text (user profile summary or search query)
            n_results: Number of results to return
            
        Returns:
            List of job matches with similarity scores
        """
        try:
            if self.jobs_collection.count() == 0:
                logger.warning("Jobs collection is empty")
                return []
            
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query_text)
            
            # Search ChromaDB
            results = self.jobs_collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, self.jobs_collection.count())
            )
            
            # Format results
            matches = []
            if results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):
                    matches.append({
                        'job_id': results['ids'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else 0,
                        'similarity_score': 1 - results['distances'][0][i] if 'distances' in results else 1.0,
                        'metadata': results['metadatas'][0][i] if 'metadatas' in results else {},
                        'document': results['documents'][0][i] if 'documents' in results else ""
                    })
            
            logger.debug(f"Found {len(matches)} job matches for query")
            return matches
            
        except Exception as e:
            logger.error(f"Failed to search jobs: {e}")
            return []
    
    def search_profiles(self, query_text: str, n_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for similar user profiles using semantic similarity.
        
        Args:
            query_text: Query text (job description or requirements)
            n_results: Number of results to return
            
        Returns:
            List of profile matches with similarity scores
        """
        try:
            if self.profiles_collection.count() == 0:
                logger.warning("Profiles collection is empty")
                return []
            
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query_text)
            
            # Search ChromaDB
            results = self.profiles_collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, self.profiles_collection.count())
            )
            
            # Format results
            matches = []
            if results['ids'] and len(results['ids'][0]) > 0:
                for i in range(len(results['ids'][0])):
                    matches.append({
                        'user_id': results['ids'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else 0,
                        'similarity_score': 1 - results['distances'][0][i] if 'distances' in results else 1.0,
                        'metadata': results['metadatas'][0][i] if 'metadatas' in results else {},
                        'document': results['documents'][0][i] if 'documents' in results else ""
                    })
            
            logger.debug(f"Found {len(matches)} profile matches for query")
            return matches
            
        except Exception as e:
            logger.error(f"Failed to search profiles: {e}")
            return []
    
    def delete_job(self, job_id: str) -> bool:
        """Delete a job from the vector store."""
        try:
            self.jobs_collection.delete(ids=[job_id])
            logger.debug(f"Deleted job {job_id} from vector store")
            return True
        except Exception as e:
            logger.error(f"Failed to delete job {job_id}: {e}")
            return False
    
    def delete_profile(self, user_id: str) -> bool:
        """Delete a user profile from the vector store."""
        try:
            self.profiles_collection.delete(ids=[user_id])
            logger.debug(f"Deleted profile {user_id} from vector store")
            return True
        except Exception as e:
            logger.error(f"Failed to delete profile {user_id}: {e}")
            return False
    
    def _create_job_text(self, job_data: Dict[str, Any]) -> str:
        """Create a rich text representation of a job for embedding."""
        parts = []
        
        if job_data.get("title"):
            parts.append(f"Job Title: {job_data['title']}")
        
        if job_data.get("company_name"):
            parts.append(f"Company: {job_data['company_name']}")
        
        if job_data.get("location"):
            parts.append(f"Location: {job_data['location']}")
        
        if job_data.get("description"):
            parts.append(f"Description: {job_data['description']}")
        
        if job_data.get("requirements"):
            requirements = job_data['requirements']
            if isinstance(requirements, list):
                parts.append(f"Requirements: {', '.join(requirements)}")
            else:
                parts.append(f"Requirements: {requirements}")
        
        if job_data.get("skills"):
            skills = job_data['skills']
            if isinstance(skills, list):
                parts.append(f"Required Skills: {', '.join(skills)}")
            else:
                parts.append(f"Required Skills: {skills}")
        
        if job_data.get("experience_level"):
            parts.append(f"Experience Level: {job_data['experience_level']}")
        
        if job_data.get("job_type"):
            parts.append(f"Job Type: {job_data['job_type']}")
        
        return "\n".join(parts)
    
    def _create_profile_text(self, profile_data: Dict[str, Any]) -> str:
        """Create a rich text representation of a user profile for embedding."""
        parts = []
        
        if profile_data.get("full_name"):
            parts.append(f"Name: {profile_data['full_name']}")
        
        if profile_data.get("skills"):
            skills = profile_data['skills']
            if isinstance(skills, list):
                parts.append(f"Skills: {', '.join(skills)}")
            else:
                parts.append(f"Skills: {skills}")
        
        if profile_data.get("experience_years") is not None:
            parts.append(f"Years of Experience: {profile_data['experience_years']}")
        
        if profile_data.get("education"):
            parts.append(f"Education: {profile_data['education']}")
        
        if profile_data.get("work_experience"):
            parts.append(f"Work Experience: {profile_data['work_experience']}")
        
        if profile_data.get("summary"):
            parts.append(f"Professional Summary: {profile_data['summary']}")
        
        return "\n".join(parts)
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about the vector store."""
        return {
            "jobs_count": self.jobs_collection.count() if self.jobs_collection else 0,
            "profiles_count": self.profiles_collection.count() if self.profiles_collection else 0,
        }


# Global vector store instance
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """
    Get the global vector store instance.
    
    Returns:
        VectorStore instance
    """
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store

