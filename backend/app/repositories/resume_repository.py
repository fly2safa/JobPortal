"""
Resume repository for database operations.
"""
from typing import List, Optional
from app.models.resume import Resume
from app.core.logging import get_logger

logger = get_logger(__name__)


class ResumeRepository:
    """Repository for resume database operations."""
    
    @staticmethod
    async def create(resume_data: dict) -> Resume:
        """Create a new resume document."""
        resume = Resume(**resume_data)
        await resume.insert()
        logger.info(f"Resume created: {resume.id} for user {resume.user_id}")
        return resume
    
    @staticmethod
    async def get_by_id(resume_id: str) -> Optional[Resume]:
        """Get resume by ID."""
        return await Resume.get(resume_id)
    
    @staticmethod
    async def get_by_user(user_id: str) -> List[Resume]:
        """Get all resumes for a user."""
        return await Resume.find(Resume.user_id == user_id).sort(-Resume.created_at).to_list()
    
    @staticmethod
    async def get_latest(user_id: str) -> Optional[Resume]:
        """Get user's most recent resume."""
        resumes = await Resume.find(Resume.user_id == user_id).sort(-Resume.created_at).limit(1).to_list()
        return resumes[0] if resumes else None
    
    @staticmethod
    async def update(resume_id: str, update_data: dict) -> Optional[Resume]:
        """Update resume document."""
        resume = await Resume.get(resume_id)
        if resume:
            for key, value in update_data.items():
                setattr(resume, key, value)
            await resume.save()
            logger.info(f"Resume updated: {resume_id}")
        return resume
    
    @staticmethod
    async def delete(resume_id: str) -> bool:
        """Delete resume document."""
        resume = await Resume.get(resume_id)
        if resume:
            await resume.delete()
            logger.info(f"Resume deleted: {resume_id}")
            return True
        return False

