"""
Interview model for scheduling interviews with candidates.
"""
from datetime import datetime
from typing import Optional
from enum import Enum
from beanie import Document
from pydantic import Field


class InterviewStatus(str, Enum):
    """Interview status enumeration."""
    SCHEDULED = "scheduled"
    RESCHEDULED = "rescheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class InterviewType(str, Enum):
    """Interview type enumeration."""
    PHONE = "phone"
    VIDEO = "video"
    IN_PERSON = "in_person"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    FINAL = "final"


class Interview(Document):
    """Interview document model."""
    
    # References
    job_id: str = Field(..., index=True)
    application_id: str = Field(..., index=True)
    
    # Candidate and employer info (denormalized for faster queries)
    candidate_id: str = Field(..., index=True)
    candidate_name: str
    candidate_email: str
    
    employer_id: str = Field(..., index=True)
    employer_name: str
    employer_email: str
    
    company_id: str = Field(..., index=True)
    company_name: str
    
    job_title: str
    
    # Interview details
    scheduled_time: datetime = Field(..., index=True)
    duration_minutes: int = Field(default=60)
    interview_type: InterviewType = Field(default=InterviewType.VIDEO)
    
    # Meeting details
    meeting_link: Optional[str] = None
    meeting_location: Optional[str] = None  # For in-person interviews
    meeting_instructions: Optional[str] = None
    
    # Status and tracking
    status: InterviewStatus = Field(default=InterviewStatus.SCHEDULED, index=True)
    status_history: list = Field(default_factory=list)  # Track status changes
    
    # Notes and feedback
    notes: Optional[str] = None  # Pre-interview notes
    feedback: Optional[str] = None  # Post-interview feedback
    interviewer_notes: Optional[str] = None
    
    # Notifications
    candidate_notified: bool = Field(default=False)
    employer_notified: bool = Field(default=False)
    reminder_sent: bool = Field(default=False)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str  # User ID who created the interview
    
    class Settings:
        name = "interviews"
        indexes = [
            "job_id",
            "application_id",
            "candidate_id",
            "employer_id",
            "company_id",
            "status",
            "scheduled_time",
            ("job_id", "application_id"),
            ("candidate_id", "scheduled_time"),
            ("employer_id", "scheduled_time"),
        ]
    
    def update_status(self, new_status: InterviewStatus, notes: Optional[str] = None):
        """
        Update interview status and track the change.
        
        Args:
            new_status: New interview status
            notes: Optional notes about the status change
        """
        # Add to status history
        self.status_history.append({
            "status": self.status,
            "changed_to": new_status,
            "changed_at": datetime.utcnow(),
            "notes": notes
        })
        
        # Update status
        self.status = new_status
        self.updated_at = datetime.utcnow()
    
    def reschedule(self, new_time: datetime, notes: Optional[str] = None):
        """
        Reschedule the interview.
        
        Args:
            new_time: New scheduled time
            notes: Optional notes about the reschedule
        """
        old_time = self.scheduled_time
        self.scheduled_time = new_time
        self.update_status(
            InterviewStatus.RESCHEDULED,
            notes or f"Rescheduled from {old_time} to {new_time}"
        )
        # Reset notification flags
        self.candidate_notified = False
        self.employer_notified = False
        self.reminder_sent = False
    
    def cancel(self, reason: Optional[str] = None):
        """
        Cancel the interview.
        
        Args:
            reason: Optional cancellation reason
        """
        self.update_status(InterviewStatus.CANCELLED, reason or "Interview cancelled")
    
    def complete(self, feedback: Optional[str] = None):
        """
        Mark the interview as completed.
        
        Args:
            feedback: Optional interview feedback
        """
        self.update_status(InterviewStatus.COMPLETED, "Interview completed")
        if feedback:
            self.feedback = feedback
        self.updated_at = datetime.utcnow()
    
    def dict(self, **kwargs):
        """Override dict to include custom serialization."""
        d = super().dict(**kwargs)
        return d

