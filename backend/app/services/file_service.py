"""
File upload and storage service.
"""
import os
import uuid
from pathlib import Path
from typing import Optional
import aiofiles
from fastapi import UploadFile
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path("uploads/resumes")
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


class FileService:
    """Service for handling file uploads and storage."""
    
    @staticmethod
    def validate_file(file: UploadFile) -> tuple[bool, Optional[str]]:
        """
        Validate uploaded file.
        
        Returns:
            (is_valid, error_message)
        """
        # Check file extension
        file_ext = Path(file.filename).suffix.lower().lstrip('.')
        if file_ext not in settings.allowed_extensions_list:
            return False, f"Invalid file type. Allowed: {', '.join(settings.allowed_extensions_list)}"
        
        # Check file size (will be checked after reading)
        return True, None
    
    @staticmethod
    async def save_file(file: UploadFile, user_id: str) -> tuple[str, str]:
        """
        Save uploaded file to storage.
        
        Returns:
            (file_path, file_url)
        """
        # Generate unique filename
        file_ext = Path(file.filename).suffix.lower()
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = UPLOADS_DIR / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            
            # Check size after reading
            if len(content) > settings.MAX_UPLOAD_SIZE:
                raise ValueError(f"File too large. Max size: {settings.MAX_UPLOAD_SIZE} bytes")
            
            await f.write(content)
        
        file_url = f"/uploads/resumes/{unique_filename}"
        logger.info(f"File saved: {file_path} for user {user_id}")
        
        return str(file_path), file_url
    
    @staticmethod
    async def delete_file(file_path: str) -> bool:
        """Delete file from storage."""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {str(e)}")
        return False

