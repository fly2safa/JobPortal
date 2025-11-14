"""
API routes for AI-powered job recommendations.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from app.models.user import User
from app.api.v1.dependencies import get_current_user
from app.services.recommendation_service import recommendation_service
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


# Response Models
class RecommendationResponse(BaseModel):
    """Single job recommendation response."""
    job_id: str
    job_title: str
    company: str
    match_score: int = Field(..., ge=0, le=100)
    match_reason: str
    skills_alignment: List[str]
    growth_potential: str


class RecommendationsListResponse(BaseModel):
    """List of job recommendations."""
    recommendations: List[RecommendationResponse]
    total: int


class SimilarJobResponse(BaseModel):
    """Similar job response."""
    job_id: str
    job_title: str
    company: str
    similarity_score: float
    location: Optional[str] = None


class SimilarJobsListResponse(BaseModel):
    """List of similar jobs."""
    similar_jobs: List[SimilarJobResponse]
    total: int


# Routes
@router.get("/", response_model=RecommendationsListResponse)
async def get_recommendations(
    limit: int = Query(10, ge=1, le=50, description="Maximum number of recommendations"),
    use_ai: bool = Query(True, description="Use AI chain for intelligent ranking"),
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized job recommendations for the current user.
    
    Uses AI-powered matching to analyze user profile, skills, and experience
    against available jobs and provide ranked recommendations with match scores.
    """
    try:
        recommendations = await recommendation_service.get_recommendations_for_user(
            user=current_user,
            limit=limit,
            use_ai=use_ai
        )
        
        return RecommendationsListResponse(
            recommendations=recommendations,
            total=len(recommendations)
        )
        
    except Exception as e:
        logger.error(f"Error getting recommendations for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate recommendations. Please try again later."
        )


@router.get("/similar/{job_id}", response_model=SimilarJobsListResponse)
async def get_similar_jobs(
    job_id: str,
    limit: int = Query(5, ge=1, le=20, description="Maximum number of similar jobs"),
    current_user: User = Depends(get_current_user)
):
    """
    Get jobs similar to a specific job.
    
    Uses vector similarity search to find jobs with similar titles,
    descriptions, and required skills.
    """
    try:
        similar_jobs = await recommendation_service.get_similar_jobs(
            job_id=job_id,
            limit=limit
        )
        
        return SimilarJobsListResponse(
            similar_jobs=similar_jobs,
            total=len(similar_jobs)
        )
        
    except Exception as e:
        logger.error(f"Error getting similar jobs for {job_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to find similar jobs. Please try again later."
        )


@router.post("/index-jobs")
async def index_all_jobs(
    current_user: User = Depends(get_current_user)
):
    """
    Index all active jobs in the vector store for recommendations.
    
    This endpoint is typically called by admins or background jobs
    to refresh the recommendation system's job index.
    
    Note: In production, this should be restricted to admin users only.
    """
    try:
        # TODO: Add admin-only check
        # if current_user.role != "admin":
        #     raise HTTPException(status_code=403, detail="Admin access required")
        
        await recommendation_service.index_all_jobs()
        
        return {
            "message": "Successfully indexed all active jobs",
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error indexing jobs: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to index jobs. Please try again later."
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for the recommendation service.
    
    Returns the status of the recommendation system components.
    """
    try:
        from app.ai.rag.vectorstore import job_vectorstore
        
        # Check vector store
        job_count = job_vectorstore.get_collection_count()
        
        return {
            "status": "healthy",
            "indexed_jobs": job_count,
            "ai_enabled": True
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e),
            "ai_enabled": False
        }

