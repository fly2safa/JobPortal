"""
Background tasks for sending emails asynchronously.
"""
import asyncio
from typing import List, Optional
from app.services.email_service import email_service
from app.core.logging import get_logger

logger = get_logger(__name__)


async def send_application_submitted_email_task(
    to_email: str,
    applicant_name: str,
    job_title: str,
    company_name: str
) -> bool:
    """
    Background task to send application submitted email.
    
    Args:
        to_email: Applicant's email
        applicant_name: Applicant's full name
        job_title: Job title
        company_name: Company name
        
    Returns:
        True if email sent successfully
    """
    logger.info(f"Background task: Sending application submitted email to {to_email}")
    
    try:
        result = await email_service.send_application_submitted_email(
            to_email=to_email,
            applicant_name=applicant_name,
            job_title=job_title,
            company_name=company_name
        )
        return result
    except Exception as e:
        logger.error(f"Error in send_application_submitted_email_task: {str(e)}")
        return False


async def send_application_status_update_email_task(
    to_email: str,
    applicant_name: str,
    job_title: str,
    company_name: str,
    new_status: str
) -> bool:
    """
    Background task to send application status update email.
    
    Args:
        to_email: Applicant's email
        applicant_name: Applicant's full name
        job_title: Job title
        company_name: Company name
        new_status: New application status
        
    Returns:
        True if email sent successfully
    """
    logger.info(f"Background task: Sending status update email to {to_email}")
    
    try:
        result = await email_service.send_application_status_update_email(
            to_email=to_email,
            applicant_name=applicant_name,
            job_title=job_title,
            company_name=company_name,
            new_status=new_status
        )
        return result
    except Exception as e:
        logger.error(f"Error in send_application_status_update_email_task: {str(e)}")
        return False


async def send_job_alert_email_task(
    to_email: str,
    user_name: str,
    job_title: str,
    company_name: str,
    job_location: str,
    job_id: str
) -> bool:
    """
    Background task to send job alert email.
    
    Args:
        to_email: User's email
        user_name: User's full name
        job_title: Job title
        company_name: Company name
        job_location: Job location
        job_id: Job ID for link
        
    Returns:
        True if email sent successfully
    """
    logger.info(f"Background task: Sending job alert email to {to_email}")
    
    try:
        result = await email_service.send_job_alert_email(
            to_email=to_email,
            user_name=user_name,
            job_title=job_title,
            company_name=company_name,
            job_location=job_location,
            job_id=job_id
        )
        return result
    except Exception as e:
        logger.error(f"Error in send_job_alert_email_task: {str(e)}")
        return False


async def send_bulk_job_alerts_task(
    recipients: List[dict],
    job_title: str,
    company_name: str,
    job_location: str,
    job_id: str
) -> dict:
    """
    Background task to send job alerts to multiple users.
    
    Args:
        recipients: List of dicts with 'email' and 'name' keys
        job_title: Job title
        company_name: Company name
        job_location: Job location
        job_id: Job ID for link
        
    Returns:
        Dictionary with success/failure counts
    """
    logger.info(f"Background task: Sending bulk job alerts to {len(recipients)} recipients")
    
    results = {"success": 0, "failed": 0, "failed_emails": []}
    
    # Send emails concurrently
    tasks = []
    for recipient in recipients:
        task = send_job_alert_email_task(
            to_email=recipient["email"],
            user_name=recipient["name"],
            job_title=job_title,
            company_name=company_name,
            job_location=job_location,
            job_id=job_id
        )
        tasks.append(task)
    
    # Wait for all tasks to complete
    task_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Count successes and failures
    for i, result in enumerate(task_results):
        if isinstance(result, Exception):
            results["failed"] += 1
            results["failed_emails"].append(recipients[i]["email"])
            logger.error(f"Failed to send email to {recipients[i]['email']}: {str(result)}")
        elif result:
            results["success"] += 1
        else:
            results["failed"] += 1
            results["failed_emails"].append(recipients[i]["email"])
    
    logger.info(
        f"Bulk job alerts completed: {results['success']} sent, {results['failed']} failed"
    )
    return results


def schedule_application_submitted_email(
    to_email: str,
    applicant_name: str,
    job_title: str,
    company_name: str
):
    """
    Schedule application submitted email to be sent in background.
    
    This is a synchronous wrapper that can be called from sync contexts.
    The actual email sending happens asynchronously.
    
    Args:
        to_email: Applicant's email
        applicant_name: Applicant's full name
        job_title: Job title
        company_name: Company name
    """
    # Create task in background
    asyncio.create_task(
        send_application_submitted_email_task(
            to_email, applicant_name, job_title, company_name
        )
    )
    logger.info(f"Scheduled application submitted email for {to_email}")


def schedule_application_status_update_email(
    to_email: str,
    applicant_name: str,
    job_title: str,
    company_name: str,
    new_status: str
):
    """
    Schedule application status update email to be sent in background.
    
    This is a synchronous wrapper that can be called from sync contexts.
    The actual email sending happens asynchronously.
    
    Args:
        to_email: Applicant's email
        applicant_name: Applicant's full name
        job_title: Job title
        company_name: Company name
        new_status: New application status
    """
    # Create task in background
    asyncio.create_task(
        send_application_status_update_email_task(
            to_email, applicant_name, job_title, company_name, new_status
        )
    )
    logger.info(f"Scheduled status update email for {to_email}")


def schedule_job_alert_email(
    to_email: str,
    user_name: str,
    job_title: str,
    company_name: str,
    job_location: str,
    job_id: str
):
    """
    Schedule job alert email to be sent in background.
    
    This is a synchronous wrapper that can be called from sync contexts.
    The actual email sending happens asynchronously.
    
    Args:
        to_email: User's email
        user_name: User's full name
        job_title: Job title
        company_name: Company name
        job_location: Job location
        job_id: Job ID for link
    """
    # Create task in background
    asyncio.create_task(
        send_job_alert_email_task(
            to_email, user_name, job_title, company_name, job_location, job_id
        )
    )
    logger.info(f"Scheduled job alert email for {to_email}")

