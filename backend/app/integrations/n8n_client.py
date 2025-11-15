"""
n8n workflow automation client for JobPortal.

This module provides integration with n8n for workflow automation including:
- Job recommendation workflows
- Candidate matching workflows
- Email notification workflows
- Resume parsing workflows
"""
from typing import Dict, Any, Optional, List
import httpx
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class N8nClient:
    """
    Client for interacting with n8n workflow automation platform.
    
    n8n is used to orchestrate complex AI workflows and automate
    repetitive tasks across the JobPortal platform.
    """
    
    def __init__(self):
        """Initialize n8n client with configuration from settings."""
        self.base_url = getattr(settings, 'N8N_BASE_URL', 'http://localhost:5678')
        self.api_key = getattr(settings, 'N8N_API_KEY', None)
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            logger.warning("n8n integration is disabled (no API key configured)")
        else:
            logger.info(f"n8n integration enabled: {self.base_url}")
    
    async def trigger_workflow(
        self,
        workflow_id: str,
        data: Dict[str, Any],
        wait_for_completion: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger an n8n workflow execution.
        
        Args:
            workflow_id: The n8n workflow ID or name
            data: Input data for the workflow
            wait_for_completion: Whether to wait for workflow to complete
            
        Returns:
            Workflow execution result if wait_for_completion=True, else execution ID
        """
        if not self.enabled:
            logger.warning(f"n8n workflow '{workflow_id}' not triggered (integration disabled)")
            return None
        
        try:
            url = f"{self.base_url}/webhook/{workflow_id}"
            headers = {
                "Content-Type": "application/json",
            }
            
            if self.api_key:
                headers["X-N8N-API-KEY"] = self.api_key
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=data, headers=headers)
                response.raise_for_status()
                
                result = response.json()
                logger.info(f"n8n workflow '{workflow_id}' triggered successfully")
                
                return result
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to trigger n8n workflow '{workflow_id}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error triggering n8n workflow '{workflow_id}': {e}")
            return None
    
    async def trigger_job_recommendation_workflow(
        self,
        user_id: str,
        user_profile: Dict[str, Any],
        job_ids: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger job recommendation workflow in n8n.
        
        This workflow analyzes user profiles and generates personalized
        job recommendations using AI.
        
        Args:
            user_id: User ID
            user_profile: User profile data
            job_ids: List of job IDs to analyze
            
        Returns:
            Workflow result with recommendations
        """
        workflow_id = getattr(settings, 'N8N_JOB_RECOMMENDATION_WORKFLOW_ID', 'job-recommendation')
        
        data = {
            "user_id": user_id,
            "user_profile": user_profile,
            "job_ids": job_ids,
            "action": "generate_recommendations"
        }
        
        return await self.trigger_workflow(workflow_id, data, wait_for_completion=True)
    
    async def trigger_candidate_matching_workflow(
        self,
        job_id: str,
        job_requirements: Dict[str, Any],
        candidate_ids: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger candidate matching workflow in n8n.
        
        This workflow analyzes candidate profiles against job requirements
        and ranks them using AI.
        
        Args:
            job_id: Job ID
            job_requirements: Job requirements and description
            candidate_ids: List of candidate user IDs to analyze
            
        Returns:
            Workflow result with ranked candidates
        """
        workflow_id = getattr(settings, 'N8N_CANDIDATE_MATCHING_WORKFLOW_ID', 'candidate-matching')
        
        data = {
            "job_id": job_id,
            "job_requirements": job_requirements,
            "candidate_ids": candidate_ids,
            "action": "rank_candidates"
        }
        
        return await self.trigger_workflow(workflow_id, data, wait_for_completion=True)
    
    async def trigger_resume_parsing_workflow(
        self,
        resume_id: str,
        file_url: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger resume parsing workflow in n8n.
        
        This workflow extracts structured data from resumes using AI.
        
        Args:
            resume_id: Resume ID
            file_url: URL to the resume file
            user_id: User ID who uploaded the resume
            
        Returns:
            Workflow result with parsed resume data
        """
        workflow_id = getattr(settings, 'N8N_RESUME_PARSING_WORKFLOW_ID', 'resume-parsing')
        
        data = {
            "resume_id": resume_id,
            "file_url": file_url,
            "user_id": user_id,
            "action": "parse_resume"
        }
        
        return await self.trigger_workflow(workflow_id, data, wait_for_completion=True)
    
    async def trigger_email_notification_workflow(
        self,
        notification_type: str,
        recipient_email: str,
        template_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger email notification workflow in n8n.
        
        This workflow sends templated emails for various events.
        
        Args:
            notification_type: Type of notification (application_submitted, interview_scheduled, etc.)
            recipient_email: Email address of recipient
            template_data: Data for email template
            
        Returns:
            Workflow result with email send status
        """
        workflow_id = getattr(settings, 'N8N_EMAIL_NOTIFICATION_WORKFLOW_ID', 'email-notification')
        
        data = {
            "notification_type": notification_type,
            "recipient_email": recipient_email,
            "template_data": template_data,
            "action": "send_email"
        }
        
        return await self.trigger_workflow(workflow_id, data, wait_for_completion=False)
    
    async def get_workflow_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a workflow execution.
        
        Args:
            execution_id: Workflow execution ID
            
        Returns:
            Execution status and result
        """
        if not self.enabled:
            return None
        
        try:
            url = f"{self.base_url}/api/v1/executions/{execution_id}"
            headers = {}
            
            if self.api_key:
                headers["X-N8N-API-KEY"] = self.api_key
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"Failed to get workflow status for '{execution_id}': {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting workflow status: {e}")
            return None
    
    def is_enabled(self) -> bool:
        """Check if n8n integration is enabled."""
        return self.enabled


# Global n8n client instance
_n8n_client: Optional[N8nClient] = None


def get_n8n_client() -> N8nClient:
    """
    Get the global n8n client instance.
    
    Returns:
        N8nClient instance
    """
    global _n8n_client
    if _n8n_client is None:
        _n8n_client = N8nClient()
    return _n8n_client


