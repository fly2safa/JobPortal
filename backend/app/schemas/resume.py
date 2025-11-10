"""
Resume schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ResumeResponse(BaseModel):
    """Schema for resume response."""
    id: str
    user_id: str
    file_url: str
    file_name: str
    file_size: int
    parsed_text: Optional[str] = None
    skills_extracted: List[str] = []
    experience_years: Optional[int] = None
    education: Optional[str] = None
    work_experience: Optional[str] = None
    summary: Optional[str] = None
    parsing_method: str
    parsing_confidence: float
    ai_used: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ResumeUploadResponse(BaseModel):
    """Schema for resume upload response."""
    resume: ResumeResponse
    message: str
    skills_synced: bool  # Whether skills were synced to user profile

