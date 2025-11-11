"""
Text splitter for RAG system.
Splits documents into smaller chunks for better retrieval.
"""
from typing import List
from app.ai.rag.loader import Document


class TextSplitter:
    """
    Splits documents into smaller chunks for embedding and retrieval.
    """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize text splitter.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks.
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of document chunks
        """
        chunks = []
        
        for doc in documents:
            doc_chunks = self._split_text(doc.page_content)
            
            for i, chunk_text in enumerate(doc_chunks):
                chunk = Document(
                    page_content=chunk_text,
                    metadata={
                        **doc.metadata,
                        "chunk_index": i,
                        "total_chunks": len(doc_chunks)
                    }
                )
                chunks.append(chunk)
        
        return chunks
    
    def _split_text(self, text: str) -> List[str]:
        """
        Split text into chunks.
        
        Args:
            text: Text to split
            
        Returns:
            List of text chunks
        """
        # Remove extra whitespace
        text = " ".join(text.split())
        
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Find the end of this chunk
            end = start + self.chunk_size
            
            # If we're not at the end of the text, try to break at a sentence or word boundary
            if end < len(text):
                # Try to find a period followed by space
                period_pos = text.rfind(". ", start, end)
                if period_pos > start + self.chunk_size // 2:
                    end = period_pos + 1
                else:
                    # Try to find a space
                    space_pos = text.rfind(" ", start, end)
                    if space_pos > start + self.chunk_size // 2:
                        end = space_pos
            
            chunks.append(text[start:end].strip())
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start < 0:
                start = 0
        
        return chunks

