"""
Recommendation service for AI-powered job and candidate matching.
Uses embeddings and similarity search to generate personalized recommendations.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models.job import Job, JobStatus
from app.models.user import User
from app.ai.rag.vectorstore import job_vector_store
from app.ai.rag.embeddings import embeddings_handler
from app.ai.chains.recommendation_chain import recommendation_chain
from app.core.logging import get_logger

logger = get_logger(__name__)


class RecommendationService:
    """
    Service for generating AI-powered job and candidate recommendations.
    """
    
    def __init__(self):
        """Initialize the recommendation service."""
        self.vector_store = job_vector_store
        self.embeddings = embeddings_handler
        self.chain = recommendation_chain
        self._vector_store_initialized = False
    
    async def initialize_vector_store(self, force_refresh: bool = False):
        """
        Initialize or refresh the job vector store with active jobs.
        
        Args:
            force_refresh: Force refresh even if already initialized
        """
        if self._vector_store_initialized and not force_refresh:
            logger.debug("Vector store already initialized")
            return
        
        try:
            logger.info("Initializing job vector store...")
            
            # Clear existing data if force refresh
            if force_refresh:
                self.vector_store.clear()
            
            # Fetch all active jobs
            active_jobs = await Job.find(Job.status == JobStatus.ACTIVE).to_list()
            
            if not active_jobs:
                logger.warning("No active jobs found to initialize vector store")
                self._vector_store_initialized = True
                return
            
            # Convert to dictionaries
            job_dicts = []
            for job in active_jobs:
                job_dict = job.dict()
                job_dict['id'] = str(job.id)
                job_dicts.append(job_dict)
            
            # Add to vector store
            added_count = await self.vector_store.add_jobs_batch(job_dicts)
            
            logger.info(
                f"Vector store initialized with {added_count}/{len(active_jobs)} jobs"
            )
            self._vector_store_initialized = True
            
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            raise
    
    async def get_job_recommendations_for_user(
        self,
        user: User,
        limit: int = 20,
        min_score: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Get personalized job recommendations for a user.
        
        Args:
            user: User model instance
            limit: Maximum number of recommendations
            min_score: Minimum similarity score threshold
            
        Returns:
            List of job recommendations with match scores and reasons
        """
        logger.info(f"Generating job recommendations for user {user.email}")
        
        # Check if embeddings are available
        if not self.embeddings.is_available:
            logger.warning("Embeddings not available, falling back to basic search")
            return await self._get_basic_recommendations(user, limit)
        
        # Initialize vector store if needed
        await self.initialize_vector_store()
        
        if self.vector_store.size() == 0:
            logger.warning("Vector store is empty, no recommendations available")
            return []
        
        try:
            # Create user profile dictionary
            user_profile = {
                'id': str(user.id),
                'skills': user.skills,
                'experience_years': user.experience_years,
                'location': user.location,
                'education': user.education,
                'bio': user.bio,
                'job_title': user.job_title,
            }
            
            # Find similar jobs
            similar_jobs = await self.vector_store.find_similar_jobs(
                user_profile=user_profile,
                k=limit * 2  # Get more than needed for filtering
            )
            
            # Filter by minimum score and format results
            recommendations = []
            for job, score in similar_jobs:
                if score < min_score:
                    continue
                
                # Generate reasons for recommendation
                reasons = await self.chain.generate_job_recommendation_reasons(
                    user_profile=user_profile,
                    job=job,
                    match_score=score
                )
                
                recommendation = {
                    'job': job,
                    'match_score': round(score, 2),
                    'reasons': reasons,
                    'recommended_at': datetime.utcnow()
                }
                
                recommendations.append(recommendation)
                
                if len(recommendations) >= limit:
                    break
            
            logger.info(
                f"Generated {len(recommendations)} recommendations for user {user.email}"
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            # Fallback to basic recommendations
            return await self._get_basic_recommendations(user, limit)
    
    async def _get_basic_recommendations(
        self,
        user: User,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Get basic job recommendations without AI (fallback).
        Matches based on skills overlap.
        
        Args:
            user: User model instance
            limit: Maximum number of recommendations
            
        Returns:
            List of basic job recommendations
        """
        logger.info(f"Using basic recommendations for user {user.email}")
        
        try:
            # Find jobs with matching skills
            user_skills = set(s.lower() for s in user.skills) if user.skills else set()
            
            # Get active jobs
            all_jobs = await Job.find(Job.status == JobStatus.ACTIVE).limit(100).to_list()
            
            # Score jobs by skill overlap
            scored_jobs = []
            for job in all_jobs:
                job_skills = set(s.lower() for s in job.skills) if job.skills else set()
                
                # Calculate overlap
                if user_skills and job_skills:
                    overlap = len(user_skills.intersection(job_skills))
                    total = len(user_skills.union(job_skills))
                    score = overlap / total if total > 0 else 0.0
                else:
                    score = 0.5  # Neutral score if no skills
                
                if score > 0.1:  # Minimum threshold
                    scored_jobs.append((job, score))
            
            # Sort by score
            scored_jobs.sort(key=lambda x: x[1], reverse=True)
            
            # Format recommendations
            recommendations = []
            for job, score in scored_jobs[:limit]:
                job_dict = job.dict()
                job_dict['id'] = str(job.id)
                
                # Generate basic reasons
                matching_skills = set(s.lower() for s in user.skills or []).intersection(
                    set(s.lower() for s in job.skills or [])
                )
                
                reasons = []
                if matching_skills:
                    skills_str = ", ".join(list(matching_skills)[:2])
                    reasons.append(f"Matching skills: {skills_str}")
                
                if job.is_remote:
                    reasons.append("Remote work available")
                
                if not reasons:
                    reasons.append("Good fit based on your profile")
                
                recommendation = {
                    'job': job_dict,
                    'match_score': round(score, 2),
                    'reasons': reasons,
                    'recommended_at': datetime.utcnow()
                }
                
                recommendations.append(recommendation)
            
            logger.info(
                f"Generated {len(recommendations)} basic recommendations for user {user.email}"
            )
            
            return recommendations
    
    async def refresh_job_in_vector_store(self, job: Job):
        """
        Refresh a single job in the vector store.
        
        Args:
            job: Job model instance
        """
        try:
            job_dict = job.dict()
            job_dict['id'] = str(job.id)
            
            if job.status == JobStatus.ACTIVE:
                # Add or update job
                await self.vector_store.add_job(job_dict)
                logger.debug(f"Refreshed job {job.id} in vector store")
            else:
                # Remove inactive job
                self.vector_store.store.remove_by_id(str(job.id))
                logger.debug(f"Removed inactive job {job.id} from vector store")
                
        except Exception as e:
            logger.error(f"Error refreshing job in vector store: {str(e)}")
    
    async def get_candidate_recommendations_for_job(
        self,
        job: Job,
        limit: int = 20,
        min_score: float = 0.3,
        include_applied: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get candidate recommendations for a job posting.
        
        Args:
            job: Job model instance
            limit: Maximum number of recommendations
            min_score: Minimum similarity score
            include_applied: Whether to include candidates who already applied
            
        Returns:
            List of candidate recommendations with match scores
        """
        logger.info(f"Generating candidate recommendations for job {job.id}")
        
        # Check if embeddings are available
        if not self.embeddings.is_available:
            logger.warning("Embeddings not available for candidate matching")
            return []
        
        try:
            # Create job embedding
            job_dict = job.dict()
            job_dict['id'] = str(job.id)
            job_embedding_text = self.embeddings.create_job_embedding_text(job_dict)
            job_embedding = await self.embeddings.create_embedding(job_embedding_text)
            
            if not job_embedding:
                logger.error("Failed to create job embedding")
                return []
            
            # Get all job seeker users
            from app.models.user import UserRole
            job_seekers = await User.find(User.role == UserRole.JOB_SEEKER).to_list()
            
            # Optionally filter out candidates who already applied
            if not include_applied:
                from app.models.application import Application
                applications = await Application.find(
                    Application.job_id == str(job.id)
                ).to_list()
                applied_user_ids = {app.applicant_id for app in applications}
                job_seekers = [
                    js for js in job_seekers 
                    if str(js.id) not in applied_user_ids
                ]
                logger.debug(
                    f"Filtered out {len(applied_user_ids)} candidates who already applied"
                )
            
            # Score candidates
            candidate_scores = []
            for candidate in job_seekers:
                # Create candidate profile
                candidate_profile = {
                    'id': str(candidate.id),
                    'name': candidate.full_name,
                    'email': candidate.email,
                    'skills': candidate.skills or [],
                    'experience_years': candidate.experience_years,
                    'location': candidate.location,
                    'education': candidate.education,
                    'bio': candidate.bio,
                    'job_title': candidate.job_title,
                    'linkedin_url': candidate.linkedin_url,
                    'portfolio_url': candidate.portfolio_url,
                }
                
                # Enhance profile with resume data if available
                from app.models.resume import Resume
                resume = await Resume.find_one(Resume.user_id == str(candidate.id))
                if resume:
                    candidate_profile['resume_text'] = resume.parsed_text
                    candidate_profile['work_experience'] = resume.work_experience
                    if resume.skills_extracted:
                        # Merge skills from resume with profile skills
                        all_skills = set(candidate_profile['skills'])
                        all_skills.update(resume.skills_extracted)
                        candidate_profile['skills'] = list(all_skills)
                
                # Create candidate embedding
                candidate_embedding = await self.embeddings.create_user_profile_embedding(
                    candidate_profile
                )
                
                if not candidate_embedding:
                    continue
                
                # Calculate similarity
                import numpy as np
                job_vec = np.array(job_embedding)
                candidate_vec = np.array(candidate_embedding)
                
                # Cosine similarity
                norm_job = np.linalg.norm(job_vec)
                norm_candidate = np.linalg.norm(candidate_vec)
                
                if norm_job > 0 and norm_candidate > 0:
                    similarity = np.dot(job_vec, candidate_vec) / (norm_job * norm_candidate)
                    score = float((similarity + 1) / 2)  # Map to [0, 1]
                    
                    if score >= min_score:
                        candidate_scores.append((candidate, score, candidate_profile))
            
            # Sort by score
            candidate_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Format recommendations
            recommendations = []
            for candidate, score, profile in candidate_scores[:limit]:
                # Generate reasons
                reasons = await self.chain.generate_job_recommendation_reasons(
                    user_profile=profile,
                    job=job_dict,
                    match_score=score
                )
                
                candidate_dict = candidate.dict()
                candidate_dict['id'] = str(candidate.id)
                
                # Get resume info if available
                from app.models.resume import Resume
                resume = await Resume.find_one(Resume.user_id == str(candidate.id))
                if resume:
                    candidate_dict['resume'] = {
                        'id': str(resume.id),
                        'file_name': resume.file_name,
                        'file_url': resume.file_url,
                        'created_at': resume.created_at
                    }
                
                recommendation = {
                    'candidate': candidate_dict,
                    'match_score': round(score, 2),
                    'reasons': reasons,
                    'recommended_at': datetime.utcnow()
                }
                
                recommendations.append(recommendation)
            
            logger.info(
                f"Generated {len(recommendations)} candidate recommendations for job {job.id}"
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating candidate recommendations: {str(e)}")
            return []


# Global recommendation service instance
recommendation_service = RecommendationService()

