"""
Conversation model for AI assistant chat history.
"""
from datetime import datetime
from typing import List, Optional
from enum import Enum
from beanie import Document
from pydantic import Field


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(dict):
    """Individual message in a conversation."""
    role: MessageRole
    content: str
    timestamp: datetime


class Conversation(Document):
    """Conversation document model for storing chat history."""
    
    # User reference
    user_id: str = Field(..., index=True)
    
    # Conversation metadata
    title: Optional[str] = Field(None, max_length=200)
    messages: List[dict] = Field(default_factory=list)
    
    # Context (optional - for job-specific or application-specific conversations)
    context_type: Optional[str] = Field(None, index=True)  # "job", "application", "general"
    context_id: Optional[str] = None  # job_id or application_id
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "conversations"
        indexes = [
            "user_id",
            "context_type",
            "created_at",
            ("user_id", "context_type"),
        ]
    
    def add_message(self, role: MessageRole, content: str):
        """
        Add a message to the conversation.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.updated_at = datetime.utcnow()
        
        # Auto-generate title from first user message if not set
        if not self.title and role == MessageRole.USER and len(self.messages) == 1:
            self.title = content[:50] + ("..." if len(content) > 50 else "")
    
    def get_messages_for_llm(self, limit: Optional[int] = None) -> List[dict]:
        """
        Get messages formatted for LLM API.
        
        Args:
            limit: Optional limit on number of messages to return (most recent)
            
        Returns:
            List of messages in format: [{"role": "user", "content": "..."}]
        """
        messages = self.messages if not limit else self.messages[-limit:]
        return [{"role": msg["role"], "content": msg["content"]} for msg in messages]

