"""
API routes for AI-powered candidate matching for employers.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from bson import ObjectId
from app.dependencies import get_current_user
from app.models.user import User
from app.models.job import Job
from app.services.candidate_matching_service import CandidateMatchingService
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/jobs/{job_id}/recommended-candidates")
async def get_recommended_candidates(
    job_id: str,
    limit: int = Query(default=10, ge=1, le=50, description="Maximum number of candidates to return"),
    current_user: User = Depends(get_current_user)
):
    """
    Get AI-recommended candidates for a specific job.
    
    This endpoint uses vector similarity search and AI scoring to rank candidates
    who have applied to the job based on their match with job requirements.
    
    **Requires**: Employer role
    
    **Returns**: List of candidates with match scores and reasons
    """
    logger.info(f"Employer {current_user.email} requesting candidate recommendations for job {job_id}")
    
    # Verify user is an employer
    if current_user.role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employers can access candidate recommendations"
        )
    
    # Validate job_id
    try:
        job_object_id = ObjectId(job_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job ID format"
        )
    
    # Get job and verify ownership
    job = await Job.get(job_object_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.employer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view candidates for your own jobs"
        )
    
    # Get candidate recommendations
    matching_service = CandidateMatchingService()
    recommendations = await matching_service.get_recommended_candidates_for_job(job, limit)
    
    if not recommendations:
        return {
            "job_id": job_id,
            "job_title": job.title,
            "total_candidates": 0,
            "candidates": []
        }
    
    # Format response
    candidates = []
    for rec in recommendations:
        candidate_data = {
            "user_id": str(rec["user"].id),
            "full_name": rec["user"].full_name,
            "email": rec["user"].email,
            "match_score": rec["match_score"],
            "reasons": rec["reasons"],
            "application_id": str(rec["application"].id),
            "application_status": rec["application"].status,
            "applied_at": rec["application"].created_at.isoformat() if rec["application"].created_at else None,
        }
        
        # Add resume info if available
        if rec["resume"]:
            candidate_data["resume"] = {
                "resume_id": str(rec["resume"].id),
                "file_url": rec["resume"].file_url,
                "skills": rec["resume"].skills_extracted or [],
                "uploaded_at": rec["resume"].created_at.isoformat() if rec["resume"].created_at else None,
            }
        
        candidates.append(candidate_data)
    
    logger.info(f"Returning {len(candidates)} candidate recommendations for job {job_id}")
    
    return {
        "job_id": job_id,
        "job_title": job.title,
        "total_candidates": len(candidates),
        "candidates": candidates
    }


@router.post("/sync-profiles")
async def sync_profiles_to_vector_store(
    current_user: User = Depends(get_current_user)
):
    """
    Sync all job seeker profiles to the vector store for semantic search.
    
    This is a one-time setup operation or can be run periodically to update the vector store.
    
    **Requires**: Employer role (or admin)
    
    **Returns**: Sync statistics
    """
    logger.info(f"User {current_user.email} requesting profile sync to vector store")
    
    # Verify user is an employer (or could add admin check)
    if current_user.role != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employers can sync profiles"
        )
    
    # Sync profiles
    matching_service = CandidateMatchingService()
    stats = await matching_service.sync_all_profiles_to_vector_store()
    
    logger.info(f"Profile sync complete: {stats}")
    
    return {
        "message": "Profile sync completed",
        "statistics": stats
    }

