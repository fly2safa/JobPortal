"""
AI-powered job recommendation service.
Provides personalized job recommendations for job seekers using vector search and LangChain.
"""
from typing import List, Dict, Any, Optional
from beanie import PydanticObjectId
from app.models.user import User
from app.models.job import Job
from app.ai.chains.recommendation_chain import job_recommendation_chain
from app.ai.rag.vectorstore import job_vectorstore
from app.core.logging import get_logger
from langchain.schema import Document

logger = get_logger(__name__)


class RecommendationService:
    """
    Service for generating AI-powered job recommendations.
    Combines vector similarity search with LangChain-based analysis.
    """
    
    async def get_recommendations_for_user(
        self,
        user: User,
        limit: int = 10,
        use_ai: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get personalized job recommendations for a user.
        
        Args:
            user: User object
            limit: Maximum number of recommendations
            use_ai: If True, use AI chain; otherwise use vector search only
            
        Returns:
            List of recommended jobs with match scores
        """
        try:
            # Build user profile
            user_profile = self._build_user_profile(user)
            
            # Get candidate jobs using vector similarity search
            candidate_jobs = await self._get_candidate_jobs(user_profile, limit * 2)
            
            if not candidate_jobs:
                logger.info(f"No candidate jobs found for user {user.id}")
                return []
            
            # Use AI chain for intelligent ranking if enabled
            if use_ai:
                recommendations = await job_recommendation_chain.get_recommendations(
                    user_profile=user_profile,
                    available_jobs=candidate_jobs,
                    top_k=limit
                )
            else:
                # Fallback to vector similarity scores
                recommendations = self._vector_based_recommendations(
                    user_profile,
                    candidate_jobs,
                    limit
                )
            
            logger.info(f"Generated {len(recommendations)} recommendations for user {user.id}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations for user {user.id}: {e}")
            return []
    
    async def get_similar_jobs(
        self,
        job_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get jobs similar to a given job.
        
        Args:
            job_id: ID of the reference job
            limit: Maximum number of similar jobs
            
        Returns:
            List of similar jobs
        """
        try:
            # Fetch the reference job
            job = await Job.get(PydanticObjectId(job_id))
            if not job:
                logger.warning(f"Job {job_id} not found")
                return []
            
            # Create search query from job details
            query = f"{job.title} {job.description} {' '.join(job.required_skills)}"
            
            # Perform vector similarity search
            similar_docs = job_vectorstore.similarity_search_with_score(
                query=query,
                k=limit + 1,  # +1 to exclude the reference job itself
                filter={"status": "active"}
            )
            
            # Filter out the reference job and format results
            similar_jobs = []
            for doc, score in similar_docs:
                doc_job_id = doc.metadata.get("job_id")
                if doc_job_id != job_id:
                    similar_jobs.append({
                        "job_id": doc_job_id,
                        "job_title": doc.metadata.get("title"),
                        "company": doc.metadata.get("company_name"),
                        "similarity_score": float(score),
                        "location": doc.metadata.get("location")
                    })
            
            return similar_jobs[:limit]
            
        except Exception as e:
            logger.error(f"Error finding similar jobs for {job_id}: {e}")
            return []
    
    async def index_job(self, job: Job):
        """
        Index a job in the vector store for recommendations.
        
        Args:
            job: Job object to index
        """
        try:
            # Create document from job
            doc = Document(
                page_content=f"{job.title}\n{job.description}\nSkills: {', '.join(job.required_skills)}",
                metadata={
                    "job_id": str(job.id),
                    "title": job.title,
                    "company_name": job.company_name or "",
                    "location": job.location or "",
                    "status": job.status,
                    "required_skills": job.required_skills
                }
            )
            
            # Add to vector store
            job_vectorstore.add_documents([doc], ids=[str(job.id)])
            logger.info(f"Indexed job {job.id} in vector store")
            
        except Exception as e:
            logger.error(f"Error indexing job {job.id}: {e}")
    
    async def index_all_jobs(self):
        """Index all active jobs in the vector store."""
        try:
            # Fetch all active jobs
            jobs = await Job.find(Job.status == "active").to_list()
            
            if not jobs:
                logger.info("No active jobs to index")
                return
            
            # Create documents
            documents = []
            ids = []
            
            for job in jobs:
                doc = Document(
                    page_content=f"{job.title}\n{job.description}\nSkills: {', '.join(job.required_skills)}",
                    metadata={
                        "job_id": str(job.id),
                        "title": job.title,
                        "company_name": job.company_name or "",
                        "location": job.location or "",
                        "status": job.status,
                        "required_skills": job.required_skills
                    }
                )
                documents.append(doc)
                ids.append(str(job.id))
            
            # Batch add to vector store
            job_vectorstore.add_documents(documents, ids=ids)
            logger.info(f"Indexed {len(jobs)} jobs in vector store")
            
        except Exception as e:
            logger.error(f"Error indexing all jobs: {e}")
    
    def _build_user_profile(self, user: User) -> Dict[str, Any]:
        """Build a user profile dictionary for recommendations."""
        return {
            "id": str(user.id),
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
            "bio": getattr(user, "bio", ""),
            "skills": getattr(user, "skills", []),
            "experience": getattr(user, "experience", ""),
            "preferences": getattr(user, "preferences", {})
        }
    
    async def _get_candidate_jobs(
        self,
        user_profile: Dict[str, Any],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Get candidate jobs using vector similarity search.
        
        Args:
            user_profile: User profile data
            limit: Maximum number of candidates
            
        Returns:
            List of candidate jobs
        """
        try:
            # Build search query from user profile
            skills = ", ".join(user_profile.get("skills", []))
            bio = user_profile.get("bio", "")
            query = f"{bio} Skills: {skills}"
            
            # Perform vector search
            similar_docs = job_vectorstore.similarity_search(
                query=query,
                k=limit,
                filter={"status": "active"}
            )
            
            # Fetch full job details
            job_ids = [doc.metadata.get("job_id") for doc in similar_docs if doc.metadata.get("job_id")]
            
            jobs = []
            for job_id in job_ids:
                try:
                    job = await Job.get(PydanticObjectId(job_id))
                    if job:
                        jobs.append({
                            "id": str(job.id),
                            "title": job.title,
                            "company_name": job.company_name,
                            "location": job.location,
                            "description": job.description,
                            "required_skills": job.required_skills,
                            "salary_range": getattr(job, "salary_range", None)
                        })
                except Exception as e:
                    logger.warning(f"Error fetching job {job_id}: {e}")
                    continue
            
            return jobs
            
        except Exception as e:
            logger.error(f"Error getting candidate jobs: {e}")
            return []
    
    def _vector_based_recommendations(
        self,
        user_profile: Dict[str, Any],
        candidate_jobs: List[Dict[str, Any]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on simple skill matching (fallback).
        
        Args:
            user_profile: User profile data
            candidate_jobs: List of candidate jobs
            limit: Maximum number of recommendations
            
        Returns:
            List of recommendations
        """
        user_skills = set(skill.lower() for skill in user_profile.get("skills", []))
        
        recommendations = []
        for job in candidate_jobs:
            job_skills = set(skill.lower() for skill in job.get("required_skills", []))
            
            # Calculate skill overlap
            overlap = len(user_skills & job_skills)
            total_skills = len(job_skills)
            
            if total_skills > 0:
                match_score = int((overlap / total_skills) * 100)
            else:
                match_score = 50  # Default score if no skills listed
            
            recommendations.append({
                "job_id": job.get("id"),
                "job_title": job.get("title"),
                "company": job.get("company_name"),
                "match_score": match_score,
                "match_reason": f"You have {overlap} matching skills out of {total_skills} required.",
                "skills_alignment": list(user_skills & job_skills),
                "growth_potential": "To be determined"
            })
        
        # Sort by match score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return recommendations[:limit]


# Global recommendation service instance
recommendation_service = RecommendationService()

