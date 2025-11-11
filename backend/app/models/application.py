"""
Application model for job applications.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from beanie import Document
from pydantic import Field


class ApplicationStatus(str, Enum):
    """Application status enumeration."""
    PENDING = "pending"
    REVIEWING = "reviewing"
    SHORTLISTED = "shortlisted"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"


class Application(Document):
    """Job application document model."""
    
    # References
    job_id: str = Field(..., index=True)
    applicant_id: str = Field(..., index=True)
    
    # Denormalized fields for faster queries
    job_title: str = Field(..., index=True)
    company_id: str = Field(..., index=True)
    company_name: str = Field(..., index=True)
    applicant_name: str
    applicant_email: str
    
    # Application details
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    additional_info: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    # Status tracking
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING, index=True)
    status_history: list = Field(default_factory=list)  # Track status changes
    
    # Notes and feedback
    employer_notes: Optional[str] = None
    rejection_reason: Optional[str] = None
    
    # Metadata
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_at: Optional[datetime] = None
    
    class Settings:
        name = "applications"
        indexes = [
            "job_id",
            "applicant_id",
            "status",
            "company_id",
            "applied_at",
            ("job_id", "applicant_id"),  # Compound index for uniqueness check
        ]
    
    def update_status(self, new_status: ApplicationStatus, notes: Optional[str] = None):
        """
        Update application status and track the change.
        
        Args:
            new_status: New application status
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
        old_status = self.status
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        # Update reviewed_at if moving from pending
        if old_status == ApplicationStatus.PENDING and new_status != ApplicationStatus.PENDING:
            self.reviewed_at = datetime.utcnow()
    
    def withdraw(self):
        """Withdraw the application (applicant action)."""
        if self.status not in [ApplicationStatus.REJECTED, ApplicationStatus.ACCEPTED]:
            self.update_status(ApplicationStatus.WITHDRAWN, "Withdrawn by applicant")
    
    def dict(self, **kwargs):
        """Override dict to include custom serialization."""
        d = super().dict(**kwargs)
        return d

