"""
Application schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from app.models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    """Schema for creating a new application."""
    job_id: str
    cover_letter: Optional[str] = Field(None, max_length=5000)
    resume_url: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ApplicationUpdate(BaseModel):
    """Schema for updating application (applicant side)."""
    cover_letter: Optional[str] = Field(None, max_length=5000)
    resume_url: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = None


class ApplicationStatusUpdate(BaseModel):
    """Schema for updating application status (employer side)."""
    status: ApplicationStatus
    notes: Optional[str] = Field(None, max_length=1000)
    rejection_reason: Optional[str] = Field(None, max_length=500)


class ApplicationEmployerNotes(BaseModel):
    """Schema for updating employer notes."""
    employer_notes: str = Field(..., max_length=2000)


class StatusHistoryItem(BaseModel):
    """Schema for status history item."""
    status: str
    changed_to: str
    changed_at: datetime
    notes: Optional[str] = None


class ApplicationResponse(BaseModel):
    """Schema for application response."""
    id: str
    job_id: str
    applicant_id: str
    
    # Denormalized fields
    job_title: str
    company_id: str
    company_name: str
    applicant_name: str
    applicant_email: str
    
    # Application details
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    additional_info: Dict[str, Any] = Field(default_factory=dict)
    
    # Status
    status: ApplicationStatus
    status_history: List[StatusHistoryItem] = Field(default_factory=list)
    
    # Notes
    employer_notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    
    # Timestamps
    applied_at: datetime
    updated_at: datetime
    reviewed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ApplicationListResponse(BaseModel):
    """Schema for paginated application list response."""
    applications: List[ApplicationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ApplicationStats(BaseModel):
    """Schema for application statistics."""
    total: int
    pending: int
    reviewing: int
    shortlisted: int
    interview: int
    rejected: int
    accepted: int
    withdrawn: int

