"""
Email service for sending notifications via SMTP.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class EmailService:
    """Service for sending email notifications."""
    
    def __init__(self):
        """Initialize email service with SMTP configuration."""
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL or settings.SMTP_USER
        self.from_name = settings.SMTP_FROM_NAME
    
    def _create_message(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> MIMEMultipart:
        """
        Create email message.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text email content (fallback)
            
        Returns:
            MIMEMultipart message object
        """
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{self.from_name} <{self.from_email}>"
        message["To"] = to_email
        
        # Add plain text version if provided
        if text_content:
            text_part = MIMEText(text_content, "plain")
            message.attach(text_part)
        
        # Add HTML version
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        return message
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """
        Send email via SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text email content (fallback)
            
        Returns:
            True if email sent successfully, False otherwise
        """
        # Check if SMTP is configured
        if not self.smtp_user or not self.smtp_password:
            logger.warning("SMTP not configured. Email not sent.")
            logger.info(f"Would send email to {to_email}: {subject}")
            return False
        
        try:
            logger.info(f"Sending email to {to_email}: {subject}")
            
            # Create message
            message = self._create_message(to_email, subject, html_content, text_content)
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    async def send_bulk_email(
        self,
        recipients: List[str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> dict:
        """
        Send email to multiple recipients.
        
        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text email content (fallback)
            
        Returns:
            Dictionary with success/failure counts
        """
        results = {"success": 0, "failed": 0, "failed_emails": []}
        
        for email in recipients:
            success = await self.send_email(email, subject, html_content, text_content)
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
                results["failed_emails"].append(email)
        
        logger.info(
            f"Bulk email completed: {results['success']} sent, {results['failed']} failed"
        )
        return results
    
    async def send_application_submitted_email(
        self,
        to_email: str,
        applicant_name: str,
        job_title: str,
        company_name: str
    ) -> bool:
        """
        Send email notification when job application is submitted.
        
        Args:
            to_email: Applicant's email
            applicant_name: Applicant's full name
            job_title: Job title
            company_name: Company name
            
        Returns:
            True if email sent successfully
        """
        subject = f"Application Submitted: {job_title} at {company_name}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">Application Submitted Successfully</h2>
                    <p>Dear {applicant_name},</p>
                    <p>Your application for the position of <strong>{job_title}</strong> at <strong>{company_name}</strong> has been successfully submitted.</p>
                    <p>We have received your application and our hiring team will review it shortly. You will be notified via email about the status of your application.</p>
                    <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Job Title:</strong> {job_title}</p>
                        <p style="margin: 5px 0 0 0;"><strong>Company:</strong> {company_name}</p>
                    </div>
                    <p>Thank you for your interest in joining our team!</p>
                    <p>Best regards,<br>{company_name} Hiring Team</p>
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                    <p style="font-size: 12px; color: #6b7280;">
                        This is an automated message from {settings.APP_NAME}. Please do not reply to this email.
                    </p>
                </div>
            </body>
        </html>
        """
        
        text_content = f"""
        Application Submitted Successfully
        
        Dear {applicant_name},
        
        Your application for the position of {job_title} at {company_name} has been successfully submitted.
        
        We have received your application and our hiring team will review it shortly. You will be notified via email about the status of your application.
        
        Job Title: {job_title}
        Company: {company_name}
        
        Thank you for your interest in joining our team!
        
        Best regards,
        {company_name} Hiring Team
        
        ---
        This is an automated message from {settings.APP_NAME}. Please do not reply to this email.
        """
        
        return await self.send_email(to_email, subject, html_content, text_content)
    
    async def send_application_status_update_email(
        self,
        to_email: str,
        applicant_name: str,
        job_title: str,
        company_name: str,
        new_status: str
    ) -> bool:
        """
        Send email notification when application status changes.
        
        Args:
            to_email: Applicant's email
            applicant_name: Applicant's full name
            job_title: Job title
            company_name: Company name
            new_status: New application status
            
        Returns:
            True if email sent successfully
        """
        status_messages = {
            "reviewing": "is currently under review",
            "shortlisted": "has been shortlisted",
            "interview": "has progressed to the interview stage",
            "rejected": "was not selected at this time",
            "accepted": "has been accepted"
        }
        
        status_message = status_messages.get(new_status.lower(), f"status has been updated to {new_status}")
        
        subject = f"Application Status Update: {job_title} at {company_name}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">Application Status Update</h2>
                    <p>Dear {applicant_name},</p>
                    <p>We wanted to update you on your application for the position of <strong>{job_title}</strong> at <strong>{company_name}</strong>.</p>
                    <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Status:</strong> {new_status.title()}</p>
                        <p style="margin: 5px 0 0 0;">Your application {status_message}.</p>
                    </div>
                    <p>Thank you for your continued interest in our company.</p>
                    <p>Best regards,<br>{company_name} Hiring Team</p>
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                    <p style="font-size: 12px; color: #6b7280;">
                        This is an automated message from {settings.APP_NAME}. Please do not reply to this email.
                    </p>
                </div>
            </body>
        </html>
        """
        
        text_content = f"""
        Application Status Update
        
        Dear {applicant_name},
        
        We wanted to update you on your application for the position of {job_title} at {company_name}.
        
        Status: {new_status.title()}
        Your application {status_message}.
        
        Thank you for your continued interest in our company.
        
        Best regards,
        {company_name} Hiring Team
        
        ---
        This is an automated message from {settings.APP_NAME}. Please do not reply to this email.
        """
        
        return await self.send_email(to_email, subject, html_content, text_content)
    
    async def send_job_alert_email(
        self,
        to_email: str,
        user_name: str,
        job_title: str,
        company_name: str,
        job_location: str,
        job_id: str
    ) -> bool:
        """
        Send email notification for job alerts/recommendations.
        
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
        subject = f"New Job Alert: {job_title} at {company_name}"
        
        job_url = f"http://localhost:3000/jobs/{job_id}"  # TODO: Use actual domain
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">New Job Match Found!</h2>
                    <p>Hi {user_name},</p>
                    <p>We found a new job that matches your profile and preferences:</p>
                    <div style="background-color: #f3f4f6; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #1f2937;">{job_title}</h3>
                        <p style="margin: 5px 0;"><strong>Company:</strong> {company_name}</p>
                        <p style="margin: 5px 0;"><strong>Location:</strong> {job_location}</p>
                        <a href="{job_url}" style="display: inline-block; margin-top: 15px; padding: 10px 20px; background-color: #2563eb; color: white; text-decoration: none; border-radius: 5px;">View Job Details</a>
                    </div>
                    <p>Don't miss this opportunity! Apply now before the position is filled.</p>
                    <p>Best regards,<br>{settings.APP_NAME} Team</p>
                    <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 20px 0;">
                    <p style="font-size: 12px; color: #6b7280;">
                        This is an automated message from {settings.APP_NAME}. You can manage your job alert preferences in your account settings.
                    </p>
                </div>
            </body>
        </html>
        """
        
        text_content = f"""
        New Job Match Found!
        
        Hi {user_name},
        
        We found a new job that matches your profile and preferences:
        
        {job_title}
        Company: {company_name}
        Location: {job_location}
        
        View Job Details: {job_url}
        
        Don't miss this opportunity! Apply now before the position is filled.
        
        Best regards,
        {settings.APP_NAME} Team
        
        ---
        This is an automated message from {settings.APP_NAME}. You can manage your job alert preferences in your account settings.
        """
        
        return await self.send_email(to_email, subject, html_content, text_content)


# Global email service instance
email_service = EmailService()



