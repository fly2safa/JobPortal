"""
Document retriever for RAG system using vector similarity search.
Retrieves relevant documents based on semantic similarity using ChromaDB.
"""
from typing import List, Optional, Dict, Any
from langchain.schema import Document
from app.ai.rag.vectorstore import docs_vectorstore
from app.core.logging import get_logger

logger = get_logger(__name__)


class Retriever:
    """
    Vector-based retriever using ChromaDB for semantic similarity search.
    Replaces keyword-based search with embedding-based retrieval.
    """
    
    def __init__(self, documents: Optional[List[Document]] = None):
        """
        Initialize retriever with optional documents.
        
        Args:
            documents: Optional list of documents to index (if not already indexed)
        """
        self.vectorstore = docs_vectorstore
        
        # Index documents if provided and collection is empty
        if documents and self.vectorstore.get_collection_count() == 0:
            try:
                self.vectorstore.add_documents(documents)
                logger.info(f"Indexed {len(documents)} documents in vector store")
            except Exception as e:
                logger.error(f"Failed to index documents: {e}")
    
    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Retrieve top-k most relevant documents using semantic similarity.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            filter: Optional metadata filter (e.g., {"category": "job_seeker"})
            
        Returns:
            List of relevant documents
        """
        try:
            # Perform vector similarity search
            results = self.vectorstore.similarity_search(
                query=query,
                k=top_k,
                filter=filter
            )
            
            logger.info(f"Retrieved {len(results)} documents for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            # Fallback to empty results
            return []
    
    def retrieve_with_scores(
        self,
        query: str,
        top_k: int = 3,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """
        Retrieve documents with relevance scores.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            filter: Optional metadata filter
            
        Returns:
            List of (document, score) tuples
        """
        try:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=top_k,
                filter=filter
            )
            
            logger.info(f"Retrieved {len(results)} documents with scores")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving documents with scores: {e}")
            return []
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add new documents to the vector store.
        
        Args:
            documents: List of documents to add
            
        Returns:
            List of document IDs
        """
        try:
            doc_ids = self.vectorstore.add_documents(documents)
            logger.info(f"Added {len(documents)} documents to retriever")
            return doc_ids
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return []

