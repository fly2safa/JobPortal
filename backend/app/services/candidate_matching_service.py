"""
AI-powered candidate matching service for employers.
Provides intelligent candidate rankings for job postings using vector search and LangChain.
"""
from typing import List, Dict, Any, Optional
from beanie import PydanticObjectId
from app.models.job import Job
from app.models.user import User
from app.models.application import Application
from app.ai.chains.candidate_matching_chain import candidate_matching_chain
from app.ai.rag.vectorstore import user_vectorstore
from app.core.logging import get_logger
from langchain.schema import Document

logger = get_logger(__name__)


class CandidateMatchingService:
    """
    Service for generating AI-powered candidate rankings for employers.
    Combines vector similarity search with LangChain-based analysis.
    """
    
    async def get_recommended_candidates(
        self,
        job_id: str,
        limit: int = 10,
        use_ai: bool = True,
        include_applicants_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get recommended candidates for a job posting.
        
        Args:
            job_id: Job posting ID
            limit: Maximum number of recommendations
            use_ai: If True, use AI chain; otherwise use vector search only
            include_applicants_only: If True, only rank existing applicants
            
        Returns:
            List of ranked candidates with match scores
        """
        try:
            # Fetch the job
            job = await Job.get(PydanticObjectId(job_id))
            if not job:
                logger.warning(f"Job {job_id} not found")
                return []
            
            # Build job profile
            job_profile = self._build_job_profile(job)
            
            # Get candidate pool
            if include_applicants_only:
                candidates = await self._get_applicants(job_id, limit * 2)
            else:
                candidates = await self._get_candidate_pool(job_profile, limit * 2)
            
            if not candidates:
                logger.info(f"No candidates found for job {job_id}")
                return []
            
            # Use AI chain for intelligent ranking if enabled
            if use_ai:
                rankings = await candidate_matching_chain.rank_candidates(
                    job=job_profile,
                    candidates=candidates,
                    top_k=limit
                )
            else:
                # Fallback to vector similarity scores
                rankings = self._vector_based_rankings(
                    job_profile,
                    candidates,
                    limit
                )
            
            logger.info(f"Generated {len(rankings)} candidate recommendations for job {job_id}")
            return rankings
            
        except Exception as e:
            logger.error(f"Error generating candidate recommendations for job {job_id}: {e}")
            return []
    
    async def index_user(self, user: User):
        """
        Index a user profile in the vector store for candidate matching.
        
        Args:
            user: User object to index
        """
        try:
            # Only index job seekers
            if user.role != "job_seeker":
                return
            
            # Create document from user profile
            skills_text = ', '.join(getattr(user, 'skills', []))
            bio = getattr(user, 'bio', '')
            experience = getattr(user, 'experience', '')
            
            doc = Document(
                page_content=f"{user.first_name} {user.last_name}\n{bio}\nSkills: {skills_text}\nExperience: {experience}",
                metadata={
                    "user_id": str(user.id),
                    "name": f"{user.first_name} {user.last_name}",
                    "email": user.email,
                    "role": user.role,
                    "skills": getattr(user, 'skills', [])
                }
            )
            
            # Add to vector store
            user_vectorstore.add_documents([doc], ids=[str(user.id)])
            logger.info(f"Indexed user {user.id} in vector store")
            
        except Exception as e:
            logger.error(f"Error indexing user {user.id}: {e}")
    
    async def index_all_users(self):
        """Index all job seeker profiles in the vector store."""
        try:
            # Fetch all job seekers
            users = await User.find(User.role == "job_seeker").to_list()
            
            if not users:
                logger.info("No job seekers to index")
                return
            
            # Create documents
            documents = []
            ids = []
            
            for user in users:
                skills_text = ', '.join(getattr(user, 'skills', []))
                bio = getattr(user, 'bio', '')
                experience = getattr(user, 'experience', '')
                
                doc = Document(
                    page_content=f"{user.first_name} {user.last_name}\n{bio}\nSkills: {skills_text}\nExperience: {experience}",
                    metadata={
                        "user_id": str(user.id),
                        "name": f"{user.first_name} {user.last_name}",
                        "email": user.email,
                        "role": user.role,
                        "skills": getattr(user, 'skills', [])
                    }
                )
                documents.append(doc)
                ids.append(str(user.id))
            
            # Batch add to vector store
            user_vectorstore.add_documents(documents, ids=ids)
            logger.info(f"Indexed {len(users)} job seekers in vector store")
            
        except Exception as e:
            logger.error(f"Error indexing all users: {e}")
    
    def _build_job_profile(self, job: Job) -> Dict[str, Any]:
        """Build a job profile dictionary for candidate matching."""
        return {
            "id": str(job.id),
            "title": job.title,
            "company_name": job.company_name,
            "location": job.location,
            "description": job.description,
            "required_skills": job.required_skills,
            "preferred_skills": getattr(job, "preferred_skills", []),
            "employment_type": getattr(job, "employment_type", "Full-time"),
            "experience_level": getattr(job, "experience_level", ""),
            "min_experience": getattr(job, "min_experience", ""),
            "education_requirement": getattr(job, "education_requirement", ""),
            "salary_range": getattr(job, "salary_range", None)
        }
    
    async def _get_candidate_pool(
        self,
        job_profile: Dict[str, Any],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Get candidate pool using vector similarity search.
        
        Args:
            job_profile: Job profile data
            limit: Maximum number of candidates
            
        Returns:
            List of candidate profiles
        """
        try:
            # Build search query from job requirements
            required_skills = ', '.join(job_profile.get('required_skills', []))
            title = job_profile.get('title', '')
            description = job_profile.get('description', '')[:200]
            
            query = f"{title}\n{description}\nRequired Skills: {required_skills}"
            
            # Perform vector search
            similar_docs = user_vectorstore.similarity_search(
                query=query,
                k=limit,
                filter={"role": "job_seeker"}
            )
            
            # Fetch full user details
            user_ids = [doc.metadata.get("user_id") for doc in similar_docs if doc.metadata.get("user_id")]
            
            candidates = []
            for user_id in user_ids:
                try:
                    user = await User.get(PydanticObjectId(user_id))
                    if user:
                        candidates.append({
                            "id": str(user.id),
                            "name": f"{user.first_name} {user.last_name}",
                            "email": user.email,
                            "current_role": getattr(user, "current_role", "Not specified"),
                            "skills": getattr(user, "skills", []),
                            "experience": getattr(user, "experience", ""),
                            "education": getattr(user, "education", ""),
                            "bio": getattr(user, "bio", "")
                        })
                except Exception as e:
                    logger.warning(f"Error fetching user {user_id}: {e}")
                    continue
            
            return candidates
            
        except Exception as e:
            logger.error(f"Error getting candidate pool: {e}")
            return []
    
    async def _get_applicants(
        self,
        job_id: str,
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Get existing applicants for a job.
        
        Args:
            job_id: Job ID
            limit: Maximum number of applicants
            
        Returns:
            List of applicant profiles
        """
        try:
            # Fetch applications for this job
            applications = await Application.find(
                Application.job_id == PydanticObjectId(job_id)
            ).limit(limit).to_list()
            
            candidates = []
            for app in applications:
                try:
                    user = await User.get(app.user_id)
                    if user:
                        candidates.append({
                            "id": str(user.id),
                            "name": f"{user.first_name} {user.last_name}",
                            "email": user.email,
                            "current_role": getattr(user, "current_role", "Not specified"),
                            "skills": getattr(user, "skills", []),
                            "experience": getattr(user, "experience", ""),
                            "education": getattr(user, "education", ""),
                            "bio": getattr(user, "bio", ""),
                            "application_id": str(app.id),
                            "application_status": app.status
                        })
                except Exception as e:
                    logger.warning(f"Error fetching applicant {app.user_id}: {e}")
                    continue
            
            return candidates
            
        except Exception as e:
            logger.error(f"Error getting applicants for job {job_id}: {e}")
            return []
    
    def _vector_based_rankings(
        self,
        job_profile: Dict[str, Any],
        candidates: List[Dict[str, Any]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Generate rankings based on simple skill matching (fallback).
        
        Args:
            job_profile: Job profile data
            candidates: List of candidates
            limit: Maximum number of rankings
            
        Returns:
            List of rankings
        """
        job_skills = set(skill.lower() for skill in job_profile.get('required_skills', []))
        
        rankings = []
        for candidate in candidates:
            candidate_skills = set(skill.lower() for skill in candidate.get('skills', []))
            
            # Calculate skill overlap
            matched_skills = job_skills & candidate_skills
            missing_skills = job_skills - candidate_skills
            additional_skills = candidate_skills - job_skills
            
            overlap = len(matched_skills)
            total_required = len(job_skills)
            
            if total_required > 0:
                match_score = int((overlap / total_required) * 100)
            else:
                match_score = 50  # Default score if no skills specified
            
            rankings.append({
                "candidate_id": candidate.get("id"),
                "candidate_name": candidate.get("name"),
                "current_role": candidate.get("current_role", "Not specified"),
                "match_score": match_score,
                "match_reason": f"Candidate has {overlap} out of {total_required} required skills.",
                "skills_match": {
                    "matched": list(matched_skills),
                    "missing": list(missing_skills),
                    "additional": list(additional_skills)
                },
                "experience_relevance": candidate.get("experience", "Not specified"),
                "concerns": f"Missing {len(missing_skills)} required skills" if missing_skills else "None"
            })
        
        # Sort by match score
        rankings.sort(key=lambda x: x["match_score"], reverse=True)
        
        return rankings[:limit]


# Global candidate matching service instance
candidate_matching_service = CandidateMatchingService()

