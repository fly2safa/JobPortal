"""
Test Session model for storing testing tracker data.
"""
from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import Field


class TestSession(Document):
    """Test session document model."""
    
    session_id: str = Field(..., unique=True, index=True)
    tester_name: str
    browser: str
    test_date: datetime = Field(default_factory=datetime.utcnow)
    
    # Test cases and bugs
    test_cases: List[dict] = Field(default_factory=list)
    bugs: List[dict] = Field(default_factory=list)
    
    # Metadata
    is_master: bool = Field(default=False, index=True)
    mode: str = Field(default="real")  # "real" or "mockup"
    version: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "test_sessions"
        indexes = [
            "session_id",
            "tester_name",
            "test_date",
            "is_master",
            "mode",
        ]

