"""
Recommendations routes for AI-powered job and candidate matching.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from datetime import datetime
from app.models.user import User
from app.models.job import Job
from app.api.dependencies import get_current_user, get_current_employer
from app.services.recommendation_service import recommendation_service
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


# Response models
class JobRecommendationResponse(BaseModel):
    """Job recommendation with match score and reasons."""
    job: dict
    match_score: float = Field(..., ge=0.0, le=1.0, description="Match score (0-1)")
    reasons: List[str] = Field(..., description="Reasons for the recommendation")
    recommended_at: datetime


class CandidateRecommendationResponse(BaseModel):
    """Candidate recommendation with match score and reasons."""
    candidate: dict
    match_score: float = Field(..., ge=0.0, le=1.0, description="Match score (0-1)")
    reasons: List[str] = Field(..., description="Reasons for the recommendation")
    recommended_at: datetime


class RecommendationsListResponse(BaseModel):
    """List of job recommendations."""
    recommendations: List[JobRecommendationResponse]
    total: int
    user_id: str


class CandidateRecommendationsListResponse(BaseModel):
    """List of candidate recommendations."""
    recommendations: List[CandidateRecommendationResponse]
    total: int
    job_id: str


# Job Seeker Endpoints
@router.get("/jobs", response_model=List[JobRecommendationResponse])
async def get_job_recommendations(
    current_user: User = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of recommendations"),
    min_score: float = Query(0.3, ge=0.0, le=1.0, description="Minimum match score threshold")
):
    """
    Get personalized job recommendations for the current user (Job Seeker only).
    
    Uses AI to analyze the user's profile (skills, experience, preferences) and
    recommend the most relevant job postings from the database.
    
    Args:
        current_user: Current authenticated user
        limit: Maximum number of recommendations (default: 20, max: 50)
        min_score: Minimum similarity score threshold (default: 0.3)
        
    Returns:
        List of job recommendations with match scores and reasons
        
    Raises:
        HTTPException: If user is not a job seeker or service error
    """
    from app.models.user import UserRole
    
    # Verify user is a job seeker
    if current_user.role != UserRole.JOB_SEEKER:
        logger.warning(
            f"Job recommendations requested by non-job seeker: {current_user.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Job recommendations are only available for job seekers"
        )
    
    logger.info(
        f"Job recommendations requested by user {current_user.email} "
        f"(limit: {limit}, min_score: {min_score})"
    )
    
    try:
        # Get recommendations from service
        recommendations = await recommendation_service.get_job_recommendations_for_user(
            user=current_user,
            limit=limit,
            min_score=min_score
        )
        
        logger.info(
            f"Returning {len(recommendations)} job recommendations for {current_user.email}"
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error getting job recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate job recommendations"
        )


@router.post("/initialize", status_code=status.HTTP_200_OK)
async def initialize_recommendation_system(
    force_refresh: bool = Query(False, description="Force refresh the vector store"),
    current_user: User = Depends(get_current_user)
):
    """
    Initialize or refresh the recommendation system's vector store.
    
    This endpoint triggers the loading of active jobs into the vector store
    for similarity search. Typically called during system startup or when
    refreshing the recommendations database.
    
    Args:
        force_refresh: Force refresh even if already initialized
        current_user: Current authenticated user (any role)
        
    Returns:
        Status message
    """
    logger.info(
        f"Vector store initialization requested by {current_user.email} "
        f"(force_refresh: {force_refresh})"
    )
    
    try:
        await recommendation_service.initialize_vector_store(force_refresh=force_refresh)
        
        vector_store_size = recommendation_service.vector_store.size()
        
        return {
            "status": "success",
            "message": f"Recommendation system initialized with {vector_store_size} jobs",
            "vector_store_size": vector_store_size
        }
        
    except Exception as e:
        logger.error(f"Error initializing recommendation system: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to initialize recommendation system"
        )


# Employer Endpoints
@router.get("/jobs/{job_id}/candidates", response_model=List[CandidateRecommendationResponse])
async def get_candidate_recommendations_for_job(
    job_id: str,
    current_user: User = Depends(get_current_employer),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of recommendations"),
    min_score: float = Query(0.3, ge=0.0, le=1.0, description="Minimum match score threshold"),
    include_applied: bool = Query(False, description="Include candidates who already applied")
):
    """
    Get AI-powered candidate recommendations for a specific job posting (Employer only).
    
    Uses AI embeddings to analyze the job requirements and match with the most suitable
    candidates from the job seeker database. Returns candidates ranked by match score
    along with specific reasons why each candidate is a good fit.
    
    Args:
        job_id: Job posting ID
        current_user: Current authenticated employer
        limit: Maximum number of recommendations (default: 20, max: 50)
        min_score: Minimum similarity score threshold (default: 0.3)
        include_applied: Whether to include candidates who already applied (default: False)
        
    Returns:
        List of candidate recommendations with match scores and reasons
        
    Raises:
        HTTPException: If job not found, unauthorized, or service error
    """
    logger.info(
        f"Candidate recommendations requested for job {job_id} by {current_user.email}"
    )
    
    # Get the job
    job = await Job.get(job_id)
    if not job:
        logger.warning(f"Job not found: {job_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Verify user owns this job
    if job.employer_id != str(current_user.id):
        logger.warning(
            f"Unauthorized candidate recommendations access: "
            f"user {current_user.email} for job {job_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view recommendations for this job"
        )
    
    # Check if job is active
    from app.models.job import JobStatus
    if job.status != JobStatus.ACTIVE:
        logger.warning(
            f"Candidate recommendations requested for inactive job {job_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot get candidate recommendations for inactive jobs"
        )
    
    try:
        # Get recommendations from service
        recommendations = await recommendation_service.get_candidate_recommendations_for_job(
            job=job,
            limit=limit,
            min_score=min_score,
            include_applied=include_applied
        )
        
        logger.info(
            f"Returning {len(recommendations)} candidate recommendations "
            f"for job {job_id}"
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Error getting candidate recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate candidate recommendations"
        )


@router.post("/jobs/{job_id}/refresh", status_code=status.HTTP_200_OK)
async def refresh_job_in_recommendations(
    job_id: str,
    current_user: User = Depends(get_current_employer)
):
    """
    Refresh a specific job in the recommendation system (Employer only).
    
    Updates the job's embedding in the vector store. Useful after editing
    a job posting to ensure recommendations reflect the latest changes.
    
    Args:
        job_id: Job posting ID
        current_user: Current authenticated employer
        
    Returns:
        Status message
        
    Raises:
        HTTPException: If job not found or unauthorized
    """
    logger.info(f"Job refresh in vector store requested for {job_id} by {current_user.email}")
    
    # Get the job
    job = await Job.get(job_id)
    if not job:
        logger.warning(f"Job not found: {job_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Verify user owns this job
    if job.employer_id != str(current_user.id):
        logger.warning(
            f"Unauthorized job refresh: user {current_user.email} for job {job_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to refresh this job"
        )
    
    try:
        await recommendation_service.refresh_job_in_vector_store(job)
        
        return {
            "status": "success",
            "message": f"Job {job_id} refreshed in recommendation system",
            "job_id": job_id
        }
        
    except Exception as e:
        logger.error(f"Error refreshing job in recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to refresh job in recommendation system"
        )


# System Status Endpoint
@router.get("/status", status_code=status.HTTP_200_OK)
async def get_recommendation_system_status(
    current_user: User = Depends(get_current_user)
):
    """
    Get the status of the recommendation system.
    
    Provides information about the vector store, embedding service,
    and overall system health.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        System status information
    """
    logger.debug(f"Recommendation system status requested by {current_user.email}")
    
    try:
        from app.ai.rag.embeddings import embeddings_handler
        
        status_info = {
            "embeddings_available": embeddings_handler.is_available,
            "vector_store_size": recommendation_service.vector_store.size(),
            "vector_store_initialized": recommendation_service._vector_store_initialized,
            "embedding_cache_size": embeddings_handler.get_cache_size(),
            "status": "operational" if embeddings_handler.is_available else "limited"
        }
        
        return status_info
        
    except Exception as e:
        logger.error(f"Error getting recommendation system status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get recommendation system status"
        )

