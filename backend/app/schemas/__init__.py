"""
Schemas package exports.
"""
from app.schemas.auth import UserRegister, UserLogin, Token
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobListResponse,
    JobPublish,
    JobStatusUpdate
)
from app.schemas.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationListResponse,
    ApplicationStatusUpdate,
    ApplicationEmployerNotes,
    ApplicationStats,
    StatusHistoryItem
)

__all__ = [
    "UserRegister",
    "UserLogin",
    "Token",
    "UserResponse",
    "UserUpdate",
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    "JobListResponse",
    "JobPublish",
    "JobStatusUpdate",
    "ApplicationCreate",
    "ApplicationUpdate",
    "ApplicationResponse",
    "ApplicationListResponse",
    "ApplicationStatusUpdate",
    "ApplicationEmployerNotes",
    "ApplicationStats",
    "StatusHistoryItem",
]

