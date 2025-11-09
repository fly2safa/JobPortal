"""
Resume model for storing uploaded resumes and parsed data.
"""
from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import Field


class Resume(Document):
    """Resume document model."""
    
    user_id: str = Field(..., index=True)
    file_url: str  # Path to stored file
    file_name: str
    file_size: int  # Size in bytes
    
    # Parsed data
    parsed_text: Optional[str] = None  # Full extracted text
    skills_extracted: List[str] = Field(default_factory=list)
    experience_years: Optional[int] = None
    education: Optional[str] = None
    work_experience: Optional[str] = None  # Summary of work history
    summary: Optional[str] = None  # Resume summary/bio
    
    # Parsing metadata
    parsing_method: str = Field(default="algorithmic")  # "algorithmic" or "ai" or "hybrid"
    parsing_confidence: float = Field(default=0.0)  # 0.0 to 1.0
    ai_used: bool = Field(default=False)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "resumes"
        indexes = [
            "user_id",
            "created_at",
        ]

