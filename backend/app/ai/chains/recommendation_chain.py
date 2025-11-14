"""
LangChain recommendation chain for AI-powered job matching.
Matches job seekers with relevant jobs based on their profile, skills, and preferences.
"""
from typing import List, Dict, Any, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class JobRecommendationChain:
    """
    LangChain-based recommendation system for matching jobs to job seekers.
    Uses GPT-4o to analyze user profiles and recommend relevant jobs.
    """
    
    def __init__(self):
        """Initialize the recommendation chain with LLM and prompt template."""
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,  # Lower temperature for more consistent recommendations
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Define prompt template for job recommendations
        self.prompt_template = PromptTemplate(
            input_variables=["user_profile", "user_skills", "user_experience", "job_listings"],
            template="""You are an AI career advisor helping job seekers find the best job matches.

User Profile:
{user_profile}

User Skills:
{user_skills}

User Experience:
{user_experience}

Available Jobs:
{job_listings}

Task: Analyze the user's profile, skills, and experience, then rank the available jobs from most to least relevant. For each recommended job, provide:
1. Job title and company
2. Match score (0-100)
3. Why it's a good match (2-3 sentences)
4. Skills alignment
5. Growth potential

Format your response as a JSON array of recommendations, ordered by match score (highest first).
Only recommend jobs with a match score of 60 or higher.

Example format:
[
  {{
    "job_id": "job123",
    "job_title": "Senior Software Engineer",
    "company": "Tech Corp",
    "match_score": 95,
    "match_reason": "Your 5 years of Python experience and expertise in FastAPI align perfectly with this role. The position offers leadership opportunities that match your career goals.",
    "skills_alignment": ["Python", "FastAPI", "MongoDB", "Docker"],
    "growth_potential": "High - Senior role with team leadership responsibilities"
  }}
]

Provide your recommendations:"""
        )
        
        # Create the LangChain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
            verbose=False
        )
        
        logger.info("Initialized JobRecommendationChain with GPT-4o")
    
    async def get_recommendations(
        self,
        user_profile: Dict[str, Any],
        available_jobs: List[Dict[str, Any]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get personalized job recommendations for a user.
        
        Args:
            user_profile: User profile data (name, bio, preferences, etc.)
            available_jobs: List of available job postings
            top_k: Number of top recommendations to return
            
        Returns:
            List of recommended jobs with match scores and reasons
        """
        try:
            # Format user data
            user_skills = ", ".join(user_profile.get("skills", []))
            user_experience = user_profile.get("experience", "Not specified")
            user_bio = user_profile.get("bio", "No bio provided")
            
            # Format job listings
            job_listings_text = self._format_jobs(available_jobs)
            
            # Run the chain
            result = await self.chain.arun(
                user_profile=user_bio,
                user_skills=user_skills,
                user_experience=user_experience,
                job_listings=job_listings_text
            )
            
            # Parse the result (expecting JSON)
            import json
            recommendations = json.loads(result)
            
            # Limit to top_k
            recommendations = recommendations[:top_k]
            
            logger.info(f"Generated {len(recommendations)} job recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating job recommendations: {e}")
            # Return fallback recommendations based on simple matching
            return self._fallback_recommendations(user_profile, available_jobs, top_k)
    
    def _format_jobs(self, jobs: List[Dict[str, Any]]) -> str:
        """Format job listings for the prompt."""
        formatted = []
        for i, job in enumerate(jobs, 1):
            job_text = f"""
Job {i}:
- ID: {job.get('id', 'N/A')}
- Title: {job.get('title', 'N/A')}
- Company: {job.get('company_name', 'N/A')}
- Location: {job.get('location', 'N/A')}
- Description: {job.get('description', 'N/A')[:200]}...
- Required Skills: {', '.join(job.get('required_skills', []))}
- Salary Range: {job.get('salary_range', 'Not specified')}
"""
            formatted.append(job_text)
        
        return "\n".join(formatted)
    
    def _fallback_recommendations(
        self,
        user_profile: Dict[str, Any],
        available_jobs: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Provide fallback recommendations using simple skill matching."""
        user_skills = set(skill.lower() for skill in user_profile.get("skills", []))
        
        scored_jobs = []
        for job in available_jobs:
            job_skills = set(skill.lower() for skill in job.get("required_skills", []))
            
            # Calculate skill overlap
            overlap = len(user_skills & job_skills)
            total_skills = len(job_skills)
            
            if total_skills > 0:
                match_score = int((overlap / total_skills) * 100)
            else:
                match_score = 0
            
            if match_score >= 30:  # Lower threshold for fallback
                scored_jobs.append({
                    "job_id": job.get("id"),
                    "job_title": job.get("title"),
                    "company": job.get("company_name"),
                    "match_score": match_score,
                    "match_reason": f"You have {overlap} matching skills out of {total_skills} required.",
                    "skills_alignment": list(user_skills & job_skills),
                    "growth_potential": "To be determined"
                })
        
        # Sort by match score
        scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)
        
        return scored_jobs[:top_k]


# Global recommendation chain instance
job_recommendation_chain = JobRecommendationChain()

