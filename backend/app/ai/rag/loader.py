"""
Document loader for RAG system.
Loads and processes documents for the knowledge base.
"""
from typing import List, Dict, Any
import os
from pathlib import Path


class Document:
    """Simple document class."""
    def __init__(self, page_content: str, metadata: Dict[str, Any] = None):
        self.page_content = page_content
        self.metadata = metadata or {}


class DocumentLoader:
    """
    Loads documents from various sources for the RAG system.
    Currently supports loading job portal documentation and FAQs.
    """
    
    def __init__(self):
        self.documents: List[Document] = []
    
    def load_job_portal_docs(self) -> List[Document]:
        """
        Load job portal documentation and FAQs.
        
        Returns:
            List of Document objects
        """
        docs = []
        
        # Job Portal Overview
        docs.append(Document(
            page_content="""
            TalentNest Job Portal Overview:
            TalentNest is a comprehensive job portal platform that connects job seekers with employers.
            The platform offers AI-powered features including resume parsing, job recommendations,
            candidate matching, and an intelligent assistant to help users navigate the platform.
            
            Key Features:
            - Job Search: Browse and search for jobs by title, location, type, and experience level
            - Resume Management: Upload and parse resumes with AI-powered extraction
            - Job Applications: Apply to jobs with cover letters and track application status
            - Employer Dashboard: Post jobs, review applications, and manage candidates
            - AI Recommendations: Get personalized job recommendations based on your profile
            - AI Assistant: Get help with job search, application tips, and career advice
            """,
            metadata={"source": "overview", "category": "general"}
        ))
        
        # Job Seeker Guide
        docs.append(Document(
            page_content="""
            Job Seeker Guide:
            
            Getting Started:
            1. Create an account by clicking "Sign Up" and selecting "Job Seeker"
            2. Complete your profile with your name, email, and basic information
            3. Upload your resume - our AI will automatically parse and extract your skills and experience
            4. Browse available jobs or use the search feature to find positions that match your skills
            
            Searching for Jobs:
            - Use the search bar to find jobs by title, keywords, or company name
            - Filter by location, job type (full-time, part-time, contract, internship)
            - Filter by experience level (entry, mid, senior, director, executive)
            - View job details including description, requirements, salary range, and benefits
            
            Applying to Jobs:
            - Click "Apply Now" on any job listing
            - Your resume will be automatically attached
            - Write a cover letter or use our AI-powered cover letter generator
            - Track your applications in the "Applications" section of your dashboard
            
            Application Status:
            - Pending: Your application has been submitted and is awaiting review
            - Reviewing: The employer is currently reviewing your application
            - Shortlisted: You've been shortlisted for an interview
            - Interview: An interview has been scheduled
            - Rejected: Unfortunately, your application was not selected
            - Accepted: Congratulations! You've been offered the position
            """,
            metadata={"source": "job_seeker_guide", "category": "job_seeker"}
        ))
        
        # Employer Guide
        docs.append(Document(
            page_content="""
            Employer Guide:
            
            Getting Started:
            1. Create an account by clicking "Sign Up" and selecting "Employer"
            2. Complete your company profile with company name and details
            3. Start posting job openings
            
            Posting Jobs:
            - Navigate to "Post a Job" from your employer dashboard
            - Fill in job details: title, description, requirements, location
            - Specify job type, experience level, and salary range
            - Add required skills and benefits
            - Set job status (active, inactive, draft, closed)
            
            Managing Applications:
            - View all applications for each job posting
            - Filter applications by status (pending, reviewing, shortlisted, rejected)
            - Review candidate profiles, resumes, and cover letters
            - Shortlist promising candidates
            - Reject applications with optional feedback
            - Schedule interviews with shortlisted candidates
            
            Application Review Workflow:
            1. New applications appear with "Pending" status
            2. Click "Start Review" to change status to "Reviewing"
            3. Review the candidate's resume and cover letter
            4. Click "Shortlist" to move promising candidates forward
            5. Click "Reject" to decline candidates (with optional reason)
            6. Schedule interviews with shortlisted candidates
            """,
            metadata={"source": "employer_guide", "category": "employer"}
        ))
        
        # AI Features
        docs.append(Document(
            page_content="""
            AI-Powered Features:
            
            Resume Parsing:
            - Upload your resume in PDF or DOCX format
            - Our AI automatically extracts: name, email, phone, skills, education, work experience
            - Parsed information is used to create your profile and match you with relevant jobs
            
            Job Recommendations:
            - Based on your skills, experience, and preferences
            - Updated regularly as new jobs are posted
            - View recommendations on your dashboard
            
            Candidate Matching (for Employers):
            - AI ranks candidates based on job requirements
            - Match score shows how well a candidate fits the position
            - Consider skills, experience level, and qualifications
            
            Cover Letter Generator:
            - Available when applying to jobs
            - AI generates a personalized cover letter based on:
              * Your resume and profile
              * The job description and requirements
              * Your relevant skills and experience
            - Edit and customize the generated cover letter before submitting
            
            AI Assistant:
            - Ask questions about using the platform
            - Get career advice and job search tips
            - Learn about application best practices
            - Get help with resume writing and interview preparation
            """,
            metadata={"source": "ai_features", "category": "features"}
        ))
        
        # FAQs
        docs.append(Document(
            page_content="""
            Frequently Asked Questions:
            
            Q: How do I reset my password?
            A: Click "Forgot Password" on the login page and follow the email instructions.
            
            Q: Can I apply to multiple jobs at once?
            A: Yes, you can apply to as many jobs as you like. Each application is tracked separately.
            
            Q: How long does it take for employers to review applications?
            A: Review times vary by employer. You'll be notified of any status changes via email.
            
            Q: Can I edit my application after submitting?
            A: No, applications cannot be edited after submission. However, you can withdraw and reapply.
            
            Q: What file formats are supported for resumes?
            A: We support PDF and DOCX formats. Maximum file size is 10MB.
            
            Q: How does the AI cover letter generator work?
            A: It analyzes the job description and your profile to create a personalized cover letter
            highlighting your relevant skills and experience.
            
            Q: Can I save jobs to apply later?
            A: Yes, click the bookmark icon on any job listing to save it for later.
            
            Q: How do I contact an employer directly?
            A: For privacy reasons, direct contact is not available until after you've been shortlisted.
            
            Q: What should I include in my cover letter?
            A: Introduce yourself, explain why you're interested in the position, highlight relevant
            experience and skills, and express enthusiasm for the opportunity.
            
            Q: How can I improve my chances of getting hired?
            A: Keep your profile updated, upload a complete resume, write tailored cover letters,
            apply to positions that match your skills, and respond promptly to interview invitations.
            """,
            metadata={"source": "faqs", "category": "help"}
        ))
        
        self.documents = docs
        return docs
    
    def load_from_text(self, text: str, metadata: Dict[str, Any] = None) -> Document:
        """
        Load a document from raw text.
        
        Args:
            text: Document text
            metadata: Optional metadata
            
        Returns:
            Document object
        """
        return Document(page_content=text, metadata=metadata or {})

