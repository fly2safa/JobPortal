"""
Resume management routes.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.models.user import User
from app.api.dependencies import get_current_job_seeker
from app.schemas.resume import ResumeResponse, ResumeUploadResponse
from app.services.file_service import FileService
from app.services.text_extractor import TextExtractor
from app.services.resume_parser import ResumeParser
from app.repositories.resume_repository import ResumeRepository
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/resumes", tags=["Resumes"])

# Initialize parser
parser = ResumeParser()


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_job_seeker)
):
    """
    Upload and parse a resume file.
    
    Uses hybrid approach: algorithmic parsing first, AI fallback if needed.
    
    Args:
        file: Resume file (PDF/DOCX)
        current_user: Current authenticated job seeker
        
    Returns:
        Resume data with parsed information
    """
    logger.info(f"Resume upload request from user {current_user.id}")
    
    # Validate file
    is_valid, error = FileService.validate_file(file)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    try:
        # Save file
        file_path, file_url = await FileService.save_file(file, str(current_user.id))
        
        # Extract text
        text = TextExtractor.extract_text(file_path)
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract text from file. Ensure file is not scanned or corrupted."
            )
        
        # Parse resume (hybrid approach)
        parsed_data = parser.parse_resume_text(text)
        
        # Create resume document
        resume_data = {
            "user_id": str(current_user.id),
            "file_url": file_url,
            "file_name": file.filename,
            "file_size": file.size or 0,
            "parsed_text": text,
            "skills_extracted": parsed_data.get("skills", []),
            "experience_years": parsed_data.get("experience_years"),
            "education": parsed_data.get("education"),
            "work_experience": parsed_data.get("work_experience"),
            "summary": parsed_data.get("summary"),
            "parsing_method": parsed_data.get("parsing_method", "algorithmic"),
            "parsing_confidence": parsed_data.get("parsing_confidence", 0.0),
            "ai_used": parsed_data.get("ai_used", False),
        }
        
        resume = await ResumeRepository.create(resume_data)
        
        # Optionally sync skills to user profile
        skills_synced = False
        if parsed_data.get("skills"):
            # Combine existing skills with newly extracted skills
            current_user.skills = list(set(current_user.skills + parsed_data["skills"]))
            if parsed_data.get("experience_years") and not current_user.experience_years:
                current_user.experience_years = parsed_data["experience_years"]
            if parsed_data.get("education") and not current_user.education:
                current_user.education = parsed_data["education"]
            await current_user.save()
            skills_synced = True
        
        logger.info(f"Resume uploaded and parsed: {resume.id} (method: {resume.parsing_method}, AI used: {resume.ai_used})")
        
        return ResumeUploadResponse(
            resume=ResumeResponse(
                id=str(resume.id),
                user_id=resume.user_id,
                file_url=resume.file_url,
                file_name=resume.file_name,
                file_size=resume.file_size,
                parsed_text=resume.parsed_text,
                skills_extracted=resume.skills_extracted,
                experience_years=resume.experience_years,
                education=resume.education,
                work_experience=resume.work_experience,
                summary=resume.summary,
                parsing_method=resume.parsing_method,
                parsing_confidence=resume.parsing_confidence,
                ai_used=resume.ai_used,
                created_at=resume.created_at,
                updated_at=resume.updated_at,
            ),
            message="Resume uploaded and parsed successfully",
            skills_synced=skills_synced,
        )
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process resume"
        )


@router.get("", response_model=List[ResumeResponse])
async def get_resumes(current_user: User = Depends(get_current_job_seeker)):
    """
    Get all resumes for current user.
    
    Args:
        current_user: Current authenticated job seeker
        
    Returns:
        List of user's resumes
    """
    resumes = await ResumeRepository.get_by_user(str(current_user.id))
    return [
        ResumeResponse(
            id=str(r.id),
            user_id=r.user_id,
            file_url=r.file_url,
            file_name=r.file_name,
            file_size=r.file_size,
            parsed_text=r.parsed_text,
            skills_extracted=r.skills_extracted,
            experience_years=r.experience_years,
            education=r.education,
            work_experience=r.work_experience,
            summary=r.summary,
            parsing_method=r.parsing_method,
            parsing_confidence=r.parsing_confidence,
            ai_used=r.ai_used,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in resumes
    ]


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_job_seeker)
):
    """
    Get specific resume by ID.
    
    Args:
        resume_id: Resume ID
        current_user: Current authenticated job seeker
        
    Returns:
        Resume data
    """
    resume = await ResumeRepository.get_by_id(resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    
    # Check ownership
    if resume.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resume")
    
    return ResumeResponse(
        id=str(resume.id),
        user_id=resume.user_id,
        file_url=resume.file_url,
        file_name=resume.file_name,
        file_size=resume.file_size,
        parsed_text=resume.parsed_text,
        skills_extracted=resume.skills_extracted,
        experience_years=resume.experience_years,
        education=resume.education,
        work_experience=resume.work_experience,
        summary=resume.summary,
        parsing_method=resume.parsing_method,
        parsing_confidence=resume.parsing_confidence,
        ai_used=resume.ai_used,
        created_at=resume.created_at,
        updated_at=resume.updated_at,
    )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_job_seeker)
):
    """
    Delete resume.
    
    Args:
        resume_id: Resume ID
        current_user: Current authenticated job seeker
    """
    resume = await ResumeRepository.get_by_id(resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    
    # Check ownership
    if resume.user_id != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this resume")
    
    # Delete file from storage
    file_path = resume.file_url.replace("/uploads/resumes/", "uploads/resumes/")
    await FileService.delete_file(file_path)
    
    # Delete document from database
    await ResumeRepository.delete(resume_id)
    
    logger.info(f"Resume deleted: {resume_id}")

