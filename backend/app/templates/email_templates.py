"""
Email templates for various notifications.
"""
from typing import Dict, Any
from app.core.config import settings


def get_base_template(content: str) -> str:
    """
    Get base email template with consistent styling.
    
    Args:
        content: HTML content to insert into template
        
    Returns:
        Complete HTML email template
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{settings.APP_NAME} Notification</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; background-color: #f3f4f6;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td align="center" style="padding: 40px 0;">
                    <table role="presentation" style="width: 600px; border-collapse: collapse; background-color: #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="padding: 40px 40px 20px 40px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">{settings.APP_NAME}</h1>
                                <p style="margin: 5px 0 0 0; color: #e0e7ff; font-size: 14px;">Connecting Talent with Opportunity</p>
                            </td>
                        </tr>
                        
                        <!-- Content -->
                        <tr>
                            <td style="padding: 40px;">
                                {content}
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="padding: 30px 40px; background-color: #f9fafb; border-top: 1px solid #e5e7eb;">
                                <p style="margin: 0 0 10px 0; font-size: 14px; color: #6b7280; line-height: 1.5;">
                                    <strong>{settings.APP_NAME}</strong><br>
                                    Your trusted partner in career advancement
                                </p>
                                <p style="margin: 0; font-size: 12px; color: #9ca3af;">
                                    This is an automated message. Please do not reply to this email.<br>
                                    © 2024 {settings.APP_NAME}. All rights reserved.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def application_submitted_template(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Template for application submitted confirmation.
    
    Args:
        data: Dictionary with keys: applicant_name, job_title, company_name
        
    Returns:
        Dictionary with 'html' and 'text' content
    """
    content = f"""
    <h2 style="margin: 0 0 20px 0; color: #1f2937; font-size: 24px;">Application Submitted Successfully! ✓</h2>
    
    <p style="margin: 0 0 15px 0; color: #374151; font-size: 16px; line-height: 1.6;">
        Dear <strong>{data['applicant_name']}</strong>,
    </p>
    
    <p style="margin: 0 0 20px 0; color: #374151; font-size: 16px; line-height: 1.6;">
        Thank you for applying! Your application for the position of <strong>{data['job_title']}</strong> 
        at <strong>{data['company_name']}</strong> has been successfully submitted.
    </p>
    
    <div style="background-color: #eff6ff; border-left: 4px solid #2563eb; padding: 20px; margin: 25px 0; border-radius: 4px;">
        <p style="margin: 0 0 10px 0; color: #1e40af; font-size: 14px; font-weight: bold;">Application Details</p>
        <p style="margin: 0 0 5px 0; color: #1e3a8a; font-size: 14px;"><strong>Position:</strong> {data['job_title']}</p>
        <p style="margin: 0; color: #1e3a8a; font-size: 14px;"><strong>Company:</strong> {data['company_name']}</p>
    </div>
    
    <h3 style="margin: 25px 0 15px 0; color: #1f2937; font-size: 18px;">What happens next?</h3>
    
    <ul style="margin: 0 0 20px 0; padding-left: 20px; color: #374151; font-size: 15px; line-height: 1.8;">
        <li>Our hiring team will carefully review your application</li>
        <li>You'll receive email updates about your application status</li>
        <li>If shortlisted, we'll contact you to schedule an interview</li>
    </ul>
    
    <p style="margin: 20px 0 0 0; color: #374151; font-size: 16px; line-height: 1.6;">
        We appreciate your interest in joining our team and wish you the best of luck!
    </p>
    
    <p style="margin: 25px 0 0 0; color: #374151; font-size: 16px;">
        Best regards,<br>
        <strong>{data['company_name']} Hiring Team</strong>
    </p>
    """
    
    html = get_base_template(content)
    
    text = f"""
Application Submitted Successfully!

Dear {data['applicant_name']},

Thank you for applying! Your application for the position of {data['job_title']} at {data['company_name']} has been successfully submitted.

Application Details:
- Position: {data['job_title']}
- Company: {data['company_name']}

What happens next?
- Our hiring team will carefully review your application
- You'll receive email updates about your application status
- If shortlisted, we'll contact you to schedule an interview

We appreciate your interest in joining our team and wish you the best of luck!

Best regards,
{data['company_name']} Hiring Team

---
This is an automated message from {settings.APP_NAME}. Please do not reply to this email.
© 2024 {settings.APP_NAME}. All rights reserved.
    """
    
    return {"html": html, "text": text}


def application_status_update_template(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Template for application status update.
    
    Args:
        data: Dictionary with keys: applicant_name, job_title, company_name, new_status
        
    Returns:
        Dictionary with 'html' and 'text' content
    """
    status_colors = {
        "reviewing": "#f59e0b",
        "shortlisted": "#10b981",
        "interview": "#8b5cf6",
        "rejected": "#ef4444",
        "accepted": "#22c55e"
    }
    
    status_icons = {
        "reviewing": "🔍",
        "shortlisted": "⭐",
        "interview": "📅",
        "rejected": "❌",
        "accepted": "✅"
    }
    
    status = data['new_status'].lower()
    color = status_colors.get(status, "#6b7280")
    icon = status_icons.get(status, "📧")
    
    status_messages = {
        "reviewing": "Your application is currently under review by our hiring team.",
        "shortlisted": "Congratulations! Your application has been shortlisted for further consideration.",
        "interview": "Great news! We'd like to invite you for an interview.",
        "rejected": "After careful consideration, we have decided to move forward with other candidates at this time.",
        "accepted": "Congratulations! We are pleased to offer you the position."
    }
    
    status_message = status_messages.get(status, f"Your application status has been updated to {data['new_status']}.")
    
    content = f"""
    <h2 style="margin: 0 0 20px 0; color: #1f2937; font-size: 24px;">Application Status Update {icon}</h2>
    
    <p style="margin: 0 0 15px 0; color: #374151; font-size: 16px; line-height: 1.6;">
        Dear <strong>{data['applicant_name']}</strong>,
    </p>
    
    <p style="margin: 0 0 20px 0; color: #374151; font-size: 16px; line-height: 1.6;">
        We wanted to update you on your application for <strong>{data['job_title']}</strong> at <strong>{data['company_name']}</strong>.
    </p>
    
    <div style="background-color: #f9fafb; border: 2px solid {color}; padding: 25px; margin: 25px 0; border-radius: 8px; text-align: center;">
        <p style="margin: 0 0 10px 0; color: #6b7280; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">Current Status</p>
        <p style="margin: 0; color: {color}; font-size: 28px; font-weight: bold;">{data['new_status'].title()}</p>
    </div>
    
    <p style="margin: 0 0 20px 0; color: #374151; font-size: 16px; line-height: 1.6;">
        {status_message}
    </p>
    
    <div style="background-color: #eff6ff; padding: 20px; margin: 25px 0; border-radius: 4px;">
        <p style="margin: 0 0 5px 0; color: #1e3a8a; font-size: 14px;"><strong>Position:</strong> {data['job_title']}</p>
        <p style="margin: 0; color: #1e3a8a; font-size: 14px;"><strong>Company:</strong> {data['company_name']}</p>
    </div>
    
    <p style="margin: 25px 0 0 0; color: #374151; font-size: 16px;">
        Thank you for your continued interest in our company.
    </p>
    
    <p style="margin: 25px 0 0 0; color: #374151; font-size: 16px;">
        Best regards,<br>
        <strong>{data['company_name']} Hiring Team</strong>
    </p>
    """
    
    html = get_base_template(content)
    
    text = f"""
Application Status Update {icon}

Dear {data['applicant_name']},

We wanted to update you on your application for {data['job_title']} at {data['company_name']}.

Current Status: {data['new_status'].title()}

{status_message}

Position: {data['job_title']}
Company: {data['company_name']}

Thank you for your continued interest in our company.

Best regards,
{data['company_name']} Hiring Team

---
This is an automated message from {settings.APP_NAME}. Please do not reply to this email.
© 2024 {settings.APP_NAME}. All rights reserved.
    """
    
    return {"html": html, "text": text}


def job_alert_template(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Template for job alert/recommendation.
    
    Args:
        data: Dictionary with keys: user_name, job_title, company_name, job_location, job_id, job_url
        
    Returns:
        Dictionary with 'html' and 'text' content
    """
    job_url = data.get('job_url', f"http://localhost:3000/jobs/{data['job_id']}")
    
    content = f"""
    <h2 style="margin: 0 0 20px 0; color: #1f2937; font-size: 24px;">New Job Match Found! 🎯</h2>
    
    <p style="margin: 0 0 15px 0; color: #374151; font-size: 16px; line-height: 1.6;">
        Hi <strong>{data['user_name']}</strong>,
    </p>
    
    <p style="margin: 0 0 25px 0; color: #374151; font-size: 16px; line-height: 1.6;">
        Great news! We found a new job opportunity that matches your profile and preferences:
    </p>
    
    <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 2px solid #2563eb; padding: 30px; margin: 25px 0; border-radius: 8px;">
        <h3 style="margin: 0 0 15px 0; color: #1e40af; font-size: 22px;">{data['job_title']}</h3>
        <p style="margin: 0 0 8px 0; color: #1e3a8a; font-size: 15px;">
            <strong>🏢 Company:</strong> {data['company_name']}
        </p>
        <p style="margin: 0 0 20px 0; color: #1e3a8a; font-size: 15px;">
            <strong>📍 Location:</strong> {data['job_location']}
        </p>
        <a href="{job_url}" style="display: inline-block; padding: 14px 32px; background-color: #2563eb; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px;">
            View Job Details →
        </a>
    </div>
    
    <div style="background-color: #fef3c7; border-left: 4px solid #f59e0b; padding: 20px; margin: 25px 0; border-radius: 4px;">
        <p style="margin: 0; color: #92400e; font-size: 14px; line-height: 1.6;">
            <strong>⚡ Act Fast!</strong> Don't miss this opportunity. Apply now before the position is filled.
        </p>
    </div>
    
    <p style="margin: 20px 0 0 0; color: #374151; font-size: 16px; line-height: 1.6;">
        This job was recommended based on your skills, experience, and preferences. We think you'd be a great fit!
    </p>
    
    <p style="margin: 25px 0 0 0; color: #374151; font-size: 16px;">
        Best of luck with your application!<br>
        <strong>{settings.APP_NAME} Team</strong>
    </p>
    
    <p style="margin: 30px 0 0 0; padding-top: 20px; border-top: 1px solid #e5e7eb; color: #6b7280; font-size: 13px;">
        You can manage your job alert preferences in your <a href="http://localhost:3000/dashboard/profile" style="color: #2563eb; text-decoration: none;">account settings</a>.
    </p>
    """
    
    html = get_base_template(content)
    
    text = f"""
New Job Match Found! 🎯

Hi {data['user_name']},

Great news! We found a new job opportunity that matches your profile and preferences:

{data['job_title']}
Company: {data['company_name']}
Location: {data['job_location']}

View Job Details: {job_url}

⚡ Act Fast! Don't miss this opportunity. Apply now before the position is filled.

This job was recommended based on your skills, experience, and preferences. We think you'd be a great fit!

Best of luck with your application!
{settings.APP_NAME} Team

---
You can manage your job alert preferences in your account settings.

This is an automated message from {settings.APP_NAME}. Please do not reply to this email.
© 2024 {settings.APP_NAME}. All rights reserved.
    """
    
    return {"html": html, "text": text}


def welcome_email_template(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Template for welcome email after registration.
    
    Args:
        data: Dictionary with keys: user_name, user_role
        
    Returns:
        Dictionary with 'html' and 'text' content
    """
    role_specific = {
        "job_seeker": {
            "title": "Start Your Career Journey",
            "benefits": [
                "Browse thousands of job opportunities",
                "Get AI-powered job recommendations",
                "Upload your resume and let employers find you",
                "Track your applications in one place"
            ]
        },
        "employer": {
            "title": "Find Your Next Great Hire",
            "benefits": [
                "Post unlimited job openings",
                "Access a pool of qualified candidates",
                "Get AI-powered candidate recommendations",
                "Manage applications efficiently"
            ]
        }
    }
    
    role = data.get('user_role', 'job_seeker')
    role_info = role_specific.get(role, role_specific['job_seeker'])
    
    benefits_html = "".join([
        f'<li style="margin-bottom: 10px; color: #374151; font-size: 15px;">{benefit}</li>'
        for benefit in role_info['benefits']
    ])
    
    content = f"""
    <h2 style="margin: 0 0 20px 0; color: #1f2937; font-size: 24px;">Welcome to {settings.APP_NAME}! 🎉</h2>
    
    <p style="margin: 0 0 15px 0; color: #374151; font-size: 16px; line-height: 1.6;">
        Hi <strong>{data['user_name']}</strong>,
    </p>
    
    <p style="margin: 0 0 20px 0; color: #374151; font-size: 16px; line-height: 1.6;">
        Thank you for joining {settings.APP_NAME}! We're excited to have you on board.
    </p>
    
    <h3 style="margin: 25px 0 15px 0; color: #1f2937; font-size: 20px;">{role_info['title']}</h3>
    
    <ul style="margin: 0 0 25px 0; padding-left: 20px; list-style-type: none;">
        {benefits_html}
    </ul>
    
    <div style="background-color: #eff6ff; padding: 25px; margin: 25px 0; border-radius: 8px; text-align: center;">
        <p style="margin: 0 0 15px 0; color: #1e40af; font-size: 16px;">Ready to get started?</p>
        <a href="http://localhost:3000/dashboard" style="display: inline-block; padding: 14px 32px; background-color: #2563eb; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px;">
            Go to Dashboard →
        </a>
    </div>
    
    <p style="margin: 25px 0 0 0; color: #374151; font-size: 16px;">
        If you have any questions, feel free to reach out to our support team.
    </p>
    
    <p style="margin: 25px 0 0 0; color: #374151; font-size: 16px;">
        Welcome aboard!<br>
        <strong>The {settings.APP_NAME} Team</strong>
    </p>
    """
    
    html = get_base_template(content)
    
    benefits_text = "\n".join([f"- {benefit}" for benefit in role_info['benefits']])
    
    text = f"""
Welcome to {settings.APP_NAME}! 🎉

Hi {data['user_name']},

Thank you for joining {settings.APP_NAME}! We're excited to have you on board.

{role_info['title']}

{benefits_text}

Ready to get started? Visit your dashboard: http://localhost:3000/dashboard

If you have any questions, feel free to reach out to our support team.

Welcome aboard!
The {settings.APP_NAME} Team

---
This is an automated message from {settings.APP_NAME}. Please do not reply to this email.
© 2024 {settings.APP_NAME}. All rights reserved.
    """
    
    return {"html": html, "text": text}

