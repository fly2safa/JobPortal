"""
Document retriever for RAG system.
Retrieves relevant documents based on user queries.
"""
from typing import List, Optional
from app.ai.rag.loader import Document


class Retriever:
    """
    Simple keyword-based retriever for finding relevant documents.
    In production, this would use vector embeddings and similarity search.
    """
    
    def __init__(self, documents: List[Document]):
        """
        Initialize retriever with documents.
        
        Args:
            documents: List of documents to search
        """
        self.documents = documents
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Retrieve top-k most relevant documents for a query.
        
        Args:
            query: User query
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        # Simple keyword-based scoring
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_docs = []
        
        for doc in self.documents:
            content_lower = doc.page_content.lower()
            
            # Calculate relevance score
            score = 0
            
            # Exact phrase match (highest weight)
            if query_lower in content_lower:
                score += 10
            
            # Individual word matches
            for word in query_words:
                if len(word) > 3:  # Ignore short words
                    count = content_lower.count(word)
                    score += count * 2
            
            # Category boost based on query keywords
            metadata = doc.metadata
            if self._is_job_seeker_query(query_lower) and metadata.get("category") == "job_seeker":
                score += 3
            elif self._is_employer_query(query_lower) and metadata.get("category") == "employer":
                score += 3
            elif self._is_feature_query(query_lower) and metadata.get("category") == "features":
                score += 3
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Sort by score and return top-k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:top_k]]
    
    def _is_job_seeker_query(self, query: str) -> bool:
        """Check if query is related to job seekers."""
        keywords = ["apply", "application", "resume", "job search", "find job", "career"]
        return any(keyword in query for keyword in keywords)
    
    def _is_employer_query(self, query: str) -> bool:
        """Check if query is related to employers."""
        keywords = ["post job", "employer", "candidate", "hire", "review application", "shortlist"]
        return any(keyword in query for keyword in keywords)
    
    def _is_feature_query(self, query: str) -> bool:
        """Check if query is related to AI features."""
        keywords = ["ai", "recommendation", "cover letter", "parse", "match"]
        return any(keyword in query for keyword in keywords)

