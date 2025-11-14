"""
LangChain candidate matching chain for AI-powered candidate ranking.
Matches job postings with relevant candidates based on skills, experience, and fit.
"""
from typing import List, Dict, Any, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class CandidateMatchingChain:
    """
    LangChain-based matching system for ranking candidates for job postings.
    Uses GPT-4o to analyze job requirements and candidate profiles.
    """
    
    def __init__(self):
        """Initialize the candidate matching chain with LLM and prompt template."""
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,  # Lower temperature for more consistent rankings
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Define prompt template for candidate matching
        self.prompt_template = PromptTemplate(
            input_variables=["job_details", "job_requirements", "candidates"],
            template="""You are an AI recruitment assistant helping employers find the best candidates for their job openings.

Job Details:
{job_details}

Job Requirements:
{job_requirements}

Candidate Pool:
{candidates}

Task: Analyze each candidate's profile, skills, and experience against the job requirements, then rank them from best to least fit. For each recommended candidate, provide:
1. Candidate name and current role
2. Match score (0-100)
3. Why they're a good fit (2-3 sentences)
4. Skills match analysis
5. Experience relevance
6. Potential concerns or gaps

Format your response as a JSON array of candidate rankings, ordered by match score (highest first).
Only recommend candidates with a match score of 50 or higher.

Example format:
[
  {{
    "candidate_id": "user123",
    "candidate_name": "John Doe",
    "current_role": "Software Engineer",
    "match_score": 92,
    "match_reason": "John has 5 years of Python and FastAPI experience, directly matching your requirements. His background in building scalable APIs aligns perfectly with this role.",
    "skills_match": {{
      "matched": ["Python", "FastAPI", "MongoDB", "Docker"],
      "missing": ["Kubernetes"],
      "additional": ["AWS", "CI/CD"]
    }},
    "experience_relevance": "Highly relevant - 5 years in backend development with similar tech stack",
    "concerns": "Limited experience with Kubernetes, but has strong containerization knowledge with Docker"
  }}
]

Provide your candidate rankings:"""
        )
        
        # Create the LangChain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
            verbose=False
        )
        
        logger.info("Initialized CandidateMatchingChain with GPT-4o")
    
    async def rank_candidates(
        self,
        job: Dict[str, Any],
        candidates: List[Dict[str, Any]],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Rank candidates for a job posting.
        
        Args:
            job: Job posting data (title, description, requirements, etc.)
            candidates: List of candidate profiles
            top_k: Number of top candidates to return
            
        Returns:
            List of ranked candidates with match scores and analysis
        """
        try:
            # Format job details
            job_details_text = self._format_job(job)
            job_requirements_text = self._format_requirements(job)
            
            # Format candidates
            candidates_text = self._format_candidates(candidates)
            
            # Run the chain
            result = await self.chain.arun(
                job_details=job_details_text,
                job_requirements=job_requirements_text,
                candidates=candidates_text
            )
            
            # Parse the result (expecting JSON)
            import json
            rankings = json.loads(result)
            
            # Limit to top_k
            rankings = rankings[:top_k]
            
            logger.info(f"Ranked {len(rankings)} candidates for job {job.get('id')}")
            return rankings
            
        except Exception as e:
            logger.error(f"Error ranking candidates: {e}")
            # Return fallback rankings based on simple skill matching
            return self._fallback_rankings(job, candidates, top_k)
    
    def _format_job(self, job: Dict[str, Any]) -> str:
        """Format job details for the prompt."""
        return f"""
Title: {job.get('title', 'N/A')}
Company: {job.get('company_name', 'N/A')}
Location: {job.get('location', 'N/A')}
Description: {job.get('description', 'N/A')[:300]}...
Employment Type: {job.get('employment_type', 'Full-time')}
Experience Level: {job.get('experience_level', 'Not specified')}
"""
    
    def _format_requirements(self, job: Dict[str, Any]) -> str:
        """Format job requirements for the prompt."""
        required_skills = ', '.join(job.get('required_skills', []))
        preferred_skills = ', '.join(job.get('preferred_skills', []))
        
        return f"""
Required Skills: {required_skills or 'Not specified'}
Preferred Skills: {preferred_skills or 'Not specified'}
Minimum Experience: {job.get('min_experience', 'Not specified')}
Education: {job.get('education_requirement', 'Not specified')}
"""
    
    def _format_candidates(self, candidates: List[Dict[str, Any]]) -> str:
        """Format candidate profiles for the prompt."""
        formatted = []
        for i, candidate in enumerate(candidates, 1):
            candidate_text = f"""
Candidate {i}:
- ID: {candidate.get('id', 'N/A')}
- Name: {candidate.get('name', 'N/A')}
- Current Role: {candidate.get('current_role', 'Not specified')}
- Experience: {candidate.get('experience', 'Not specified')}
- Skills: {', '.join(candidate.get('skills', []))}
- Education: {candidate.get('education', 'Not specified')}
- Bio: {candidate.get('bio', 'No bio provided')[:150]}...
"""
            formatted.append(candidate_text)
        
        return "\n".join(formatted)
    
    def _fallback_rankings(
        self,
        job: Dict[str, Any],
        candidates: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        """Provide fallback rankings using simple skill matching."""
        job_skills = set(skill.lower() for skill in job.get('required_skills', []))
        
        ranked_candidates = []
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
            
            if match_score >= 30:  # Lower threshold for fallback
                ranked_candidates.append({
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
        ranked_candidates.sort(key=lambda x: x["match_score"], reverse=True)
        
        return ranked_candidates[:top_k]


# Global candidate matching chain instance
candidate_matching_chain = CandidateMatchingChain()

