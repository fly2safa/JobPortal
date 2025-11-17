"""
Pydantic schemas for interview operations.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.interview import InterviewStatus, InterviewType


class InterviewBase(BaseModel):
    """Base interview schema."""
    scheduled_time: datetime
    duration_minutes: int = Field(default=60, ge=15, le=480)
    interview_type: InterviewType = InterviewType.VIDEO
    meeting_link: Optional[str] = None
    meeting_location: Optional[str] = None
    meeting_instructions: Optional[str] = None
    notes: Optional[str] = None


class InterviewCreate(InterviewBase):
    """Schema for creating an interview."""
    job_id: str
    application_id: str


class InterviewUpdate(BaseModel):
    """Schema for updating an interview."""
    scheduled_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(default=None, ge=15, le=480)
    interview_type: Optional[InterviewType] = None
    meeting_link: Optional[str] = None
    meeting_location: Optional[str] = None
    meeting_instructions: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[InterviewStatus] = None
    feedback: Optional[str] = None
    interviewer_notes: Optional[str] = None


class InterviewReschedule(BaseModel):
    """Schema for rescheduling an interview."""
    scheduled_time: datetime
    reason: Optional[str] = None


class InterviewCancel(BaseModel):
    """Schema for cancelling an interview."""
    reason: Optional[str] = None


class InterviewComplete(BaseModel):
    """Schema for completing an interview."""
    feedback: Optional[str] = None
    interviewer_notes: Optional[str] = None


class InterviewResponse(InterviewBase):
    """Schema for interview response."""
    id: str
    job_id: str
    application_id: str
    
    candidate_id: str
    candidate_name: str
    candidate_email: str
    
    employer_id: str
    employer_name: str
    employer_email: str
    
    company_id: str
    company_name: str
    job_title: str
    
    status: InterviewStatus
    status_history: list = []
    
    feedback: Optional[str] = None
    interviewer_notes: Optional[str] = None
    
    candidate_notified: bool = False
    employer_notified: bool = False
    reminder_sent: bool = False
    
    created_at: datetime
    updated_at: datetime
    created_by: str
    
    class Config:
        from_attributes = True


class InterviewListResponse(BaseModel):
    """Schema for list of interviews."""
    interviews: list[InterviewResponse]
    total: int
    page: int
    page_size: int

