"""
n8n workflow automation client for AI orchestration.
Integrates with n8n for complex AI workflows and automation.
"""
from typing import Dict, Any, Optional, List
import httpx
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class N8NClient:
    """
    Client for interacting with n8n workflow automation platform.
    Used for orchestrating complex AI workflows and automations.
    """
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize n8n client.
        
        Args:
            base_url: n8n instance URL (defaults to env variable)
            api_key: n8n API key (defaults to env variable)
        """
        self.base_url = base_url or getattr(settings, 'N8N_BASE_URL', 'http://localhost:5678')
        self.api_key = api_key or getattr(settings, 'N8N_API_KEY', None)
        self.enabled = bool(self.api_key)
        
        if not self.enabled:
            logger.warning("n8n integration is disabled - N8N_API_KEY not configured")
        else:
            logger.info(f"n8n client initialized - Base URL: {self.base_url}")
    
    async def trigger_workflow(
        self,
        workflow_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger an n8n workflow with data.
        
        Args:
            workflow_id: ID of the workflow to trigger
            data: Data to pass to the workflow
            
        Returns:
            Workflow execution result
        """
        if not self.enabled:
            logger.warning("n8n is disabled - skipping workflow trigger")
            return {"status": "skipped", "reason": "n8n not configured"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/webhook/{workflow_id}",
                    json=data,
                    headers={
                        "X-N8N-API-KEY": self.api_key
                    } if self.api_key else {},
                    timeout=30.0
                )
                
                response.raise_for_status()
                result = response.json()
                
                logger.info(f"n8n workflow {workflow_id} triggered successfully")
                return result
                
        except Exception as e:
            logger.error(f"Error triggering n8n workflow {workflow_id}: {e}")
            return {"status": "error", "error": str(e)}
    
    async def trigger_job_recommendation_workflow(
        self,
        user_id: str,
        user_profile: Dict[str, Any],
        job_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Trigger job recommendation workflow.
        
        Args:
            user_id: User ID
            user_profile: User profile data
            job_ids: List of job IDs to analyze
            
        Returns:
            Workflow result
        """
        workflow_id = getattr(settings, 'N8N_JOB_RECOMMENDATION_WORKFLOW_ID', 'job-recommendation')
        
        data = {
            "user_id": user_id,
            "user_profile": user_profile,
            "job_ids": job_ids,
            "action": "generate_recommendations"
        }
        
        return await self.trigger_workflow(workflow_id, data)
    
    async def trigger_candidate_matching_workflow(
        self,
        job_id: str,
        job_details: Dict[str, Any],
        candidate_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Trigger candidate matching workflow.
        
        Args:
            job_id: Job ID
            job_details: Job details
            candidate_ids: List of candidate IDs to analyze
            
        Returns:
            Workflow result
        """
        workflow_id = getattr(settings, 'N8N_CANDIDATE_MATCHING_WORKFLOW_ID', 'candidate-matching')
        
        data = {
            "job_id": job_id,
            "job_details": job_details,
            "candidate_ids": candidate_ids,
            "action": "rank_candidates"
        }
        
        return await self.trigger_workflow(workflow_id, data)
    
    async def trigger_resume_parsing_workflow(
        self,
        user_id: str,
        resume_file_url: str
    ) -> Dict[str, Any]:
        """
        Trigger resume parsing workflow.
        
        Args:
            user_id: User ID
            resume_file_url: URL to resume file
            
        Returns:
            Workflow result with parsed data
        """
        workflow_id = getattr(settings, 'N8N_RESUME_PARSING_WORKFLOW_ID', 'resume-parsing')
        
        data = {
            "user_id": user_id,
            "resume_file_url": resume_file_url,
            "action": "parse_resume"
        }
        
        return await self.trigger_workflow(workflow_id, data)
    
    async def trigger_email_notification_workflow(
        self,
        recipient_email: str,
        template_name: str,
        template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger email notification workflow.
        
        Args:
            recipient_email: Recipient email address
            template_name: Email template name
            template_data: Data for template rendering
            
        Returns:
            Workflow result
        """
        workflow_id = getattr(settings, 'N8N_EMAIL_NOTIFICATION_WORKFLOW_ID', 'email-notification')
        
        data = {
            "recipient_email": recipient_email,
            "template_name": template_name,
            "template_data": template_data,
            "action": "send_email"
        }
        
        return await self.trigger_workflow(workflow_id, data)
    
    async def get_workflow_status(self, execution_id: str) -> Dict[str, Any]:
        """
        Get the status of a workflow execution.
        
        Args:
            execution_id: Execution ID
            
        Returns:
            Execution status
        """
        if not self.enabled:
            return {"status": "disabled"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/executions/{execution_id}",
                    headers={
                        "X-N8N-API-KEY": self.api_key
                    } if self.api_key else {},
                    timeout=10.0
                )
                
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Error getting workflow status for {execution_id}: {e}")
            return {"status": "error", "error": str(e)}


# Global n8n client instance
n8n_client = N8NClient()

