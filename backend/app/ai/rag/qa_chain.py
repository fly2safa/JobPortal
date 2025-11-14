"""
Question-answering chain for RAG system.
Combines retrieval with LLM to answer user questions.
"""
from typing import List, Optional, Dict, Any
from app.ai.rag.loader import DocumentLoader, Document
from app.ai.rag.splitter import TextSplitter
from app.ai.rag.retriever import Retriever
from app.ai.providers import get_llm, ProviderError
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class QAChain:
    """
    Question-answering chain that uses RAG to answer user questions.
    """
    
    def __init__(self):
        """Initialize QA chain with document loader and retriever."""
        self.loader = DocumentLoader()
        self.splitter = TextSplitter(chunk_size=500, chunk_overlap=50)
        self.retriever: Optional[Retriever] = None
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Load and index documents for retrieval."""
        try:
            # Load documents
            documents = self.loader.load_job_portal_docs()
            
            # Split into chunks
            chunks = self.splitter.split_documents(documents)
            
            # Initialize retriever
            self.retriever = Retriever(chunks)
            
            logger.info(f"Knowledge base initialized with {len(chunks)} document chunks")
        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {e}")
            # Initialize with empty retriever as fallback
            self.retriever = Retriever([])
    
    async def answer_question(
        self,
        question: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Answer a user question using RAG.
        
        Args:
            question: User's question
            conversation_history: Previous messages in the conversation
            user_context: Optional context about the user (role, profile, etc.)
            
        Returns:
            Answer string
        """
        try:
            # Retrieve relevant documents
            relevant_docs = self.retriever.retrieve(question, top_k=3)
            
            # Build context from retrieved documents
            context = self._build_context(relevant_docs)
            
            # Build system prompt
            system_prompt = self._build_system_prompt(context, user_context)
            
            # Build messages for OpenAI
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add conversation history (limit to last 10 messages)
            if conversation_history:
                messages.extend(conversation_history[-10:])
            
            # Add current question
            messages.append({"role": "user", "content": question})
            
            # Get LLM with automatic fallback
            try:
                llm = get_llm(temperature=0.7, max_tokens=500)
                
                # Invoke LLM
                answer = llm.invoke(messages).content
                logger.info(f"Generated answer for question: {question[:50]}...")
                
                return answer
                
            except ProviderError as e:
                logger.error(f"All AI providers failed: {e}")
                return self._fallback_response(question, relevant_docs)
            
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            return "I apologize, but I'm having trouble processing your question right now. Please try again or contact support if the issue persists."
    
    def _build_context(self, documents: List[Document]) -> str:
        """Build context string from retrieved documents."""
        if not documents:
            return "No specific documentation found for this query."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"[Document {i}]\n{doc.page_content}\n")
        
        return "\n".join(context_parts)
    
    def _build_system_prompt(self, context: str, user_context: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt for the LLM."""
        user_role = "user"
        if user_context:
            user_role = user_context.get("role", "user")
        
        prompt = f"""You are a helpful AI assistant for TalentNest, a job portal platform.
Your role is to help users navigate the platform, answer questions about features, and provide career advice.

User Role: {user_role}

Relevant Documentation:
{context}

Guidelines:
- Be friendly, professional, and helpful
- Provide accurate information based on the documentation
- If you're not sure about something, admit it and suggest contacting support
- For job seekers: focus on job search, applications, and career development
- For employers: focus on posting jobs, reviewing candidates, and hiring
- Keep responses concise but informative
- Use bullet points or numbered lists when appropriate
- If the question is not related to the job portal, politely redirect to platform-related topics
"""
        return prompt
    
    def _fallback_response(self, question: str, relevant_docs: List[Document]) -> str:
        """Provide a fallback response when OpenAI API is not available."""
        if not relevant_docs:
            return "I don't have specific information about that. Please contact support for assistance."
        
        # Return the most relevant document content
        return f"Based on our documentation:\n\n{relevant_docs[0].page_content[:500]}..."


# Global QA chain instance
qa_chain = QAChain()

