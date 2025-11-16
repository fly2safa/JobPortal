"""
TalentNest Testing Tracker - GUI Application
A standalone GUI tool for tracking manual testing progress.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import json
from datetime import datetime
from pathlib import Path
import requests
import os

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()
RESULTS_DIR = SCRIPT_DIR / "results"


class Bug:
    """Represents a bug report."""
    
    def __init__(self, bug_id="", test_id="", title="", severity="Medium", 
                 priority="P2", description="", steps_to_reproduce="", 
                 expected="", actual="", environment="", screenshot=""):
        self.bug_id = bug_id
        self.test_id = test_id
        self.title = title
        self.severity = severity  # Critical, High, Medium, Low
        self.priority = priority  # P0, P1, P2, P3
        self.description = description
        self.steps_to_reproduce = steps_to_reproduce
        self.expected_behavior = expected
        self.actual_behavior = actual
        self.environment = environment
        self.screenshot = screenshot
        self.reported_by = ""
        self.reported_date = ""


class TestCase:
    """Represents a single test case."""
    
    def __init__(self, id, section, title, description, steps):
        self.id = id
        self.section = section
        self.title = title
        self.description = description
        self.steps = steps
        self.status = "Not Started"  # Not Started, Pass, Fail, Blocked
        self.actual_results = ""
        self.notes = ""
        self.tested_by = ""
        self.tested_date = ""
        self.bugs = []  # List of bug IDs associated with this test


class TestingTrackerApp:
    """Main GUI application for testing tracker."""
    
    # Version number - Update this when making changes to the application
    # Format: MAJOR.MINOR.PATCH
    # - MAJOR: Breaking changes or major new features
    # - MINOR: New features, backward compatible
    # - PATCH: Bug fixes, small improvements
    # 
    # v2.1.3 - Fix file paths - save to testing_tool/results/
    #          - All results now save to testing_tool/results/ (not root/results/)
    #          - Update .gitignore to exclude test_progress_*.json and test_report_*.md
    #          - Use script-relative paths for cross-platform compatibility
    # v2.1.2 - Fix scrollbar issue - all 83 tests now accessible
    #          - Remove tree height limit to allow full scrolling
    #          - Update initial popup to mention name AND browser
    #          - Remove debug logging (confirmed all tests load correctly)
    # v2.1.1 - UI improvements and UX refinements
    #          - Split Quick Jump buttons into two rows (8 per row)
    #          - Removed premature welcome popup after entering name
    #          - Welcome message now shows only after browser selection
    #          - Added requirements.txt and comprehensive README.md
    # v2.1.0 - Added 5 documentation verification test cases (16.1-16.5)
    #          Now includes ERD, Architecture diagrams, README completeness,
    #          cross-platform instructions, and compliance documentation tests
    #          Total test cases: 83 (was 78)
    VERSION = "2.1.3"
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"TalentNest Testing Tracker v{self.VERSION}")
        # Start at a baseline of 1024x768 (common minimum for general users),
        # then maximize the window so all controls are visible on larger displays.
        self.root.geometry("1024x768")
        try:
            # On Windows and most platforms this will open the window maximized
            self.root.state("zoomed")
        except Exception:
            # Fallback for environments that don't support 'zoomed'
            try:
                self.root.attributes("-zoomed", True)
            except Exception:
                pass
        
        # Set minimum window size aligned with baseline resolution
        self.root.minsize(1024, 768)
        
        # Configure colors and theme
        self.colors = {
            'primary': '#2563eb',      # Blue
            'success': '#10b981',      # Green
            'danger': '#ef4444',       # Red
            'warning': '#f59e0b',      # Orange
            'info': '#06b6d4',         # Cyan
            'dark': '#1f2937',         # Dark gray
            'light': '#f3f4f6',        # Light gray
            'white': '#ffffff',
            'border': '#d1d5db'
        }
        
        # Configure style
        self.setup_styles()
        
        # API configuration for database integration
        self.api_base_url = "http://localhost:8000/api/v1"
        self.mode = "real"  # "real" or "mockup"
        
        # Test data
        self.test_cases = self.load_test_cases()
        self.current_test = None
        self.tester_name = ""
        self.tester_info = {}
        self.bugs = []  # List of all bugs
        self.bug_counter = 1  # Auto-increment bug ID
        self._programmatic_selection = False  # Flag to prevent event loops
        self.has_unsaved_changes = False  # Track if there are unsaved changes
        self.loaded_filename = None  # Track which file was loaded
        
        # Setup UI
        self.setup_ui()
        self.load_tester_info()
        
        # Update progress to show total test count on startup
        self.update_progress()
        
        # Setup window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Disable testing until name is entered
        self.testing_enabled = False
        self.browser_prompt_shown = False  # Track if browser prompt was shown
        
        # Schedule the name check after UI is fully loaded
        self.root.after(100, self.check_tester_name)
    
    def setup_styles(self):
        """Configure ttk styles for modern look."""
        style = ttk.Style()
        
        # Configure Treeview
        style.configure("Treeview",
                       background=self.colors['white'],
                       foreground=self.colors['dark'],
                       rowheight=28,
                       fieldbackground=self.colors['white'],
                       borderwidth=0)
        style.map('Treeview', background=[('selected', self.colors['primary'])])
        
        # Configure Treeview headings
        style.configure("Treeview.Heading",
                       background=self.colors['light'],
                       foreground=self.colors['dark'],
                       relief="flat",
                       font=('Arial', 10, 'bold'))
        style.map("Treeview.Heading",
                 background=[('active', self.colors['border'])])
        
        # Configure buttons
        style.configure("Primary.TButton",
                       font=('Arial', 10, 'bold'),
                       padding=8)
        
        style.configure("Success.TButton",
                       font=('Arial', 10),
                       padding=6)
        
        style.configure("Danger.TButton",
                       font=('Arial', 10),
                       padding=6)
        
        # Configure LabelFrame
        style.configure("TLabelframe",
                       background=self.colors['white'],
                       borderwidth=1,
                       relief="solid")
        style.configure("TLabelframe.Label",
                       font=('Arial', 11, 'bold'),
                       foreground=self.colors['dark'])
        
        # Configure Progress bar
        style.configure("TProgressbar",
                       thickness=20,
                       troughcolor=self.colors['light'],
                       background=self.colors['success'])
        
    def load_test_cases(self):
        """Load all test cases based on current implementation status (100% Complete)."""
        test_cases = []
        
        # Authentication & Authorization (Phase 1 - Complete)
        test_cases.extend([
            TestCase("1.1", "Authentication", "User Registration (Job Seeker)",
                    "Verify job seeker can register successfully with password visibility toggle",
                    ["Navigate to signup", "Select Job Seeker role", "Fill form with password toggle", "Submit"]),
            TestCase("1.2", "Authentication", "User Registration (Employer)",
                    "Verify employer can register successfully with password visibility toggle",
                    ["Navigate to signup", "Select Employer role", "Fill form with password toggle", "Submit"]),
            TestCase("1.3", "Authentication", "User Login",
                    "Verify users can log in with valid credentials and password visibility toggle",
                    ["Navigate to login", "Enter credentials", "Toggle password visibility", "Click login"]),
            TestCase("1.4", "Authentication", "Login with Invalid Credentials",
                    "Verify proper error handling for invalid login",
                    ["Navigate to login", "Enter invalid credentials", "Click login", "Verify error"]),
            TestCase("1.5", "Authentication", "Rate Limiting on Auth Endpoints",
                    "Verify rate limiting works correctly on registration/login",
                    ["Attempt multiple rapid logins", "Verify rate limit error", "Wait and retry"]),
            TestCase("1.6", "Authentication", "Logout",
                    "Verify users can log out successfully",
                    ["Log in", "Click logout", "Verify redirect"]),
            TestCase("1.7", "Authentication", "Protected Routes",
                    "Verify unauthorized users cannot access protected routes",
                    ["Log out", "Try to access protected URLs", "Verify redirect"]),
        ])
        
        # Job Seeker Features (Phase 2 - Complete)
        test_cases.extend([
            TestCase("2.1", "Job Seeker", "Browse Jobs (Unauthenticated)",
                    "Verify anyone can browse job listings",
                    ["Navigate to jobs page", "View job listings"]),
            TestCase("2.2", "Job Seeker", "Job Search and Filters",
                    "Verify job search and filtering functionality",
                    ["Search by keyword", "Filter by location", "Filter by type", "Filter by skills"]),
            TestCase("2.3", "Job Seeker", "View Job Details",
                    "Verify job detail page displays all information",
                    ["Click on job listing", "Review all details (title, company, location, salary, skills)"]),
            TestCase("2.4", "Job Seeker", "Apply for a Job",
                    "Verify job seeker can apply for a job with cover letter generation",
                    ["Log in", "Navigate to job", "Click Apply", "Generate cover letter", "Fill form", "Submit"]),
            TestCase("2.5", "Job Seeker", "Upload Resume with AI Parsing",
                    "Verify resume upload and AI parsing functionality",
                    ["Log in", "Navigate to profile", "Upload resume (PDF/DOCX)", "Wait for AI parsing", "Review extracted skills"]),
            TestCase("2.6", "Job Seeker", "View My Applications",
                    "Verify job seeker can view their application history with status",
                    ["Log in", "Navigate to My Applications", "Review list with status badges"]),
            TestCase("2.7", "Job Seeker", "Update Profile",
                    "Verify job seeker can update their profile",
                    ["Log in", "Navigate to profile", "Update fields (skills, experience, education)", "Save"]),
            TestCase("2.8", "Job Seeker", "View Application Status Updates",
                    "Verify job seeker receives email notifications for status changes",
                    ["Apply to job", "Employer updates status", "Check email", "Verify status in dashboard"]),
        ])
        
        # Employer Features (Phase 2 - Complete)
        test_cases.extend([
            TestCase("3.1", "Employer", "View Employer Dashboard",
                    "Verify employer dashboard displays relevant information with clear 'Employer Dashboard' label",
                    ["Log in as employer", "View dashboard metrics", "Verify 'Employer Dashboard' label with Home icon"]),
            TestCase("3.2", "Employer", "Create Job Posting",
                    "Verify employer can create a new job posting",
                    ["Log in", "Navigate to Post Job", "Fill form (title, description, skills, location, salary)", "Publish"]),
            TestCase("3.3", "Employer", "Edit Job Posting",
                    "Verify employer can edit existing job postings",
                    ["Log in", "Navigate to My Jobs", "Click Edit", "Modify fields", "Save"]),
            TestCase("3.4", "Employer", "Close/Archive Job Posting",
                    "Verify employer can close or archive job postings",
                    ["Log in", "Navigate to My Jobs", "Click Close", "Confirm"]),
            TestCase("3.5", "Employer", "View Applications for a Job",
                    "Verify employer can view all applications for a specific job",
                    ["Log in", "Navigate to job", "Click View Applications", "Review application list"]),
            TestCase("3.6", "Employer", "Review Application Details",
                    "Verify employer can view detailed application information",
                    ["Log in", "Navigate to applications", "Click on application", "Review candidate details and resume"]),
            TestCase("3.7", "Employer", "Shortlist Candidate",
                    "Verify employer can shortlist candidates",
                    ["Log in", "Navigate to application", "Click Shortlist", "Verify status update"]),
            TestCase("3.8", "Employer", "Reject Candidate",
                    "Verify employer can reject candidates with reason",
                    ["Log in", "Navigate to application", "Click Reject", "Enter reason", "Submit"]),
            TestCase("3.9", "Employer", "Add Employer Notes",
                    "Verify employer can add private notes to applications",
                    ["Log in", "Navigate to application", "Add note", "Save"]),
            TestCase("3.10", "Employer", "Update Company Profile",
                    "Verify employer can update company information",
                    ["Log in", "Navigate to company profile", "Update fields", "Save"]),
        ])
        
        # AI Features (Phase 3 - Complete)
        test_cases.extend([
            TestCase("4.1", "AI Features", "AI Resume Parsing",
                    "Verify AI can parse uploaded resumes and extract skills",
                    ["Log in", "Upload resume", "Wait for AI parsing", "Review extracted data (skills, experience, education)"]),
            TestCase("4.2", "AI Features", "AI Assistant Chat (RAG-based)",
                    "Verify AI assistant provides helpful responses using RAG",
                    ["Log in", "Navigate to AI Assistant", "Ask questions about jobs", "Review contextual responses"]),
            TestCase("4.3", "AI Features", "AI Cover Letter Generation",
                    "Verify AI can generate personalized cover letters",
                    ["Log in", "Apply to job", "Click Generate Cover Letter", "Review generated content", "Edit if needed"]),
            TestCase("4.4", "AI Features", "AI Job Recommendations (Vector Search)",
                    "Verify AI recommends relevant jobs using ChromaDB vector similarity + AI scoring",
                    ["Log in as job seeker", "Navigate to Recommendations", "Review match scores (0-100%)", "Review match reasons", "Verify color coding"]),
            TestCase("4.5", "AI Features", "AI Candidate Matching (Vector Search)",
                    "Verify AI ranks candidates using ChromaDB vector similarity + AI scoring",
                    ["Log in as employer", "Navigate to job applications", "View AI Recommendations section", "Review candidate match scores", "Review match reasons", "Test refresh functionality"]),
            TestCase("4.6", "AI Features", "AI Provider Fallback",
                    "Verify automatic fallback between OpenAI and Anthropic providers",
                    ["Configure primary provider", "Simulate provider failure", "Verify automatic switch to fallback"]),
        ])
        
        # Interview Scheduling (Phase 3 - Complete)
        test_cases.extend([
            TestCase("5.1", "Interviews", "Schedule Interview (Employer)",
                    "Verify employer can schedule interviews with candidates",
                    ["Log in as employer", "Navigate to application", "Click Schedule Interview", "Select date/time", "Add meeting link", "Send invitation"]),
            TestCase("5.2", "Interviews", "View Scheduled Interviews (Employer)",
                    "Verify employer can view all scheduled interviews",
                    ["Log in as employer", "Navigate to Interviews page", "View calendar/list of interviews"]),
            TestCase("5.3", "Interviews", "View Scheduled Interviews (Job Seeker)",
                    "Verify job seeker can view their scheduled interviews",
                    ["Log in as job seeker", "Navigate to Interviews page", "View upcoming interviews"]),
            TestCase("5.4", "Interviews", "Interview Email Notifications",
                    "Verify email notifications are sent for interview scheduling",
                    ["Schedule interview", "Check candidate email", "Verify interview details in email"]),
            TestCase("5.5", "Interviews", "Update Interview Status",
                    "Verify employer can update interview status",
                    ["Log in as employer", "Navigate to interview", "Update status (completed, cancelled)", "Save"]),
        ])
        
        # Email Notifications (Phase 2 - Complete)
        test_cases.extend([
            TestCase("6.1", "Email", "Application Submitted Email",
                    "Verify job seeker receives confirmation email after applying",
                    ["Apply to job", "Check email", "Verify confirmation email received"]),
            TestCase("6.2", "Email", "Application Status Update Email",
                    "Verify job seeker receives email when application status changes",
                    ["Employer updates application status", "Check job seeker email", "Verify status update email"]),
            TestCase("6.3", "Email", "Job Alert Email",
                    "Verify job seekers receive email alerts for matching jobs",
                    ["Configure job preferences", "New matching job posted", "Check email", "Verify job alert email"]),
        ])
        
        # UI/UX Features (Phase 4 - Complete)
        test_cases.extend([
            TestCase("7.1", "UI/UX", "Dark Mode Toggle",
                    "Verify dark mode toggle works throughout the application",
                    ["Click theme toggle in navbar", "Verify theme changes", "Navigate through pages", "Verify dark mode persists"]),
            TestCase("7.2", "UI/UX", "Password Visibility Toggle",
                    "Verify password visibility toggle works in login and registration forms",
                    ["Navigate to login", "Toggle password visibility", "Verify eye icon changes", "Verify password shows/hides", "Test in registration form"]),
            TestCase("7.3", "UI/UX", "Loading States",
                    "Verify loading states display correctly for async operations",
                    ["Perform actions (search, apply, upload)", "Verify loading spinners", "Verify loading messages"]),
            TestCase("7.4", "UI/UX", "Error Handling and Messages",
                    "Verify user-friendly error messages display correctly",
                    ["Trigger errors (invalid login, network error)", "Verify error messages", "Verify retry options"]),
            TestCase("7.5", "UI/UX", "Empty States",
                    "Verify helpful empty state messages display when no data",
                    ["Navigate to empty lists (applications, jobs, recommendations)", "Verify empty state messages", "Verify call-to-action buttons"]),
        ])
        
        # Edge Cases & Error Handling (Phase 4 - Complete)
        test_cases.extend([
            TestCase("8.1", "Edge Cases", "Form Validation",
                    "Verify all forms have proper validation",
                    ["Test empty fields", "Test invalid formats", "Test mismatches (password confirmation)", "Verify validation messages"]),
            TestCase("8.2", "Edge Cases", "Network Error Handling",
                    "Verify app handles network errors gracefully",
                    ["Go offline", "Try actions", "Verify error messages", "Go online", "Retry"]),
            TestCase("8.3", "Edge Cases", "Session Expiration",
                    "Verify app handles expired JWT tokens properly",
                    ["Wait for token expiry", "Try action", "Verify redirect to login"]),
            TestCase("8.4", "Edge Cases", "Large File Upload",
                    "Verify file upload handles large files appropriately",
                    ["Try uploading large resume file", "Verify error message or progress indicator"]),
            TestCase("8.5", "Edge Cases", "XSS Prevention",
                    "Verify app is protected against XSS vulnerabilities",
                    ["Try malicious input in forms", "Verify sanitization", "Verify no script execution"]),
            TestCase("8.6", "Edge Cases", "Concurrent Actions",
                    "Verify app handles concurrent user actions",
                    ["Open two tabs", "Perform same action", "Verify no conflicts", "Verify data consistency"]),
            TestCase("8.7", "Edge Cases", "Duplicate Application Prevention",
                    "Verify users cannot apply to the same job twice",
                    ["Apply to job", "Try to apply again", "Verify prevention message"]),
            TestCase("8.8", "Edge Cases", "Rate Limiting Error Handling",
                    "Verify frontend handles rate limit errors gracefully",
                    ["Exceed rate limit", "Verify user-friendly error message", "Verify retry-after information"]),
        ])
        
        # Responsive Design (Phase 4 - Complete)
        test_cases.extend([
            TestCase("9.1", "Responsive", "Mobile Responsiveness (375px)",
                    "Verify app works well on mobile devices",
                    ["Set width to 375px", "Navigate through pages", "Test functionality", "Verify mobile menu"]),
            TestCase("9.2", "Responsive", "Tablet Responsiveness (768px)",
                    "Verify app works well on tablet devices",
                    ["Set width to 768px", "Navigate through pages", "Test functionality"]),
            TestCase("9.3", "Responsive", "Desktop Responsiveness (1920px)",
                    "Verify app looks good on large screens",
                    ["Set to full screen", "Navigate through pages", "Check layout", "Verify dark mode"]),
        ])
        
        # Performance (Phase 4 - Complete)
        test_cases.extend([
            TestCase("10.1", "Performance", "Page Load Time",
                    "Verify pages load within acceptable time",
                    ["Clear cache", "Navigate to pages", "Measure load times", "Verify < 3 seconds"]),
            TestCase("10.2", "Performance", "Search Performance",
                    "Verify search returns results quickly",
                    ["Perform various searches", "Measure response time", "Verify < 1 second"]),
            TestCase("10.3", "Performance", "Large Dataset Handling",
                    "Verify app handles large amounts of data",
                    ["Test with 1000+ jobs", "Test pagination", "Test filtering", "Verify performance"]),
            TestCase("10.4", "Performance", "AI Recommendation Performance",
                    "Verify AI recommendations load within acceptable time",
                    ["Navigate to recommendations", "Measure load time", "Verify < 5 seconds"]),
        ])
        
        # Security & Compliance (Phase 4 - Complete)
        test_cases.extend([
            TestCase("11.1", "Security", "Password Hashing",
                    "Verify passwords are properly hashed (bcrypt)",
                    ["Register new user", "Check database", "Verify password is hashed"]),
            TestCase("11.2", "Security", "JWT Token Security",
                    "Verify JWT tokens are properly secured",
                    ["Log in", "Check token in storage", "Verify httpOnly or secure storage"]),
            TestCase("11.3", "Security", "CORS Configuration",
                    "Verify CORS is properly configured",
                    ["Test cross-origin requests", "Verify CORS headers", "Verify allowed origins"]),
            TestCase("11.4", "Security", "Input Sanitization",
                    "Verify all user inputs are sanitized",
                    ["Test various inputs", "Verify no script injection", "Verify SQL injection prevention"]),
        ])

        # Infrastructure & DevOps (Phase 1 & 4 - Complete) - Product Runtime
        test_cases.extend([
            TestCase("12.1", "Infrastructure", "Backend Docker Image Build",
                    "Verify backend Docker image builds successfully using backend.Dockerfile",
                    ["From project root, run docker compose build backend", "Verify image builds without errors"]),
            TestCase("12.2", "Infrastructure", "Frontend Docker Image Build",
                    "Verify frontend Docker image builds successfully using frontend.Dockerfile",
                    ["From project root, run docker compose build frontend", "Verify image builds without errors"]),
            TestCase("12.3", "Infrastructure", "Docker Compose Up (Full Stack)",
                    "Verify full stack (backend + frontend) starts correctly with docker-compose.yml",
                    ["Run docker compose up", "Verify backend is reachable on port 8000", "Verify frontend is reachable on port 3000"]),
            TestCase("12.4", "Infrastructure", "Environment Variables & Secrets",
                    "Verify app behavior when critical environment variables are missing or misconfigured",
                    ["Temporarily remove or change a required env var", "Start backend", "Verify clear startup error or validation message", "Restore env var and confirm normal startup"]),
            TestCase("12.5", "Infrastructure", "Rate Limiting Configuration",
                    "Verify rate limiting is correctly configured and can be toggled via settings",
                    ["Check RATE_LIMIT_ENABLED and related settings", "Hit auth and AI endpoints rapidly", "Verify 429 responses and proper headers"]),
        ])

        # End-to-End Journeys (Covers Phases 1–4 Plan)
        test_cases.extend([
            TestCase("13.1", "End-to-End", "Job Seeker Happy Path",
                    "Verify a job seeker can complete the full journey from registration to interview",
                    ["Register as job seeker", "Complete profile and upload resume with AI parsing", "Search for jobs and view details", "Apply to at least one job with AI-generated cover letter", "View application status updates and email notifications", "Accept interview invite and view it in dashboard"]),
            TestCase("13.2", "End-to-End", "Employer Happy Path",
                    "Verify an employer can complete the full journey from registration to interviewing candidates",
                    ["Register as employer", "Create and publish a job", "Review incoming applications", "Use AI candidate matching for a job", "Shortlist and reject candidates", "Schedule an interview and confirm emails are sent"]),
            TestCase("13.3", "End-to-End", "AI Assistant & Recommendations Coverage",
                    "Verify AI assistant, job recommendations, and candidate matching all work together",
                    ["Log in as job seeker and ask AI assistant about improving profile", "View AI job recommendations and navigate to a recommended job", "Log in as employer for that job and view AI candidate matching list", "Confirm match scores and reasons are consistent with profiles and job description"]),
            TestCase("13.4", "End-to-End", "Multi-Role Isolation",
                    "Verify data separation and correct routing between job seeker and employer roles",
                    ["Create both job seeker and employer accounts", "Log in as each in different browsers/incognito", "Verify dashboards, menus, and accessible pages are appropriate per role", "Confirm one role cannot see or modify the other's data"]),
        ])

        # n8n Workflows & Integrations (Phase 3 & 4 - Complete) - Functional Effects
        test_cases.extend([
            TestCase("14.1", "n8n", "n8n Connectivity (Functional)",
                    "Verify backend can reach the configured n8n instance",
                    ["Ensure n8n is running", "Trigger a simple test workflow from backend (e.g., via n8n_client)", "Verify successful response"]),
            TestCase("14.2", "n8n", "Workflow Configuration Documentation",
                    "Verify at least one user-visible feature that depends on n8n behaves correctly",
                    ["Perform an action in the app that triggers an n8n workflow (such as a notification or background process)", "Confirm the expected outcome occurs (email sent, record updated, or external system called)", "Check n8n execution history to confirm the workflow ran without errors"]),
            TestCase("14.3", "n8n", "n8n Compliance Verification",
                    "Verify all critical n8n workflows required by the app complete successfully",
                    ["Identify critical workflows (e.g., email notifications or AI orchestration)", "Trigger each workflow via normal app usage", "Confirm correct side effects for each (emails, updates, logs) with no failures in n8n"]),
        ])

        # Testing Tools & Data Seeding (Phase 4 - Complete)
        test_cases.extend([
            TestCase("15.1", "Testing Tools", "GUI Testing Tracker Functionality",
                    "Verify this Testing Tracker tool works end-to-end for a tester",
                    ["Launch testing_tool/test_tracker.py", "Enter tester name", "Update a few test cases", "Save results file and reopen to confirm persistence"]),
            TestCase("15.2", "Testing Tools", "Results Export and Reload",
                    "Verify test results can be exported and reloaded without data loss",
                    ["Mark several tests as Pass/Fail with notes", "Save to results file", "Close app", "Reopen and load results file", "Verify statuses, notes, and bugs persist"]),
            TestCase("15.3", "Testing Tools", "Database/Test Data Seeding",
                    "Verify database seeding tools (DB_ContentGen) successfully create realistic demo data used by the app",
                    ["Run seeding scripts for sample jobs, users, and applications", "Log in as job seeker and employer", "Verify seeded data appears correctly in job lists, recommendations, and candidate matching views"]),
        ])
        
        # Documentation & Compliance (Phase 4 - Complete)
        test_cases.extend([
            TestCase("16.1", "Documentation", "ERD Diagram Verification",
                    "Verify ERD diagram exists in README.md with all 7 MongoDB collections and relationships",
                    ["Open root README.md", "Locate ERD section (Entity Relationship Diagram)", "Verify all 7 collections present: User, Company, Job, Application, Resume, Conversation, Interview", "Verify relationships are shown with proper cardinality", "Verify Mermaid diagram renders correctly"]),
            TestCase("16.2", "Documentation", "Architecture Diagrams Verification",
                    "Verify all architecture diagrams exist in README.md and use Mermaid format",
                    ["Open root README.md", "Verify System Flow Diagram exists", "Verify Detailed System Architecture Diagram exists", "Verify Frontend Architecture Diagram exists", "Verify all diagrams use Mermaid format", "Verify diagrams are readable and comprehensive"]),
            TestCase("16.3", "Documentation", "README Production Status Verification",
                    "Verify README documents production-ready status with all phases complete and bonus features",
                    ["Open root README.md", "Verify project status shows 'Production Ready' or 'All Phases Complete'", "Verify all 4 phases marked as complete", "Verify bonus features section lists 11+ features", "Verify tech stack section includes AI providers, ChromaDB, LangChain, n8n", "Verify deployment section exists with Docker instructions"]),
            TestCase("16.4", "Documentation", "Cross-Platform Instructions Verification",
                    "Verify frontend and backend READMEs have instructions for Windows (PowerShell/CMD) and macOS/Linux (bash)",
                    ["Open frontend/README.md", "Verify Windows PowerShell commands for env file creation", "Verify Windows CMD commands as alternative", "Verify macOS/Linux bash commands", "Open backend/README.md", "Verify venv activation for Windows and Linux/Mac", "Verify all critical setup steps have OS-specific instructions"]),
            TestCase("16.5", "Documentation", "Compliance Documentation Verification",
                    "Verify all compliance and verification documents exist in docs/ folder",
                    ["Check docs/SPEC_TO_IMPLEMENTATION_ANALYSIS.md exists", "Check docs/PROJECT_IMPLEMENTATION_VERIFICATION.md exists", "Check docs/SPECIFICATION_COMPLIANCE_REVIEW.md exists", "Check docs/TEST_TRACKER_COMPLIANCE_REVIEW.md exists", "Open each document and verify it has comprehensive content", "Verify all documents show 100% compliance/completion"]),
        ])

        return test_cases
    
    def setup_ui(self):
        """Setup the user interface."""
        # Create main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(2, weight=1)  # Row 2 contains the main content (test list and details)
        
        # Save location info banner at the very top
        self.create_save_location_banner(main_container)
        
        # Header
        self.create_header(main_container)

        # Split main content area into adjustable panes (left: Test Cases, right: Test Details)
        paned = ttk.PanedWindow(main_container, orient=tk.HORIZONTAL)
        paned.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Left and right containers inside the paned window
        left_container = ttk.Frame(paned)
        right_container = ttk.Frame(paned)
        paned.add(left_container, weight=1)
        paned.add(right_container, weight=2)

        # Left panel - Test list
        self.create_test_list(left_container)

        # Right panel - Test details
        self.create_test_details(right_container)
        
        # Bottom panel - Actions
        self.create_actions(main_container)
    
    def create_save_location_banner(self, parent):
        """Create a banner at the top showing where results will be saved."""
        banner_frame = tk.Frame(parent, bg=self.colors['info'], relief=tk.FLAT, bd=0)
        banner_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        banner_inner = tk.Frame(banner_frame, bg=self.colors['info'])
        banner_inner.pack(fill=tk.X, padx=15, pady=8)
        
        # Get the current working directory and results path
        current_dir = Path.cwd()
        results_path = (current_dir / "results").resolve()
        
        # Create results directory if it doesn't exist
        results_path.mkdir(exist_ok=True)
        
        # Icon and title
        tk.Label(banner_inner,
                text="💾",
                font=("Arial", 14),
                bg=self.colors['info'],
                fg=self.colors['white']).pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Label(banner_inner,
                text="Save Location:",
                font=("Arial", 11, "bold"),
                bg=self.colors['info'],
                fg=self.colors['white']).pack(side=tk.LEFT, padx=(0, 8))
        
        # Path
        tk.Label(banner_inner,
                text=str(results_path),
                font=("Arial", 10),
                bg=self.colors['info'],
                fg=self.colors['white']).pack(side=tk.LEFT)
        
        # Info text
        tk.Label(banner_inner,
                text="(Test results and progress files will be saved here)",
                font=("Arial", 9, "italic"),
                bg=self.colors['info'],
                fg=self.colors['light']).pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_header(self, parent):
        """Create header section with modern styling."""
        # Main header frame with colored background
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=120)
        header_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.grid_propagate(False)
        
        # Inner container for padding
        inner_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Top row - Title and Tester Info
        top_row = tk.Frame(inner_frame, bg=self.colors['primary'])
        top_row.pack(fill=tk.X, pady=(0, 10))
        
        # Title with icon
        title_frame = tk.Frame(top_row, bg=self.colors['primary'])
        title_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(title_frame, 
                              text=f"🧪 TalentNest Testing Tracker v{self.VERSION}",
                              font=("Arial", 20, "bold"),
                              bg=self.colors['primary'],
                              fg=self.colors['white'])
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = tk.Label(title_frame,
                                 text="  Manual Testing Dashboard",
                                 font=("Arial", 11),
                                 bg=self.colors['primary'],
                                 fg=self.colors['light'])
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Tester info on the right
        info_frame = tk.Frame(top_row, bg=self.colors['white'], relief=tk.FLAT, bd=0)
        info_frame.pack(side=tk.RIGHT, padx=5, pady=2)
        
        info_inner = tk.Frame(info_frame, bg=self.colors['white'])
        info_inner.pack(padx=15, pady=8)
        
        tk.Label(info_inner, text="👤 Tester:", 
                font=("Arial", 10, "bold"),
                bg=self.colors['white'],
                fg=self.colors['dark']).grid(row=0, column=0, padx=(0, 5), sticky=tk.W)
        self.tester_entry = ttk.Entry(info_inner, width=18, font=("Arial", 10))
        self.tester_entry.grid(row=0, column=1, padx=5)
        self.tester_entry.bind('<FocusOut>', self.on_tester_name_complete)
        self.tester_entry.bind('<Return>', self.on_tester_name_complete)  # Enter key
        
        tk.Label(info_inner, text="🌐 Browser:",
                font=("Arial", 10, "bold"),
                bg=self.colors['white'],
                fg=self.colors['dark']).grid(row=0, column=2, padx=(15, 5), sticky=tk.W)
        self.browser_combo = ttk.Combobox(info_inner, width=12, font=("Arial", 10),
                                         values=["Chrome", "Firefox", "Safari", "Edge", "Other..."])
        self.browser_combo.grid(row=0, column=3, padx=5)
        self.browser_combo.bind('<<ComboboxSelected>>', self.on_browser_selected)
        self.browser_combo.bind('<FocusOut>', self.on_browser_complete)
        
        # Mode toggle (Real/Mockup) on the right
        mode_frame = tk.Frame(top_row, bg=self.colors['white'], relief=tk.FLAT, bd=0)
        mode_frame.pack(side=tk.RIGHT, padx=(10, 0), pady=2)
        
        mode_inner = tk.Frame(mode_frame, bg=self.colors['white'])
        mode_inner.pack(padx=15, pady=8)
        
        tk.Label(mode_inner, text="Mode:", 
                font=("Arial", 10, "bold"),
                bg=self.colors['white'],
                fg=self.colors['dark']).grid(row=0, column=0, padx=(0, 10), sticky=tk.W)
        
        # Create mode variable
        self.mode_var = tk.StringVar(value="real")
        
        # Real mode radio button
        real_radio = tk.Radiobutton(mode_inner,
                                    text="🎯 REAL Testing",
                                    variable=self.mode_var,
                                    value="real",
                                    font=("Arial", 9, "bold"),
                                    bg=self.colors['white'],
                                    fg=self.colors['success'],
                                    selectcolor=self.colors['white'],
                                    activebackground=self.colors['white'],
                                    command=self.on_mode_change)
        real_radio.grid(row=0, column=1, padx=5)
        
        # Mockup mode radio button
        mockup_radio = tk.Radiobutton(mode_inner,
                                      text="🧪 MOCKUP/Practice",
                                      variable=self.mode_var,
                                      value="mockup",
                                      font=("Arial", 9),
                                      bg=self.colors['white'],
                                      fg=self.colors['warning'],
                                      selectcolor=self.colors['white'],
                                      activebackground=self.colors['white'],
                                      command=self.on_mode_change)
        mockup_radio.grid(row=0, column=2, padx=5)
        
        # Bottom row - Progress
        progress_frame = tk.Frame(inner_frame, bg=self.colors['primary'])
        progress_frame.pack(fill=tk.X)
        
        # Loaded file label (top row)
        self.loaded_file_label = tk.Label(progress_frame,
                                          text="",
                                          font=("Arial", 9, "italic"),
                                          bg=self.colors['primary'],
                                          fg=self.colors['light'])
        self.loaded_file_label.pack(side=tk.TOP, anchor=tk.W, padx=5, pady=(2, 0))
        
        # Progress label (bottom row)
        progress_label_frame = tk.Frame(progress_frame, bg=self.colors['primary'])
        progress_label_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_label = tk.Label(progress_label_frame,
                                       text="Progress: 0/0 tests (0%)",
                                       font=("Arial", 11, "bold"),
                                       bg=self.colors['primary'],
                                       fg=self.colors['white'])
        self.progress_label.pack(side=tk.LEFT)
        
        # Stats labels
        self.stats_label = tk.Label(progress_label_frame,
                                    text="✅ 0 Pass  |  ❌ 0 Fail  |  🚫 0 Blocked  |  ⬜ 0 Not Started",
                                    font=("Arial", 10),
                                    bg=self.colors['primary'],
                                    fg=self.colors['light'])
        self.stats_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, length=500, mode='determinate')
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
        
    def create_test_list(self, parent):
        """Create test list section."""
        list_frame = ttk.LabelFrame(parent, text="Test Cases", padding="5")
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Quick jump buttons with better styling
        jump_container = tk.Frame(list_frame, bg=self.colors['light'], relief=tk.FLAT, bd=1)
        jump_container.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 8))
        
        self.jump_frame = tk.Frame(jump_container, bg=self.colors['light'])
        self.jump_frame.pack(fill=tk.X, padx=8, pady=6)
        
        tk.Label(self.jump_frame, text="⚡ Quick Jump:", 
                font=("Arial", 10, "bold"),
                bg=self.colors['light'],
                fg=self.colors['dark']).grid(row=0, column=0, padx=(0, 8), sticky=tk.W)
        
        # Store section buttons
        self.section_buttons = {}
        
        # Create treeview (no height limit - let it expand to fill space)
        columns = ("ID", "Section", "Title", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings")
        
        # Configure columns
        self.tree.column("#0", width=30, stretch=False)
        self.tree.column("ID", width=50, stretch=False)
        self.tree.column("Section", width=100)
        self.tree.column("Title", width=250)
        self.tree.column("Status", width=100)
        
        # Configure headings
        self.tree.heading("#0", text="")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Section", text="Section")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Status", text="Status")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Populate tree
        self.populate_tree()
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self.on_test_select)
        
    def populate_tree(self):
        """Populate the test tree."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Group by section
        sections = {}
        for test in self.test_cases:
            if test.section not in sections:
                sections[test.section] = []
            sections[test.section].append(test)
        
        # Store section items for jumping
        self.section_items = {}
        
        # Create quick jump buttons (only first time)
        if not self.section_buttons:
            section_list = list(sections.keys())
            
            # Split buttons into two rows (8 buttons per row)
            buttons_per_row = 8
            
            for idx, section in enumerate(section_list):
                # Calculate row and column for two-row layout
                row = (idx // buttons_per_row)
                col = (idx % buttons_per_row) + 1  # +1 to leave space for label
                
                # Short names and icons for buttons
                button_info = {
                    "Authentication": ("🔐 Auth", "#8b5cf6"),      # Purple
                    "Job Seeker": ("👤 Seeker", "#3b82f6"),       # Blue
                    "Employer": ("💼 Employer", "#06b6d4"),       # Cyan
                    "AI Features": ("🤖 AI", "#10b981"),          # Green
                    "Interview": ("📅 Interview", "#f97316"),     # Orange
                    "Email": ("📧 Email", "#8b5cf6"),             # Purple
                    "UI/UX": ("🎨 UI/UX", "#ec4899"),             # Pink
                    "Edge Cases": ("⚠️ Edge", "#f59e0b"),         # Orange
                    "Responsive": ("📱 Resp", "#ec4899"),         # Pink
                    "Performance": ("⚡ Perf", "#ef4444"),        # Red
                    "Security": ("🔒 Security", "#dc2626"),       # Dark Red
                    "Infrastructure": ("🏗️ Infra", "#6366f1"),    # Indigo
                    "End-to-End": ("🔄 E2E", "#14b8a6"),          # Teal
                    "n8n": ("🔗 n8n", "#059669"),                 # Emerald
                    "Testing Tools": ("🧪 Tools", "#8b5cf6"),     # Purple
                    "Documentation": ("📚 Docs", "#0ea5e9")       # Sky Blue
                }
                btn_text, btn_color = button_info.get(section, (section[:6], self.colors['primary']))
                
                # Create button with explicit command
                def make_command(s):
                    return lambda: self.jump_to_section(s)
                
                # Create styled button with better visual feedback
                btn = tk.Button(self.jump_frame, 
                               text=btn_text,
                               font=("Arial", 9, "bold"),
                               bg=btn_color,
                               fg="white",
                               activebackground=btn_color,
                               activeforeground="white",
                               relief=tk.RAISED,  # Raised relief for button look
                               bd=2,              # Border width
                               cursor="hand2",
                               padx=12,
                               pady=6,
                               command=make_command(section))
                btn.grid(row=row, column=col, padx=3, pady=2)
                
                # Add hover effects
                def on_enter(e, button=btn, color=btn_color):
                    button.config(relief=tk.SUNKEN, bd=3)
                
                def on_leave(e, button=btn, color=btn_color):
                    button.config(relief=tk.RAISED, bd=2)
                
                btn.bind("<Enter>", on_enter)
                btn.bind("<Leave>", on_leave)
                
                self.section_buttons[section] = btn
        
        # Add to tree
        for section, tests in sections.items():
            section_id = self.tree.insert("", "end", text="📁", values=("", section, "", ""),
                                         tags=("section", section))
            self.section_items[section] = section_id
            
            for test in tests:
                # Status icon
                icon = self.get_status_icon(test.status)
                self.tree.insert(section_id, "end", text=icon,
                               values=(test.id, "", test.title, test.status),
                               tags=(test.id,))
        
        # Expand all sections
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
    
    def get_status_icon(self, status):
        """Get icon for status."""
        icons = {
            "Not Started": "⬜",
            "Pass": "✅",
            "Fail": "❌",
            "Blocked": "🚫"
        }
        return icons.get(status, "⬜")
    
    def create_test_details(self, parent):
        """Create test details section."""
        details_frame = ttk.LabelFrame(parent, text="Test Details", padding="5")
        details_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        details_frame.columnconfigure(0, weight=1)
        # Let multiple rows expand so the panel can use available vertical space
        details_frame.rowconfigure(3, weight=1)  # Description
        details_frame.rowconfigure(5, weight=2)  # Steps
        details_frame.rowconfigure(7, weight=2)  # Actual Results
        details_frame.rowconfigure(9, weight=1)  # Notes
        
        # Test ID and Title
        self.test_id_label = ttk.Label(details_frame, text="Select a test case",
                                       font=("Arial", 12, "bold"))
        self.test_id_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Status - Color-coded buttons (move near top so they are always visible)
        status_frame = tk.Frame(details_frame, bg=self.colors['white'])
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        tk.Label(status_frame, text="Status:", font=("Arial", 10, "bold"),
                bg=self.colors['white']).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.status_var = tk.StringVar(value="Not Started")
        
        # Define status colors
        self.status_colors = {
            "Not Started": {"bg": "white", "fg": "black", "active": "#f0f0f0"},
            "Pass": {"bg": "#28a745", "fg": "white", "active": "#218838"},  # Green
            "Fail": {"bg": "#dc3545", "fg": "white", "active": "#c82333"},  # Red
            "Blocked": {"bg": "#fd7e14", "fg": "white", "active": "#e8590c"}  # Orange
        }
        
        # Create status buttons
        self.status_buttons = {}
        statuses = ["Not Started", "Pass", "Fail", "Blocked"]
        for i, status in enumerate(statuses):
            btn = tk.Button(
                status_frame, 
                text=status,
                font=("Arial", 9, "bold"),
                width=12,
                relief=tk.RAISED,
                bd=2,
                command=lambda s=status: self.set_status(s)
            )
            btn.grid(row=0, column=i+1, padx=5)
            self.status_buttons[status] = btn
            
        # Initialize button colors
        self.update_status_button_colors()

        # Description
        ttk.Label(details_frame, text="Description:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.description_label = ttk.Label(details_frame, text="", wraplength=600)
        self.description_label.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Steps
        ttk.Label(details_frame, text="Steps:", font=("Arial", 10, "bold")).grid(
            row=4, column=0, sticky=tk.W)
        # Slightly smaller height so status buttons stay visible on shorter screens
        self.steps_text = scrolledtext.ScrolledText(details_frame, height=5, wrap=tk.WORD)
        self.steps_text.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.steps_text.config(state=tk.DISABLED)
        
        # Actual Results
        ttk.Label(details_frame, text="Actual Results:", font=("Arial", 10, "bold")).grid(
            row=6, column=0, sticky=tk.W)
        self.results_text = scrolledtext.ScrolledText(details_frame, height=5, wrap=tk.WORD)
        self.results_text.grid(row=7, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Notes
        ttk.Label(details_frame, text="Notes:", font=("Arial", 10, "bold")).grid(
            row=8, column=0, sticky=tk.W)
        self.notes_text = scrolledtext.ScrolledText(details_frame, height=3, wrap=tk.WORD)
        self.notes_text.grid(row=9, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Bug reporting section
        bug_frame = ttk.Frame(details_frame)
        bug_frame.grid(row=10, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(bug_frame, text="Bugs:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W)
        
        self.bugs_label = ttk.Label(bug_frame, text="No bugs reported", foreground="green")
        self.bugs_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        ttk.Button(bug_frame, text="Report Bug", command=self.report_bug).grid(
            row=0, column=2, padx=5)
        ttk.Button(bug_frame, text="View Bugs", command=self.view_bugs).grid(
            row=0, column=3, padx=5)
        
    def create_actions(self, parent):
        """Create actions section."""
        actions_frame = ttk.Frame(parent)
        actions_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Left side buttons - Database actions
        left_frame = ttk.Frame(actions_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        # Database buttons (v2.0)
        self.load_db_button = ttk.Button(left_frame, text="📥 Load from Database", 
                                        command=self.load_from_database,
                                        style="Primary.TButton")
        self.load_db_button.grid(row=0, column=0, padx=5)
        
        self.save_db_button = ttk.Button(left_frame, text="💾 Save to Database", 
                                        command=self.save_to_database,
                                        style="Success.TButton")
        self.save_db_button.grid(row=0, column=1, padx=5)
        
        # Legacy file buttons (keep for backward compatibility)
        self.load_file_button = ttk.Button(left_frame, text="📂 Load File", 
                                          command=self.load_progress)
        self.load_file_button.grid(row=0, column=2, padx=5)
        
        self.save_file_button = ttk.Button(left_frame, text="💾 Save File", 
                                          command=self.save_progress)
        self.save_file_button.grid(row=0, column=3, padx=5)
        
        self.export_button = ttk.Button(left_frame, text="📄 Export Report", 
                                       command=self.export_report)
        self.export_button.grid(row=0, column=4, padx=5)
        
        # Right side buttons
        right_frame = ttk.Frame(actions_frame)
        right_frame.grid(row=0, column=1, sticky=tk.E)
        
        # Navigation buttons on top row
        nav_frame = ttk.Frame(right_frame)
        nav_frame.grid(row=0, column=0, sticky=tk.E)
        self.prev_button = ttk.Button(nav_frame, text="Previous", command=self.previous_test)
        self.prev_button.grid(row=0, column=0, padx=5)
        self.next_button = ttk.Button(nav_frame, text="Next", command=self.next_test)
        self.next_button.grid(row=0, column=1, padx=5)
        
        # Exit button on bottom row (safer placement)
        exit_frame = ttk.Frame(right_frame)
        exit_frame.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
        ttk.Button(exit_frame, text="🚪 Exit Application", command=self.on_closing,
                  style="Danger.TButton").grid(row=0, column=0, padx=5)
        
        actions_frame.columnconfigure(1, weight=1)
        
        # Info section at the bottom - showing database info
        info_frame = tk.Frame(parent, bg=self.colors['info'], relief=tk.FLAT, bd=1)
        info_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        info_container = tk.Frame(info_frame, bg=self.colors['info'])
        info_container.pack(fill=tk.X, padx=10, pady=8)
        
        # Title
        tk.Label(info_container,
                text="💾 Database Integration (v2.0):",
                font=("Arial", 10, "bold"),
                bg=self.colors['info'],
                fg=self.colors['white']).pack(side=tk.LEFT, padx=(0, 10))
        
        # Info
        tk.Label(info_container,
                text="Test results are saved to MongoDB. Ensure backend is running on localhost:8000",
                font=("Arial", 9),
                bg=self.colors['info'],
                fg=self.colors['white']).pack(side=tk.LEFT)
    
    def on_test_select(self, event):
        """Handle test selection."""
        # Skip if this is a programmatic selection
        if self._programmatic_selection:
            return
            
        selection = self.tree.selection()
        if not selection:
            return
        
        # Save current test if any
        if self.current_test:
            self.save_current_test()
        
        # Get selected item
        item = selection[0]
        
        # Check if item still exists (handle deletion case)
        try:
            values = self.tree.item(item, 'values')
            tags = self.tree.item(item, 'tags')
        except:
            return
        
        # Check if it's a section header
        if not values[0] and "section" in tags:
            # Section header clicked - select first test in that section
            children = self.tree.get_children(item)
            if children:
                first_child = children[0]
                self._programmatic_selection = True
                self.tree.selection_set(first_child)
                self.tree.see(first_child)
                self._programmatic_selection = False
                # Trigger selection event for the first child
                child_values = self.tree.item(first_child, 'values')
                test_id = child_values[0]
                for test in self.test_cases:
                    if test.id == test_id:
                        self.current_test = test
                        self.display_test(test)
                        break
            return
        
        if not values[0]:  # Empty or invalid item
            return
        
        test_id = values[0]
        
        # Find test case
        for test in self.test_cases:
            if test.id == test_id:
                self.current_test = test
                self.display_test(test)
                break
    
    def jump_to_section(self, section):
        """Jump to a specific section."""
        if section and section in self.section_items:
            # Save current test first
            if self.current_test:
                self.save_current_test()
            
            section_item = self.section_items[section]
            # Get first test in section
            children = self.tree.get_children(section_item)
            
            if children:
                first_child = children[0]
                child_values = self.tree.item(first_child, 'values')
                test_id = child_values[0]
                
                # Find the test
                for test in self.test_cases:
                    if test.id == test_id:
                        # Use flag to prevent event from firing
                        self._programmatic_selection = True
                        
                        # Select the new item
                        self.tree.selection_set(first_child)
                        self.tree.see(first_child)
                        self.tree.focus(first_child)
                        
                        # Reset flag
                        self._programmatic_selection = False
                        
                        # Update current test and display
                        self.current_test = test
                        self.display_test(test)
                        
                        # Force UI update
                        self.root.update_idletasks()
                        break
    
    def display_test(self, test):
        """Display test details."""
        # Update title
        self.test_id_label.config(text=f"Test {test.id}: {test.title}")
        
        # Update description
        self.description_label.config(text=test.description)
        
        # Update steps
        self.steps_text.config(state=tk.NORMAL)
        self.steps_text.delete(1.0, tk.END)
        for i, step in enumerate(test.steps, 1):
            self.steps_text.insert(tk.END, f"{i}. {step}\n")
        self.steps_text.config(state=tk.DISABLED)
        
        # Update status
        self.status_var.set(test.status)
        self.update_status_button_colors()  # Update button colors
        
        # Update results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, test.actual_results)
        
        # Update notes
        self.notes_text.delete(1.0, tk.END)
        self.notes_text.insert(1.0, test.notes)
        
        # Update bugs label
        self.update_bugs_label()
    
    def save_current_test(self):
        """Save current test data."""
        if not self.current_test:
            return
        
        self.current_test.status = self.status_var.get()
        self.current_test.actual_results = self.results_text.get(1.0, tk.END).strip()
        self.current_test.notes = self.notes_text.get(1.0, tk.END).strip()
        self.current_test.tested_by = self.tester_entry.get()
        self.current_test.tested_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Mark as having unsaved changes
        self.has_unsaved_changes = True
        
        # Update tree
        self.populate_tree()
        self.update_progress()
    
    def set_status(self, status):
        """Set the status and update button colors."""
        self.status_var.set(status)
        self.update_status_button_colors()
        self.has_unsaved_changes = True
        if self.current_test:
            self.save_current_test()
    
    def update_status_button_colors(self):
        """Update status button colors based on current selection."""
        current_status = self.status_var.get()
        
        for status, btn in self.status_buttons.items():
            colors = self.status_colors[status]
            if status == current_status:
                # Selected button - show with color
                btn.config(
                    bg=colors["bg"],
                    fg=colors["fg"],
                    activebackground=colors["active"],
                    relief=tk.SUNKEN,
                    bd=3
                )
            else:
                # Unselected button - white background
                btn.config(
                    bg="white",
                    fg="black",
                    activebackground="#f0f0f0",
                    relief=tk.RAISED,
                    bd=2
                )
    
    def on_status_change(self):
        """Handle status change."""
        if self.current_test:
            self.save_current_test()
    
    def on_closing(self):
        """Handle window close event - prompt to save if there are unsaved changes."""
        # Check if there are any completed tests
        completed_tests = sum(1 for test in self.test_cases if test.status != "Not Started")
        
        if completed_tests > 0 and self.has_unsaved_changes:
            # Prompt to save to database
            mode_text = "MOCKUP" if self.mode == "mockup" else "database"
            response = messagebox.askyesnocancel(
                "Save Before Exit?",
                f"You have {completed_tests} completed test(s) with unsaved changes.\n\n"
                f"Would you like to save to {mode_text}?\n\n"
                "• Yes - Save to database\n"
                "• No - Exit without saving\n"
                "• Cancel - Return to testing"
            )
            
            if response is None:  # Cancel
                return  # Return to app
            
            if response:  # Yes - Save to database
                # Try to save to database (will offer file fallback if database unavailable)
                self.save_to_database()
                # Note: save_to_database() now handles file fallback internally
                # If user saved to file via fallback, has_unsaved_changes will be False
                # If user cancelled both database and file save, has_unsaved_changes will still be True
                if self.has_unsaved_changes:
                    # User might have cancelled or error occurred
                    confirm = messagebox.askyesno(
                        "Exit Anyway?",
                        "Save was not completed.\n\n"
                        "Exit anyway?"
                    )
                    if not confirm:
                        return
            
            # Offer to export report
            response2 = messagebox.askyesno(
                "Export Test Report?",
                f"You've completed {completed_tests} test(s).\n\n"
                "Would you like to export a summary report?\n\n"
                "This creates a readable markdown file."
            )
            
            if response2:
                self.export_report()
            
            # Exit the application
            self.root.destroy()
        else:
            # No changes or no completed tests, just close
            self.root.destroy()
    
    def update_progress(self):
        """Update progress bar, label, and stats."""
        total = len(self.test_cases)
        
        # Count by status
        passed = sum(1 for test in self.test_cases if test.status == "Pass")
        failed = sum(1 for test in self.test_cases if test.status == "Fail")
        blocked = sum(1 for test in self.test_cases if test.status == "Blocked")
        not_started = sum(1 for test in self.test_cases if test.status == "Not Started")
        
        completed = passed + failed + blocked
        percentage = (completed / total * 100) if total > 0 else 0
        
        # Update progress label
        self.progress_label.config(text=f"Progress: {completed}/{total} tests ({percentage:.0f}%)")
        
        # Update stats label
        self.stats_label.config(
            text=f"✅ {passed} Pass  |  ❌ {failed} Fail  |  🚫 {blocked} Blocked  |  ⬜ {not_started} Not Started"
        )
        
        # Update progress bar
        self.progress_bar['value'] = percentage
    
    def previous_test(self):
        """Navigate to previous test."""
        # Save current test data before navigating
        if self.current_test:
            self.save_current_test()
        
        if not self.current_test:
            return
        
        current_index = self.test_cases.index(self.current_test)
        if current_index > 0:
            self.select_test(self.test_cases[current_index - 1])
    
    def next_test(self):
        """Navigate to next test."""
        # Save current test data before navigating
        if self.current_test:
            self.save_current_test()
        
        if not self.current_test:
            # Select first test
            if self.test_cases:
                self.select_test(self.test_cases[0])
            return
        
        current_index = self.test_cases.index(self.current_test)
        if current_index < len(self.test_cases) - 1:
            self.select_test(self.test_cases[current_index + 1])
    
    def select_test(self, test):
        """Select a test in the tree."""
        # Find and select the test in tree
        for item in self.tree.get_children():
            for child in self.tree.get_children(item):
                values = self.tree.item(child, 'values')
                if values[0] == test.id:
                    self.tree.selection_set(child)
                    self.tree.see(child)
                    self.current_test = test
                    self.display_test(test)
                    return
    
    def check_tester_name(self):
        """Check if tester name is entered and prompt if not."""
        tester_name = self.tester_entry.get().strip()
        
        if not tester_name:
            # Disable all testing controls
            self.disable_testing_controls()
            
            # Show prompt dialog
            messagebox.showwarning(
                "Setup Required",
                "⚠️ Please enter your name AND select your browser before starting testing.\n\n"
                "Required information:\n"
                "1️⃣ Enter your name in the 'Tester' field\n"
                "2️⃣ Select your browser from the 'Browser' dropdown\n\n"
                "This information is required to:\n"
                "• Track who tested each test case\n"
                "• Identify browser-specific issues\n"
                "• Save your progress with your name\n"
                "• Generate accurate team reports"
            )
            
            # Focus on the tester entry
            self.tester_entry.focus_set()
            self.testing_enabled = False
        else:
            # Enable testing controls
            self.enable_testing_controls()
            self.testing_enabled = True
    
    def on_tester_name_complete(self, event=None):
        """Handle tester name completion (FocusOut or Enter key)."""
        tester_name = self.tester_entry.get().strip()
        
        # Validate minimum length (at least 2 characters)
        if tester_name and len(tester_name) >= 2:
            if not self.testing_enabled:
                # Update status label to show waiting for browser
                if hasattr(self, 'test_id_label'):
                    self.test_id_label.config(
                        text="⏳ Please select your browser to continue...", 
                        foreground='orange'
                    )
                
                # Check if browser is selected
                browser = self.browser_combo.get().strip()
                if not browser:
                    # Just focus on browser dropdown - no popup message
                    self.browser_combo.focus_set()
                    return
                # If browser is already filled, don't activate here - let browser selection handle it
                # This prevents double activation
        elif not tester_name and self.testing_enabled:
            self.disable_testing_controls()
            self.testing_enabled = False
        elif tester_name and len(tester_name) < 2:
            # Name too short
            messagebox.showwarning(
                "Name Too Short",
                "Please enter your full name (at least 2 characters).\n\n"
                "Example: John, Alice, Bob, etc."
            )
            self.tester_entry.focus_set()
    
    def on_browser_complete(self, event=None):
        """Handle browser selection completion."""
        # Check if both name and browser are filled
        tester_name = self.tester_entry.get().strip()
        browser = self.browser_combo.get().strip()
        
        # Don't activate if browser is still "Other..." (waiting for custom input)
        if browser == "Other...":
            return
        
        if tester_name and len(tester_name) >= 2 and browser and not self.testing_enabled:
            # Both are filled, activate testing
            self.activate_testing(tester_name)
    
    def on_mode_change(self):
        """Handle mode toggle change (Real/Mockup)."""
        self.mode = self.mode_var.get()
        
        # Update title to show current mode
        if self.mode == "mockup":
            self.root.title(f"TalentNest Testing Tracker v{self.VERSION} - ⚠️ MOCKUP MODE")
            messagebox.showinfo(
                "Mockup Mode Activated",
                "🧪 You are now in MOCKUP/Practice mode!\n\n"
                "• Use this to test the testing tracker itself\n"
                "• Practice the workflow\n"
                "• Train new team members\n\n"
                "⚠️ Data will NOT be saved to real testing results.\n"
                "Switch to REAL mode for actual testing."
            )
        else:
            self.root.title(f"TalentNest Testing Tracker v{self.VERSION}")
    
    def activate_testing(self, tester_name):
        """Activate testing after both name and browser are provided."""
        # Both name and browser are filled
        self.enable_testing_controls()
        self.testing_enabled = True
        self.save_tester_info()
        
        # Prompt to load from database
        response = messagebox.askyesno(
            "Load Previous Progress?",
            "Would you like to load previous test progress from the database?\n\n"
            "• Yes: Load TEAM_MASTER from database\n"
            "• No: Start fresh"
        )
        
        if response:
            self.load_from_database()
        else:
            messagebox.showinfo(
                "Ready to Test!",
                f"✅ Welcome, {tester_name}!\n\n"
                "You can now start testing!\n\n"
                "Tip: Use 'Load from Database' button anytime\n"
                "to load TEAM_MASTER progress."
            )
    
    def disable_testing_controls(self):
        """Disable all testing controls until name and browser are entered."""
        # Unbind tree selection event to prevent selection
        self.tree.unbind('<<TreeviewSelect>>')
        
        # Change tree appearance to show it's disabled
        style = ttk.Style()
        style.configure("Treeview", foreground="gray")
        
        # Disable text fields
        if hasattr(self, 'results_text'):
            self.results_text.config(state=tk.DISABLED, bg='#f0f0f0')
        if hasattr(self, 'notes_text'):
            self.notes_text.config(state=tk.DISABLED, bg='#f0f0f0')
        
        # Disable navigation buttons
        if hasattr(self, 'prev_button'):
            self.prev_button.config(state=tk.DISABLED)
        if hasattr(self, 'next_button'):
            self.next_button.config(state=tk.DISABLED)
        
        # Disable action buttons (database)
        if hasattr(self, 'load_db_button'):
            self.load_db_button.config(state=tk.DISABLED)
        if hasattr(self, 'save_db_button'):
            self.save_db_button.config(state=tk.DISABLED)
        # Disable action buttons (file)
        if hasattr(self, 'load_file_button'):
            self.load_file_button.config(state=tk.DISABLED)
        if hasattr(self, 'save_file_button'):
            self.save_file_button.config(state=tk.DISABLED)
        if hasattr(self, 'export_button'):
            self.export_button.config(state=tk.DISABLED)
        
        # Disable status buttons
        if hasattr(self, 'status_buttons'):
            for btn in self.status_buttons.values():
                btn.config(state=tk.DISABLED)
        
        # Update test ID label to show disabled state
        if hasattr(self, 'test_id_label'):
            self.test_id_label.config(text="⚠️ Enter your name to start testing", foreground='red')
    
    def enable_testing_controls(self):
        """Enable all testing controls."""
        # Re-bind tree selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_test_select)
        
        # Restore tree appearance
        style = ttk.Style()
        style.configure("Treeview", foreground=self.colors['dark'])
        
        # Enable text fields
        if hasattr(self, 'results_text'):
            self.results_text.config(state=tk.NORMAL, bg='white')
        if hasattr(self, 'notes_text'):
            self.notes_text.config(state=tk.NORMAL, bg='white')
        
        # Enable navigation buttons
        if hasattr(self, 'prev_button'):
            self.prev_button.config(state=tk.NORMAL)
        if hasattr(self, 'next_button'):
            self.next_button.config(state=tk.NORMAL)
        
        # Enable action buttons (database)
        if hasattr(self, 'load_db_button'):
            self.load_db_button.config(state=tk.NORMAL)
        if hasattr(self, 'save_db_button'):
            self.save_db_button.config(state=tk.NORMAL)
        # Enable action buttons (file)
        if hasattr(self, 'load_file_button'):
            self.load_file_button.config(state=tk.NORMAL)
        if hasattr(self, 'save_file_button'):
            self.save_file_button.config(state=tk.NORMAL)
        if hasattr(self, 'export_button'):
            self.export_button.config(state=tk.NORMAL)
        
        # Enable status buttons
        if hasattr(self, 'status_buttons'):
            for btn in self.status_buttons.values():
                btn.config(state=tk.NORMAL)
        
        # Reset test ID label
        if hasattr(self, 'test_id_label'):
            self.test_id_label.config(text="Select a test case", foreground='black')
    
    def on_browser_selected(self, event=None):
        """Handle browser selection, prompt for custom browser if 'Other' is selected."""
        selected = self.browser_combo.get()
        
        if selected == "Other...":
            # Prompt user for custom browser name
            from tkinter import simpledialog
            custom_browser = simpledialog.askstring(
                "Custom Browser",
                "Enter your browser name:",
                parent=self.root
            )
            
            if custom_browser and custom_browser.strip():
                # Format as "Other (BrowserName)"
                formatted_browser = f"Other ({custom_browser.strip()})"
                self.browser_combo.set(formatted_browser)
            else:
                # If cancelled or empty, don't proceed - keep "Other..." selected
                # This prevents activation until a valid browser is entered
                return
        
        # Save the tester info
        self.save_tester_info()
        
        # Check if we should activate testing (both name and browser filled)
        self.on_browser_complete()
    
    def save_tester_info(self, event=None):
        """Save tester information."""
        self.tester_info = {
            "name": self.tester_entry.get(),
            "browser": self.browser_combo.get(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    
    def load_tester_info(self):
        """Load tester information from previous session."""
        # Don't auto-load - force user to enter name each session
        # This ensures accountability and prevents accidental testing under wrong name
        self.tester_entry.delete(0, tk.END)
        self.browser_combo.set("")  # Clear browser selection
        
        # Optionally load from file but don't auto-fill (commented out)
        # try:
        #     info_file = Path("tester_info.json")
        #     if info_file.exists():
        #         with open(info_file, 'r') as f:
        #             self.tester_info = json.load(f)
        #             self.tester_entry.insert(0, self.tester_info.get("name", ""))
        #             self.browser_combo.set(self.tester_info.get("browser", "Chrome"))
        # except Exception as e:
        #     print(f"Could not load tester info: {e}")
    
    def load_team_file(self):
        """Load the team's master test results file."""
        # Look for team file first
        team_file = RESULTS_DIR / "TEAM_MASTER_test_results.json"
        
        if team_file.exists():
            # Ask if they want to load the team file
            response = messagebox.askyesno(
                "Load Team File",
                f"Found team master file:\n{team_file.name}\n\n"
                "This contains all team members' test results.\n\n"
                "Load this file to continue from where the team left off?"
            )
            
            if response:
                try:
                    with open(team_file, 'r') as f:
                        data = json.load(f)
                    
                    # Load test cases
                    for test in self.test_cases:
                        for test_data in data.get('test_cases', []):
                            if test.id == test_data['id']:
                                test.status = test_data['status']
                                test.actual_results = test_data['actual_results']
                                test.notes = test_data['notes']
                                test.tested_by = test_data['tested_by']
                                test.tested_date = test_data['tested_date']
                                test.bugs = test_data.get('bugs', [])
                                break
                    
                    # Load bugs
                    self.bugs = []
                    for bug_data in data.get('bugs', []):
                        bug = Bug(
                            bug_id=bug_data['bug_id'],
                            test_id=bug_data['test_id'],
                            title=bug_data['title'],
                            severity=bug_data['severity'],
                            priority=bug_data['priority'],
                            description=bug_data['description'],
                            steps_to_reproduce=bug_data['steps_to_reproduce'],
                            expected=bug_data['expected_behavior'],
                            actual=bug_data['actual_behavior'],
                            environment=bug_data['environment'],
                            screenshot=bug_data.get('screenshot', '')
                        )
                        bug.reported_by = bug_data.get('reported_by', '')
                        bug.reported_date = bug_data.get('reported_date', '')
                        self.bugs.append(bug)
                    
                    # Update bug counter
                    if self.bugs:
                        max_bug_num = max([int(bug.bug_id.split('-')[1]) for bug in self.bugs if '-' in bug.bug_id])
                        self.bug_counter = max_bug_num + 1
                    
                    # Refresh UI
                    self.populate_tree()
                    self.update_progress()
                    
                    if self.current_test:
                        self.display_test(self.current_test)
                    
                    # Reset unsaved changes flag
                    self.has_unsaved_changes = False
                    
                    # Track loaded filename
                    self.loaded_filename = team_file.name
                    self.loaded_file_label.config(text=f"📂 Loaded: {self.loaded_filename}")
                    
                    messagebox.showinfo("Team File Loaded", 
                                       f"✅ Loaded team master file!\n\n"
                                       f"You can now continue testing from where the team left off.\n"
                                       f"When done, use 'Save to Team File' to update the master file.")
                    return
                
                except Exception as e:
                    messagebox.showerror("Error", f"Could not load team file:\n{str(e)}")
        
        # If no team file or user declined, offer to create one or load another file
        response = messagebox.askyesnocancel(
            "No Team File Found",
            "No team master file found.\n\n"
            "• Yes - Create a new team master file\n"
            "• No - Load a different file\n"
            "• Cancel - Start fresh"
        )
        
        if response is True:  # Create new team file
            messagebox.showinfo("Team File Created",
                               "A new team master file will be created when you save.\n\n"
                               "Use 'Save to Team File' to create:\n"
                               "TEAM_MASTER_test_results.json")
        elif response is False:  # Load different file
            self.load_progress()
    
    def save_my_progress(self):
        """Save individual tester's progress (personal backup)."""
        self.save_progress()
    
    def save_personal_backup_silent(self):
        """Save personal backup automatically without prompting for filename."""
        # Save current test first
        if self.current_test:
            self.save_current_test()
        
        # Save tester info
        self.save_tester_info()
        
        # Create results directory if it doesn't exist
        RESULTS_DIR.mkdir(exist_ok=True)
        
        # Auto-generate filename
        tester_name = self.tester_entry.get() or 'tester'
        filename = RESULTS_DIR / f"test_progress_{tester_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Prepare data
        data = {
            "tester_info": self.tester_info,
            "saved_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bug_counter": self.bug_counter,
            "test_cases": [],
            "bugs": []
        }
        
        for test in self.test_cases:
            data["test_cases"].append({
                "id": test.id,
                "section": test.section,
                "title": test.title,
                "description": test.description,
                "steps": test.steps,
                "status": test.status,
                "actual_results": test.actual_results,
                "notes": test.notes,
                "tested_by": test.tested_by,
                "tested_date": test.tested_date,
                "bugs": test.bugs
            })
        
        for bug in self.bugs:
            data["bugs"].append({
                "bug_id": bug.bug_id,
                "test_id": bug.test_id,
                "title": bug.title,
                "severity": bug.severity,
                "priority": bug.priority,
                "description": bug.description,
                "steps_to_reproduce": bug.steps_to_reproduce,
                "expected_behavior": bug.expected_behavior,
                "actual_behavior": bug.actual_behavior,
                "environment": bug.environment,
                "screenshot": bug.screenshot,
                "reported_by": bug.reported_by,
                "reported_date": bug.reported_date
            })
        
        # Save to file silently
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Save tester info for next session
            with open("tester_info.json", 'w') as f:
                json.dump(self.tester_info, f, indent=2)
            
            print(f"Personal backup saved: {filename.name}")  # Console log only, no popup
        
        except Exception as e:
            print(f"Could not save personal backup: {str(e)}")
    
    def save_to_team_file(self):
        """Save/merge current results to the team master file."""
        # Save current test first
        if self.current_test:
            self.save_current_test()
        
        # Save tester info
        self.save_tester_info()
        
        # Create results directory if it doesn't exist
        RESULTS_DIR.mkdir(exist_ok=True)
        
        team_file = RESULTS_DIR / "TEAM_MASTER_test_results.json"
        
        # Check if team file exists
        if team_file.exists():
            # Merge with existing team file
            response = messagebox.askyesno(
                "Update Team File",
                f"Team master file exists.\n\n"
                f"This will merge your results with the existing team results.\n\n"
                f"Your tests will update the team file.\n"
                f"Tester: {self.tester_entry.get()}\n\n"
                f"Continue?"
            )
            
            if not response:
                return
            
            try:
                # Load existing team data
                with open(team_file, 'r') as f:
                    team_data = json.load(f)
                
                # Merge: Update tests that this tester worked on
                team_tests = {t['id']: t for t in team_data.get('test_cases', [])}
                team_bugs = {b['bug_id']: b for b in team_data.get('bugs', [])}
                
                # Update with current tester's results
                for test in self.test_cases:
                    if test.status != "Not Started" or test.id in team_tests:
                        team_tests[test.id] = {
                            "id": test.id,
                            "section": test.section,
                            "title": test.title,
                            "description": test.description,
                            "steps": test.steps,
                            "status": test.status,
                            "actual_results": test.actual_results,
                            "notes": test.notes,
                            "tested_by": test.tested_by,
                            "tested_date": test.tested_date,
                            "bugs": test.bugs
                        }
                
                # Add new bugs
                for bug in self.bugs:
                    team_bugs[bug.bug_id] = {
                        "bug_id": bug.bug_id,
                        "test_id": bug.test_id,
                        "title": bug.title,
                        "severity": bug.severity,
                        "priority": bug.priority,
                        "description": bug.description,
                        "steps_to_reproduce": bug.steps_to_reproduce,
                        "expected_behavior": bug.expected_behavior,
                        "actual_behavior": bug.actual_behavior,
                        "environment": bug.environment,
                        "screenshot": bug.screenshot,
                        "reported_by": bug.reported_by,
                        "reported_date": bug.reported_date
                    }
                
                # Prepare merged data
                merged_data = {
                    "team_file": True,
                    "last_updated_by": self.tester_info.get('name', 'Unknown'),
                    "last_updated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "bug_counter": max(team_data.get('bug_counter', 1), self.bug_counter),
                    "test_cases": list(team_tests.values()),
                    "bugs": list(team_bugs.values())
                }
                
                # Save merged data
                with open(team_file, 'w') as f:
                    json.dump(merged_data, f, indent=2)
                
                # Reset unsaved changes flag
                self.has_unsaved_changes = False
                
                messagebox.showinfo("Team File Updated",
                                   f"✅ Team master file updated successfully!\n\n"
                                   f"File: {team_file.name}\n"
                                   f"Location: {team_file.parent}\n"
                                   f"Updated by: {self.tester_entry.get()}\n\n"
                                   f"Other team members can now load this file to see your progress!")
            
            except Exception as e:
                messagebox.showerror("Error", f"Could not update team file:\n{str(e)}")
        
        else:
            # Create new team file
            response = messagebox.askyesno(
                "Create Team File",
                f"Create new team master file?\n\n"
                f"File: TEAM_MASTER_test_results.json\n"
                f"Location: {results_dir}\n\n"
                f"This will be the shared file for all team members."
            )
            
            if not response:
                return
            
            try:
                # Prepare data
                data = {
                    "team_file": True,
                    "created_by": self.tester_info.get('name', 'Unknown'),
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "last_updated_by": self.tester_info.get('name', 'Unknown'),
                    "last_updated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "bug_counter": self.bug_counter,
                    "test_cases": [],
                    "bugs": []
                }
                
                for test in self.test_cases:
                    data["test_cases"].append({
                        "id": test.id,
                        "section": test.section,
                        "title": test.title,
                        "description": test.description,
                        "steps": test.steps,
                        "status": test.status,
                        "actual_results": test.actual_results,
                        "notes": test.notes,
                        "tested_by": test.tested_by,
                        "tested_date": test.tested_date,
                        "bugs": test.bugs
                    })
                
                for bug in self.bugs:
                    data["bugs"].append({
                        "bug_id": bug.bug_id,
                        "test_id": bug.test_id,
                        "title": bug.title,
                        "severity": bug.severity,
                        "priority": bug.priority,
                        "description": bug.description,
                        "steps_to_reproduce": bug.steps_to_reproduce,
                        "expected_behavior": bug.expected_behavior,
                        "actual_behavior": bug.actual_behavior,
                        "environment": bug.environment,
                        "screenshot": bug.screenshot,
                        "reported_by": bug.reported_by,
                        "reported_date": bug.reported_date
                    })
                
                # Save to file
                with open(team_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                # Reset unsaved changes flag
                self.has_unsaved_changes = False
                
                messagebox.showinfo("Team File Created",
                                   f"✅ Team master file created successfully!\n\n"
                                   f"File: {team_file.name}\n"
                                   f"Location: {team_file.parent}\n\n"
                                   f"Team members should use 'Load Team File' to load this file.")
            
            except Exception as e:
                messagebox.showerror("Error", f"Could not create team file:\n{str(e)}")
    
    def save_progress(self):
        """Save testing progress to file."""
        # Save current test first
        if self.current_test:
            self.save_current_test()
        
        # Save tester info
        self.save_tester_info()
        
        # Create results directory if it doesn't exist
        RESULTS_DIR.mkdir(exist_ok=True)
        
        # Ask for filename (with timestamp)
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=str(RESULTS_DIR),
            initialfile=f"test_progress_{self.tester_entry.get() or 'tester'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            title="Save Test Progress"
        )
        
        if not filename:
            return
        
        # Prepare data
        data = {
            "tester_info": self.tester_info,
            "saved_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bug_counter": self.bug_counter,
            "test_cases": [],
            "bugs": []
        }
        
        for test in self.test_cases:
            data["test_cases"].append({
                "id": test.id,
                "section": test.section,
                "title": test.title,
                "description": test.description,
                "steps": test.steps,
                "status": test.status,
                "actual_results": test.actual_results,
                "notes": test.notes,
                "tested_by": test.tested_by,
                "tested_date": test.tested_date,
                "bugs": test.bugs
            })
        
        for bug in self.bugs:
            data["bugs"].append({
                "bug_id": bug.bug_id,
                "test_id": bug.test_id,
                "title": bug.title,
                "severity": bug.severity,
                "priority": bug.priority,
                "description": bug.description,
                "steps_to_reproduce": bug.steps_to_reproduce,
                "expected_behavior": bug.expected_behavior,
                "actual_behavior": bug.actual_behavior,
                "environment": bug.environment,
                "screenshot": bug.screenshot,
                "reported_by": bug.reported_by,
                "reported_date": bug.reported_date
            })
        
        # Save to file
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Save tester info for next session
            with open("tester_info.json", 'w') as f:
                json.dump(self.tester_info, f, indent=2)
            
            # Reset unsaved changes flag
            self.has_unsaved_changes = False
            
            messagebox.showinfo("Success", 
                               f"✅ Test progress saved successfully!\n\n"
                               f"File: {Path(filename).name}\n"
                               f"Location: {Path(filename).parent}\n\n"
                               f"You can load this file later to continue testing.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save progress:\n{str(e)}")
    
    def load_progress(self):
        """Load testing progress from file."""
        # Create results directory if it doesn't exist
        RESULTS_DIR.mkdir(exist_ok=True)
        
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=str(RESULTS_DIR),
            title="Load Test Progress"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Load tester info
            self.tester_info = data.get("tester_info", {})
            self.tester_entry.delete(0, tk.END)
            self.tester_entry.insert(0, self.tester_info.get("name", ""))
            self.browser_combo.set(self.tester_info.get("browser", "Chrome"))
            
            # Load bug counter
            self.bug_counter = data.get("bug_counter", 1)
            
            # Load test cases
            for test_data in data.get("test_cases", []):
                for test in self.test_cases:
                    if test.id == test_data["id"]:
                        test.status = test_data.get("status", "Not Started")
                        test.actual_results = test_data.get("actual_results", "")
                        test.notes = test_data.get("notes", "")
                        test.tested_by = test_data.get("tested_by", "")
                        test.tested_date = test_data.get("tested_date", "")
                        test.bugs = test_data.get("bugs", [])
                        break
            
            # Load bugs
            self.bugs = []
            for bug_data in data.get("bugs", []):
                bug = Bug(
                    bug_id=bug_data.get("bug_id", ""),
                    test_id=bug_data.get("test_id", ""),
                    title=bug_data.get("title", ""),
                    severity=bug_data.get("severity", "Medium"),
                    priority=bug_data.get("priority", "P2"),
                    description=bug_data.get("description", ""),
                    steps_to_reproduce=bug_data.get("steps_to_reproduce", ""),
                    expected=bug_data.get("expected_behavior", ""),
                    actual=bug_data.get("actual_behavior", ""),
                    environment=bug_data.get("environment", ""),
                    screenshot=bug_data.get("screenshot", "")
                )
                bug.reported_by = bug_data.get("reported_by", "")
                bug.reported_date = bug_data.get("reported_date", "")
                self.bugs.append(bug)
            
            # Refresh UI
            self.populate_tree()
            self.update_progress()
            
            if self.current_test:
                self.display_test(self.current_test)
            
            # Reset unsaved changes flag since we just loaded
            self.has_unsaved_changes = False
            
            # Track loaded filename
            self.loaded_filename = Path(filename).name
            self.loaded_file_label.config(text=f"📂 Loaded: {self.loaded_filename}")
            
            messagebox.showinfo("Success", f"Progress loaded from:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load progress:\n{str(e)}")
    
    def merge_results(self):
        """Merge results from multiple testers."""
        # Create results directory if it doesn't exist
        RESULTS_DIR.mkdir(exist_ok=True)
        
        # Ask user to select multiple files
        filenames = filedialog.askopenfilenames(
            title="Select Test Progress Files to Merge",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialdir=str(RESULTS_DIR)
        )
        
        if not filenames or len(filenames) < 2:
            messagebox.showwarning("Warning", 
                                  "Please select at least 2 files to merge.\n\n"
                                  "Tip: Hold Ctrl (Windows/Linux) or Cmd (Mac) to select multiple files.")
            return
        
        try:
            # Merge strategy: For each test, use the most recent completed result
            merged_tests = {}
            merged_bugs = {}
            all_testers = []
            
            for filename in filenames:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                tester_name = data.get('tester_info', {}).get('name', 'Unknown')
                all_testers.append(tester_name)
                
                # Merge test cases
                for test_data in data.get('test_cases', []):
                    test_id = test_data['id']
                    
                    # If test is not in merged yet, or if this test is completed and more recent
                    if test_id not in merged_tests:
                        merged_tests[test_id] = test_data
                    else:
                        # Prefer completed tests over not started
                        current_status = merged_tests[test_id]['status']
                        new_status = test_data['status']
                        
                        # Priority: Pass > Fail > Blocked > Not Started
                        status_priority = {
                            'Pass': 4,
                            'Fail': 3,
                            'Blocked': 2,
                            'Not Started': 1
                        }
                        
                        if status_priority.get(new_status, 0) > status_priority.get(current_status, 0):
                            merged_tests[test_id] = test_data
                        elif new_status == current_status and new_status != 'Not Started':
                            # If same status and not "Not Started", use the one with more details
                            if len(test_data.get('actual_results', '')) > len(merged_tests[test_id].get('actual_results', '')):
                                merged_tests[test_id] = test_data
                
                # Merge bugs (keep all unique bugs)
                for bug_data in data.get('bugs', []):
                    bug_id = bug_data['bug_id']
                    if bug_id not in merged_bugs:
                        merged_bugs[bug_id] = bug_data
            
            # Apply merged data to current session
            for test in self.test_cases:
                if test.id in merged_tests:
                    test_data = merged_tests[test.id]
                    test.status = test_data['status']
                    test.actual_results = test_data['actual_results']
                    test.notes = test_data['notes']
                    test.tested_by = test_data['tested_by']
                    test.tested_date = test_data['tested_date']
                    test.bugs = test_data.get('bugs', [])
            
            # Update bugs list
            self.bugs = []
            for bug_data in merged_bugs.values():
                bug = Bug(
                    bug_id=bug_data['bug_id'],
                    test_id=bug_data['test_id'],
                    title=bug_data['title'],
                    severity=bug_data['severity'],
                    priority=bug_data['priority'],
                    description=bug_data['description'],
                    steps_to_reproduce=bug_data['steps_to_reproduce'],
                    expected=bug_data['expected_behavior'],
                    actual=bug_data['actual_behavior'],
                    environment=bug_data['environment'],
                    screenshot=bug_data.get('screenshot', '')
                )
                bug.reported_by = bug_data.get('reported_by', '')
                bug.reported_date = bug_data.get('reported_date', '')
                self.bugs.append(bug)
            
            # Update bug counter
            if self.bugs:
                max_bug_num = max([int(bug.bug_id.split('-')[1]) for bug in self.bugs if '-' in bug.bug_id])
                self.bug_counter = max_bug_num + 1
            
            # Refresh UI
            self.populate_tree()
            self.update_progress()
            
            if self.current_test:
                self.display_test(self.current_test)
            
            # Show summary
            total = len(self.test_cases)
            passed = sum(1 for test in self.test_cases if test.status == "Pass")
            failed = sum(1 for test in self.test_cases if test.status == "Fail")
            blocked = sum(1 for test in self.test_cases if test.status == "Blocked")
            
            # Mark as having unsaved changes since we merged
            self.has_unsaved_changes = True
            
            messagebox.showinfo("Merge Complete", 
                               f"✅ Successfully merged {len(filenames)} test result files!\n\n"
                               f"Testers: {', '.join(all_testers)}\n\n"
                               f"Merged Results:\n"
                               f"• Passed: {passed}\n"
                               f"• Failed: {failed}\n"
                               f"• Blocked: {blocked}\n"
                               f"• Total Bugs: {len(self.bugs)}\n\n"
                               f"⚠️ Don't forget to save the merged results!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Could not merge results:\n{str(e)}")
    
    # ========================================================================
    # DATABASE METHODS (v2.0)
    # ========================================================================
    
    def get_api_endpoint(self):
        """Get the correct API endpoint based on mode (real or mockup)."""
        if self.mode == "mockup":
            return f"{self.api_base_url}/testing/mockup"
        else:
            return f"{self.api_base_url}/testing"
    
    def check_backend_health(self):
        """Check if backend is running and accessible."""
        try:
            response = requests.get(f"{self.api_base_url.replace('/api/v1', '')}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_testing_endpoint_exists(self):
        """Check if the testing endpoint exists by trying to access it."""
        endpoint = self.get_api_endpoint()
        try:
            # Try a HEAD request first (lightweight)
            try:
                response = requests.head(f"{endpoint}/test-sessions", timeout=5)
                # 405 Method Not Allowed means route exists but doesn't support HEAD
                # 404 means route doesn't exist
                if response.status_code == 405:
                    return True
                if response.status_code == 404:
                    return False
            except:
                pass
            
            # Try OPTIONS request (CORS preflight)
            try:
                response = requests.options(f"{endpoint}/test-sessions", timeout=5)
                # 405 or 200 means route exists
                # 404 means route doesn't exist
                if response.status_code in [200, 405]:
                    return True
                if response.status_code == 404:
                    return False
            except:
                pass
            
            # If we can't determine, assume it might exist (let the actual POST try)
            return None
        except requests.exceptions.ConnectionError:
            return False
        except Exception as e:
            # If we can't determine, assume it might exist
            return None
    
    def save_to_database(self):
        """Save test session to MongoDB via API."""
        # Save current test first
        if self.current_test:
            self.save_current_test()
        
        # Prepare data
        data = {
            "session_id": f"{self.tester_entry.get()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "tester_name": self.tester_entry.get(),
            "browser": self.browser_combo.get(),
            "test_date": datetime.now().isoformat(),
            "test_cases": [
                {
                    "test_id": test.id,
                    "section": test.section,
                    "title": test.title,
                    "status": test.status,
                    "actual_results": test.actual_results,
                    "notes": test.notes,
                    "tested_date": test.tested_date or None
                }
                for test in self.test_cases
            ],
            "bugs": [
                {
                    "bug_id": bug.bug_id,
                    "test_id": bug.test_id,
                    "severity": bug.severity,
                    "description": bug.description,
                    "steps_to_reproduce": bug.steps_to_reproduce,
                    "expected": bug.expected_behavior,
                    "actual": bug.actual_behavior,
                    "reported_by": bug.reported_by,
                    "reported_date": bug.reported_date
                }
                for bug in self.bugs
            ],
            "is_master": False,
            "version": self.VERSION
        }
        
        endpoint = self.get_api_endpoint()
        
        # Show warning if in mockup mode
        if self.mode == "mockup":
            response = messagebox.askyesno(
                "Mockup Mode",
                "⚠️ You are in MOCKUP mode!\n\n"
                "This will NOT save to real testing data.\n"
                "Continue?"
            )
            if not response:
                return
        
        # Check if backend is running
        if not self.check_backend_health():
            response_msg = messagebox.askyesno(
                "Backend Not Running",
                "❌ Backend server is not running or not accessible.\n\n"
                "Please ensure the backend is running:\n"
                "1. Open terminal in backend folder\n"
                "2. Run: python -m uvicorn app.main:app --reload\n"
                "3. Try saving again\n\n"
                "Would you like to save to a file instead?\n\n"
                "• Yes - Save to JSON file\n"
                "• No - Cancel save"
            )
            if response_msg:
                self.save_progress()
            return
        
        # Check if testing endpoint exists (but don't block if uncertain)
        endpoint_exists = self.check_testing_endpoint_exists()
        if endpoint_exists is False:
            # Endpoint definitely doesn't exist
            response_msg = messagebox.askyesno(
                "Database Endpoint Not Available",
                f"⚠️ The testing database endpoint is not available.\n\n"
                f"Endpoint: {endpoint}/test-sessions\n\n"
                f"The backend testing API endpoint has not been implemented yet.\n\n"
                f"Would you like to save to a file instead?\n\n"
                f"• Yes - Save to JSON file\n"
                f"• No - Cancel save"
            )
            if response_msg:
                self.save_progress()
            return
        # If endpoint_exists is None (uncertain), proceed anyway - let the POST request determine
        
        # Try to save to database
        try:
            response = requests.post(
                f"{endpoint}/test-sessions",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # Accept both 200 (OK) and 201 (Created) as success
            # 201 is common for first-time POST requests
            if response.status_code in [200, 201]:
                self.has_unsaved_changes = False
                mode_text = "MOCKUP" if self.mode == "mockup" else "database"
                status_msg = "created" if response.status_code == 201 else "saved"
                messagebox.showinfo(
                    "Success",
                    f"✅ Session {status_msg} to {mode_text}!\n\n"
                    f"Session ID: {data['session_id']}\n"
                    f"Tests completed: {sum(1 for t in self.test_cases if t.status != 'Not Started')}/{len(self.test_cases)}"
                )
            elif response.status_code == 404:
                # Endpoint not found - this shouldn't happen if check passed, but handle it anyway
                response_msg = messagebox.askyesno(
                    "Database Endpoint Not Found",
                    f"⚠️ The testing database endpoint returned 404 Not Found.\n\n"
                    f"Endpoint: {endpoint}/test-sessions\n\n"
                    f"This might mean:\n"
                    f"• The endpoint hasn't been implemented yet\n"
                    f"• The endpoint path is incorrect\n\n"
                    f"Would you like to save to a file instead?\n\n"
                    f"• Yes - Save to JSON file\n"
                    f"• No - Cancel save"
                )
                if response_msg:
                    self.save_progress()
            elif response.status_code == 422:
                # Validation error - data format issue
                error_detail = response.text
                try:
                    error_json = response.json()
                    if "detail" in error_json:
                        error_detail = str(error_json["detail"])
                except:
                    pass
                
                messagebox.showerror(
                    "Validation Error",
                    f"❌ Data validation failed:\n\n"
                    f"Status: {response.status_code}\n"
                    f"Error: {error_detail}\n\n"
                    f"Please check your test data and try again."
                )
            else:
                # Other HTTP errors
                error_detail = response.text
                try:
                    error_json = response.json()
                    if "detail" in error_json:
                        error_detail = error_json["detail"]
                except:
                    pass
                
                response_msg = messagebox.askyesno(
                    "Database Save Failed",
                    f"❌ Failed to save to database:\n\n"
                    f"Status: {response.status_code}\n"
                    f"Error: {error_detail}\n\n"
                    f"Would you like to save to a file instead?\n\n"
                    f"• Yes - Save to JSON file\n"
                    f"• No - Cancel save"
                )
                if response_msg:
                    # Fallback to file save
                    self.save_progress()
        except requests.exceptions.ConnectionError:
            response_msg = messagebox.askyesno(
                "Connection Error",
                "❌ Could not connect to backend server!\n\n"
                "The backend testing API endpoint may not be available.\n\n"
                "Would you like to save to a file instead?\n\n"
                "• Yes - Save to JSON file\n"
                "• No - Cancel save"
            )
            if response_msg:
                # Fallback to file save
                self.save_progress()
        except Exception as e:
            response_msg = messagebox.askyesno(
                "Save Error",
                f"❌ An error occurred while saving:\n\n"
                f"{str(e)}\n\n"
                f"Would you like to save to a file instead?\n\n"
                f"• Yes - Save to JSON file\n"
                f"• No - Cancel save"
            )
            if response_msg:
                # Fallback to file save
                self.save_progress()
    
    def load_from_database(self):
        """Load TEAM_MASTER from MongoDB via API."""
        endpoint = self.get_api_endpoint()
        
        # Check if backend is running first
        if not self.check_backend_health():
            response_msg = messagebox.askyesno(
                "Backend Not Running",
                "❌ Backend server is not running or not accessible.\n\n"
                "Please ensure the backend is running:\n"
                "1. Open terminal in backend folder\n"
                "2. Run: python -m uvicorn app.main:app --reload\n"
                "3. Try loading again\n\n"
                "Would you like to load from a file instead?\n\n"
                "• Yes - Load from JSON file\n"
                "• No - Cancel"
            )
            if response_msg:
                self.load_progress()
            return
        
        # Check if testing endpoint exists
        endpoint_exists = self.check_testing_endpoint_exists()
        if endpoint_exists is False:
            # Endpoint doesn't exist
            response_msg = messagebox.askyesno(
                "Database Endpoint Not Available",
                f"⚠️ The testing database endpoint is not available.\n\n"
                f"Endpoint: {endpoint}/test-sessions/master\n\n"
                f"The backend testing API endpoint has not been implemented yet.\n\n"
                f"Would you like to load from a file instead?\n\n"
                f"• Yes - Load from JSON file\n"
                f"• No - Cancel"
            )
            if response_msg:
                self.load_progress()
            return
        
        try:
            response = requests.get(
                f"{endpoint}/test-sessions/master",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    self.load_session_data(data)
                    mode_text = "MOCKUP_MASTER" if self.mode == "mockup" else "TEAM_MASTER"
                    self.loaded_filename = f"{mode_text} (from database)"
                    self.loaded_file_label.config(text=f"📂 {self.loaded_filename}")
                    
                    completed = sum(1 for t in self.test_cases if t.status != "Not Started")
                    messagebox.showinfo(
                        "Success",
                        f"✅ Loaded {mode_text}\n\n"
                        f"Last updated: {data.get('test_date', 'Unknown')}\n"
                        f"Tests completed: {completed}/{len(self.test_cases)}"
                    )
                else:
                    # Empty response - no data yet (first time use)
                    mode_text = "MOCKUP_MASTER" if self.mode == "mockup" else "TEAM_MASTER"
                    messagebox.showinfo(
                        "No Data Yet",
                        f"✅ Connected to database successfully!\n\n"
                        f"No {mode_text} data found yet.\n"
                        f"This is normal for first-time use.\n\n"
                        f"Start testing and save to create the first entry!"
                    )
            elif response.status_code == 404:
                # Endpoint not found - offer to load from file instead
                mode_text = "MOCKUP_MASTER" if self.mode == "mockup" else "TEAM_MASTER"
                response_msg = messagebox.askyesno(
                    "Database Endpoint Not Available",
                    f"⚠️ The testing database endpoint is not available.\n\n"
                    f"Status: 404 Not Found\n"
                    f"Endpoint: {endpoint}/test-sessions/master\n\n"
                    f"The backend testing API endpoint has not been implemented yet.\n\n"
                    f"Would you like to load from a file instead?\n\n"
                    f"• Yes - Load from JSON file\n"
                    f"• No - Cancel"
                )
                if response_msg:
                    # Fallback to file load
                    self.load_progress()
            else:
                # Other HTTP errors
                error_detail = response.text
                try:
                    error_json = response.json()
                    if "detail" in error_json:
                        error_detail = error_json["detail"]
                except:
                    pass
                
                response_msg = messagebox.askyesno(
                    "Database Load Failed",
                    f"❌ Failed to load from database:\n\n"
                    f"Status: {response.status_code}\n"
                    f"Error: {error_detail}\n\n"
                    f"Would you like to load from a file instead?\n\n"
                    f"• Yes - Load from JSON file\n"
                    f"• No - Cancel"
                )
                if response_msg:
                    # Fallback to file load
                    self.load_progress()
        except requests.exceptions.ConnectionError:
            response_msg = messagebox.askyesno(
                "Connection Error",
                "❌ Could not connect to backend server!\n\n"
                "The backend testing API endpoint may not be available.\n\n"
                "Would you like to load from a file instead?\n\n"
                "• Yes - Load from JSON file\n"
                "• No - Cancel"
            )
            if response_msg:
                # Fallback to file load
                self.load_progress()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {str(e)}")
    
    def load_session_data(self, data):
        """Load session data into the application (works for both file and database)."""
        # Load tester info
        self.tester_entry.delete(0, tk.END)
        self.tester_entry.insert(0, data.get("tester_name", ""))
        self.browser_combo.set(data.get("browser", "Chrome"))
        
        # Load test cases
        for test_data in data.get("test_cases", []):
            for test in self.test_cases:
                if test.id == test_data["test_id"]:
                    test.status = test_data.get("status", "Not Started")
                    test.actual_results = test_data.get("actual_results", "")
                    test.notes = test_data.get("notes", "")
                    test.tested_date = test_data.get("tested_date", "")
                    break
        
        # Load bugs
        self.bugs = []
        for bug_data in data.get("bugs", []):
            bug = Bug(
                bug_id=bug_data.get("bug_id", ""),
                test_id=bug_data.get("test_id", ""),
                severity=bug_data.get("severity", "Medium"),
                description=bug_data.get("description", ""),
                steps_to_reproduce=bug_data.get("steps_to_reproduce", ""),
                expected=bug_data.get("expected", ""),
                actual=bug_data.get("actual", "")
            )
            bug.reported_by = bug_data.get("reported_by", "")
            bug.reported_date = bug_data.get("reported_date", "")
            self.bugs.append(bug)
        
        # Update bug counter
        if self.bugs:
            max_bug_num = max([int(bug.bug_id.split('-')[1]) for bug in self.bugs if '-' in bug.bug_id], default=0)
            self.bug_counter = max_bug_num + 1
        
        # Refresh UI
        self.populate_tree()
        self.update_progress()
        
        if self.current_test:
            self.display_test(self.current_test)
        
        # Reset unsaved changes flag
        self.has_unsaved_changes = False
    
    # ========================================================================
    # END DATABASE METHODS
    # ========================================================================
    
    def export_report(self):
        """Export testing report to markdown."""
        # Save current test first
        if self.current_test:
            self.save_current_test()
        
        # Create results directory if it doesn't exist
        RESULTS_DIR.mkdir(exist_ok=True)
        
        # Ask for filename (with timestamp)
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialdir=str(RESULTS_DIR),
            initialfile=f"test_report_{self.tester_entry.get() or 'tester'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write("# TalentNest Testing Report\n\n")
                f.write(f"**Tester:** {self.tester_info.get('name', 'N/A')}\n\n")
                f.write(f"**Browser:** {self.tester_info.get('browser', 'N/A')}\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                
                # Summary
                total = len(self.test_cases)
                passed = sum(1 for test in self.test_cases if test.status == "Pass")
                failed = sum(1 for test in self.test_cases if test.status == "Fail")
                blocked = sum(1 for test in self.test_cases if test.status == "Blocked")
                not_started = sum(1 for test in self.test_cases if test.status == "Not Started")
                
                f.write("## Summary\n\n")
                f.write(f"- **Total Test Cases:** {total}\n")
                f.write(f"- **Passed:** {passed} ✅\n")
                f.write(f"- **Failed:** {failed} ❌\n")
                f.write(f"- **Blocked:** {blocked} 🚫\n")
                f.write(f"- **Not Started:** {not_started} ⬜\n")
                
                if total > 0:
                    pass_rate = (passed / total * 100)
                    f.write(f"- **Pass Rate:** {pass_rate:.1f}%\n")
                
                f.write("\n---\n\n")
                
                # Test cases by section
                sections = {}
                for test in self.test_cases:
                    if test.section not in sections:
                        sections[test.section] = []
                    sections[test.section].append(test)
                
                for section, tests in sections.items():
                    f.write(f"## {section}\n\n")
                    
                    for test in tests:
                        icon = self.get_status_icon(test.status)
                        f.write(f"### {icon} Test {test.id}: {test.title}\n\n")
                        f.write(f"**Status:** {test.status}\n\n")
                        f.write(f"**Description:** {test.description}\n\n")
                        
                        if test.actual_results:
                            f.write(f"**Actual Results:**\n```\n{test.actual_results}\n```\n\n")
                        
                        if test.notes:
                            f.write(f"**Notes:** {test.notes}\n\n")
                        
                        if test.tested_by:
                            f.write(f"**Tested By:** {test.tested_by}\n\n")
                        
                        if test.tested_date:
                            f.write(f"**Tested Date:** {test.tested_date}\n\n")
                        
                        f.write("---\n\n")
            
            messagebox.showinfo("Success", f"Report exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not export report:\n{str(e)}")
    
    def report_bug(self):
        """Open bug reporting dialog."""
        if not self.current_test:
            messagebox.showwarning("Warning", "Please select a test case first.")
            return
        
        # Create bug report dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Report Bug - Test {self.current_test.id}")
        dialog.geometry("700x700")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Bug ID (auto-generated)
        ttk.Label(main_frame, text="Bug ID:", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        bug_id = f"BUG-{self.bug_counter:03d}"
        ttk.Label(main_frame, text=bug_id, foreground="blue").grid(
            row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Test ID
        ttk.Label(main_frame, text="Test Case:", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        ttk.Label(main_frame, text=f"{self.current_test.id}: {self.current_test.title}").grid(
            row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Bug Title
        ttk.Label(main_frame, text="Bug Title:*", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        title_entry = ttk.Entry(main_frame, width=50)
        title_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Severity
        ttk.Label(main_frame, text="Severity:*", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        severity_frame = ttk.Frame(main_frame)
        severity_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        severity_var = tk.StringVar(value="Medium")
        severities = ["Critical", "High", "Medium", "Low"]
        for i, sev in enumerate(severities):
            ttk.Radiobutton(severity_frame, text=sev, variable=severity_var, value=sev).grid(
                row=0, column=i, padx=5)
        row += 1
        
        # Priority
        ttk.Label(main_frame, text="Priority:*", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        priority_frame = ttk.Frame(main_frame)
        priority_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        priority_var = tk.StringVar(value="P2")
        priorities = ["P0", "P1", "P2", "P3"]
        for i, pri in enumerate(priorities):
            ttk.Radiobutton(priority_frame, text=pri, variable=priority_var, value=pri).grid(
                row=0, column=i, padx=5)
        row += 1
        
        # Description
        ttk.Label(main_frame, text="Description:*", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=(tk.W, tk.N), pady=5)
        description_text = scrolledtext.ScrolledText(main_frame, height=4, wrap=tk.WORD)
        description_text.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Steps to Reproduce
        ttk.Label(main_frame, text="Steps to Reproduce:*", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=(tk.W, tk.N), pady=5)
        steps_text = scrolledtext.ScrolledText(main_frame, height=4, wrap=tk.WORD)
        steps_text.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        # Pre-fill with test steps
        steps_text.insert(1.0, "\n".join(f"{i}. {step}" for i, step in enumerate(self.current_test.steps, 1)))
        row += 1
        
        # Expected Behavior
        ttk.Label(main_frame, text="Expected Behavior:*", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=(tk.W, tk.N), pady=5)
        expected_text = scrolledtext.ScrolledText(main_frame, height=3, wrap=tk.WORD)
        expected_text.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Actual Behavior
        ttk.Label(main_frame, text="Actual Behavior:*", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=(tk.W, tk.N), pady=5)
        actual_text = scrolledtext.ScrolledText(main_frame, height=3, wrap=tk.WORD)
        actual_text.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        # Pre-fill with actual results if available
        if self.current_test.actual_results:
            actual_text.insert(1.0, self.current_test.actual_results)
        row += 1
        
        # Screenshot/Attachment
        ttk.Label(main_frame, text="Screenshot:", font=("Arial", 10, "bold")).grid(
            row=row, column=0, sticky=tk.W, pady=5)
        screenshot_entry = ttk.Entry(main_frame, width=50)
        screenshot_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        def save_bug():
            # Validate
            if not title_entry.get().strip():
                messagebox.showwarning("Validation Error", "Bug title is required.")
                return
            if not description_text.get(1.0, tk.END).strip():
                messagebox.showwarning("Validation Error", "Description is required.")
                return
            
            # Create bug
            bug = Bug(
                bug_id=bug_id,
                test_id=self.current_test.id,
                title=title_entry.get().strip(),
                severity=severity_var.get(),
                priority=priority_var.get(),
                description=description_text.get(1.0, tk.END).strip(),
                steps_to_reproduce=steps_text.get(1.0, tk.END).strip(),
                expected=expected_text.get(1.0, tk.END).strip(),
                actual=actual_text.get(1.0, tk.END).strip(),
                environment=f"Browser: {self.tester_info.get('browser', 'N/A')}",
                screenshot=screenshot_entry.get().strip()
            )
            bug.reported_by = self.tester_entry.get()
            bug.reported_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Add to bugs list
            self.bugs.append(bug)
            self.bug_counter += 1
            
            # Add bug ID to test case
            if bug_id not in self.current_test.bugs:
                self.current_test.bugs.append(bug_id)
            
            # Update bugs label
            self.update_bugs_label()
            
            # Close dialog
            dialog.destroy()
            
            messagebox.showinfo("Success", f"Bug {bug_id} reported successfully!")
        
        ttk.Button(button_frame, text="Save Bug", command=save_bug).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).grid(row=0, column=1, padx=5)
    
    def view_bugs(self):
        """View all bugs."""
        if not self.bugs:
            messagebox.showinfo("No Bugs", "No bugs have been reported yet.")
            return
        
        # Create bugs view dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Bug Reports")
        dialog.geometry("900x600")
        dialog.transient(self.root)
        
        # Main frame
        main_frame = ttk.Frame(dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Create treeview
        columns = ("Bug ID", "Test ID", "Title", "Severity", "Priority", "Reported By")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)
        
        # Configure columns
        tree.column("Bug ID", width=80)
        tree.column("Test ID", width=60)
        tree.column("Title", width=300)
        tree.column("Severity", width=80)
        tree.column("Priority", width=60)
        tree.column("Reported By", width=100)
        
        # Configure headings
        for col in columns:
            tree.heading(col, text=col)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Populate tree
        for bug in self.bugs:
            tree.insert("", "end", values=(
                bug.bug_id,
                bug.test_id,
                bug.title,
                bug.severity,
                bug.priority,
                bug.reported_by
            ))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Export Bugs", command=self.export_bugs).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Close", command=dialog.destroy).grid(row=0, column=1, padx=5)
    
    def update_bugs_label(self):
        """Update the bugs label for current test."""
        if not self.current_test:
            return
        
        bug_count = len(self.current_test.bugs)
        if bug_count == 0:
            self.bugs_label.config(text="No bugs reported", foreground="green")
        else:
            bug_ids = ", ".join(self.current_test.bugs)
            self.bugs_label.config(text=f"{bug_count} bug(s): {bug_ids}", foreground="red")
    
    def export_bugs(self):
        """Export all bugs to markdown."""
        if not self.bugs:
            messagebox.showinfo("No Bugs", "No bugs to export.")
            return
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialfile=f"bug_report_{self.tester_entry.get() or 'tester'}_{datetime.now().strftime('%Y%m%d')}.md"
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write("# Bug Report - TalentNest Job Portal\n\n")
                f.write(f"**Reported By:** {self.tester_info.get('name', 'N/A')}\n\n")
                f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                
                # Summary
                f.write("## Summary\n\n")
                f.write(f"**Total Bugs:** {len(self.bugs)}\n\n")
                
                critical = sum(1 for bug in self.bugs if bug.severity == "Critical")
                high = sum(1 for bug in self.bugs if bug.severity == "High")
                medium = sum(1 for bug in self.bugs if bug.severity == "Medium")
                low = sum(1 for bug in self.bugs if bug.severity == "Low")
                
                f.write(f"- **Critical:** {critical} 🔴\n")
                f.write(f"- **High:** {high} 🟠\n")
                f.write(f"- **Medium:** {medium} 🟡\n")
                f.write(f"- **Low:** {low} 🟢\n\n")
                
                f.write("---\n\n")
                
                # Bug details
                for bug in self.bugs:
                    f.write(f"## {bug.bug_id}: {bug.title}\n\n")
                    f.write(f"**Test Case:** {bug.test_id}\n\n")
                    f.write(f"**Severity:** {bug.severity} | **Priority:** {bug.priority}\n\n")
                    f.write(f"**Reported By:** {bug.reported_by} on {bug.reported_date}\n\n")
                    
                    f.write(f"### Description\n\n{bug.description}\n\n")
                    
                    f.write(f"### Steps to Reproduce\n\n```\n{bug.steps_to_reproduce}\n```\n\n")
                    
                    f.write(f"### Expected Behavior\n\n{bug.expected_behavior}\n\n")
                    
                    f.write(f"### Actual Behavior\n\n{bug.actual_behavior}\n\n")
                    
                    if bug.environment:
                        f.write(f"### Environment\n\n{bug.environment}\n\n")
                    
                    if bug.screenshot:
                        f.write(f"### Screenshot\n\n{bug.screenshot}\n\n")
                    
                    f.write("---\n\n")
            
            messagebox.showinfo("Success", f"Bug report exported to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not export bug report:\n{str(e)}")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = TestingTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

