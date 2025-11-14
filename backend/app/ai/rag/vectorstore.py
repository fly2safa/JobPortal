"""
ChromaDB vector store for semantic search and retrieval.
Stores document embeddings and performs similarity search.
"""
from typing import List, Optional, Dict, Any
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from app.ai.rag.embeddings import embedding_service
from app.core.logging import get_logger
from pathlib import Path

logger = get_logger(__name__)


class VectorStore:
    """
    ChromaDB-based vector store for document embeddings and similarity search.
    """
    
    def __init__(
        self,
        collection_name: str = "jobportal_docs",
        persist_directory: Optional[str] = None
    ):
        """
        Initialize ChromaDB vector store.
        
        Args:
            collection_name: Name of the ChromaDB collection
            persist_directory: Directory to persist the database (None for in-memory)
        """
        self.collection_name = collection_name
        
        # Set up persist directory
        if persist_directory is None:
            persist_directory = str(Path(__file__).parent.parent.parent / "data" / "chroma_db")
        
        self.persist_directory = persist_directory
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Initialize LangChain Chroma wrapper
            self.vectorstore = Chroma(
                client=self.client,
                collection_name=self.collection_name,
                embedding_function=embedding_service.embeddings,
                persist_directory=self.persist_directory
            )
            
            logger.info(f"Initialized ChromaDB vector store: {collection_name} at {persist_directory}")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def add_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of LangChain Document objects
            ids: Optional list of document IDs
            
        Returns:
            List of document IDs
        """
        try:
            doc_ids = self.vectorstore.add_documents(documents=documents, ids=ids)
            logger.info(f"Added {len(documents)} documents to vector store")
            return doc_ids
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Perform similarity search for a query.
        
        Args:
            query: Search query
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of relevant documents
        """
        try:
            results = self.vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter
            )
            logger.info(f"Similarity search returned {len(results)} results for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            return []
    
    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[tuple[Document, float]]:
        """
        Perform similarity search with relevance scores.
        
        Args:
            query: Search query
            k: Number of results to return
            filter: Optional metadata filter
            
        Returns:
            List of (document, score) tuples
        """
        try:
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter
            )
            logger.info(f"Similarity search with scores returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search with scores: {e}")
            return []
    
    def delete_collection(self):
        """Delete the entire collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.warning(f"Error deleting collection: {e}")
    
    def get_collection_count(self) -> int:
        """
        Get the number of documents in the collection.
        
        Returns:
            Number of documents
        """
        try:
            collection = self.client.get_collection(name=self.collection_name)
            return collection.count()
        except Exception as e:
            logger.error(f"Error getting collection count: {e}")
            return 0
    
    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Get a LangChain retriever interface.
        
        Args:
            search_kwargs: Optional search parameters (e.g., {'k': 4})
            
        Returns:
            LangChain retriever
        """
        if search_kwargs is None:
            search_kwargs = {'k': 4}
        
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)


# Global vector store instances
job_vectorstore = VectorStore(collection_name="jobs", persist_directory=None)
user_vectorstore = VectorStore(collection_name="users", persist_directory=None)
docs_vectorstore = VectorStore(collection_name="docs", persist_directory=None)

