"""
TalentNest Testing Tracker - GUI Application
A standalone GUI tool for tracking manual testing progress.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
from datetime import datetime
from pathlib import Path


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
    
    def __init__(self, root):
        self.root = root
        self.root.title("TalentNest Testing Tracker")
        self.root.geometry("1200x800")
        
        # Test data
        self.test_cases = self.load_test_cases()
        self.current_test = None
        self.tester_name = ""
        self.tester_info = {}
        self.bugs = []  # List of all bugs
        self.bug_counter = 1  # Auto-increment bug ID
        
        # Setup UI
        self.setup_ui()
        self.load_tester_info()
        
    def load_test_cases(self):
        """Load all test cases."""
        test_cases = []
        
        # Authentication & Authorization
        test_cases.extend([
            TestCase("1.1", "Authentication", "User Registration (Job Seeker)",
                    "Verify job seeker can register successfully",
                    ["Navigate to signup", "Select Job Seeker role", "Fill form", "Submit"]),
            TestCase("1.2", "Authentication", "User Registration (Employer)",
                    "Verify employer can register successfully",
                    ["Navigate to signup", "Select Employer role", "Fill form", "Submit"]),
            TestCase("1.3", "Authentication", "User Login",
                    "Verify users can log in with valid credentials",
                    ["Navigate to login", "Enter credentials", "Click login"]),
            TestCase("1.4", "Authentication", "Login with Invalid Credentials",
                    "Verify proper error handling for invalid login",
                    ["Navigate to login", "Enter invalid credentials", "Click login"]),
            TestCase("1.5", "Authentication", "Logout",
                    "Verify users can log out successfully",
                    ["Log in", "Click logout", "Verify redirect"]),
            TestCase("1.6", "Authentication", "Protected Routes",
                    "Verify unauthorized users cannot access protected routes",
                    ["Log out", "Try to access protected URLs", "Verify redirect"]),
        ])
        
        # Job Seeker Features
        test_cases.extend([
            TestCase("2.1", "Job Seeker", "Browse Jobs (Unauthenticated)",
                    "Verify anyone can browse job listings",
                    ["Navigate to jobs page", "View job listings"]),
            TestCase("2.2", "Job Seeker", "Job Search and Filters",
                    "Verify job search and filtering functionality",
                    ["Search by keyword", "Filter by location", "Filter by type"]),
            TestCase("2.3", "Job Seeker", "View Job Details",
                    "Verify job detail page displays all information",
                    ["Click on job listing", "Review all details"]),
            TestCase("2.4", "Job Seeker", "Apply for a Job",
                    "Verify job seeker can apply for a job",
                    ["Log in", "Navigate to job", "Click Apply", "Fill form", "Submit"]),
            TestCase("2.5", "Job Seeker", "Upload Resume",
                    "Verify resume upload and parsing functionality",
                    ["Log in", "Navigate to profile", "Upload resume", "Verify parsing"]),
            TestCase("2.6", "Job Seeker", "View My Applications",
                    "Verify job seeker can view their application history",
                    ["Log in", "Navigate to My Applications", "Review list"]),
            TestCase("2.7", "Job Seeker", "Update Profile",
                    "Verify job seeker can update their profile",
                    ["Log in", "Navigate to profile", "Update fields", "Save"]),
        ])
        
        # Employer Features
        test_cases.extend([
            TestCase("3.1", "Employer", "View Employer Dashboard",
                    "Verify employer dashboard displays relevant information",
                    ["Log in as employer", "View dashboard metrics"]),
            TestCase("3.2", "Employer", "Create Job Posting",
                    "Verify employer can create a new job posting",
                    ["Log in", "Navigate to Post Job", "Fill form", "Publish"]),
            TestCase("3.3", "Employer", "Edit Job Posting",
                    "Verify employer can edit existing job postings",
                    ["Log in", "Navigate to My Jobs", "Click Edit", "Modify", "Save"]),
            TestCase("3.4", "Employer", "Close/Archive Job Posting",
                    "Verify employer can close or archive job postings",
                    ["Log in", "Navigate to My Jobs", "Click Close", "Confirm"]),
            TestCase("3.5", "Employer", "View Applications for a Job",
                    "Verify employer can view all applications for a specific job",
                    ["Log in", "Navigate to job", "Click View Applications"]),
            TestCase("3.6", "Employer", "Review Application Details",
                    "Verify employer can view detailed application information",
                    ["Log in", "Navigate to applications", "Click on application"]),
            TestCase("3.7", "Employer", "Shortlist Candidate",
                    "Verify employer can shortlist candidates",
                    ["Log in", "Navigate to application", "Click Shortlist"]),
            TestCase("3.8", "Employer", "Reject Candidate",
                    "Verify employer can reject candidates with reason",
                    ["Log in", "Navigate to application", "Click Reject", "Enter reason"]),
            TestCase("3.9", "Employer", "Add Employer Notes",
                    "Verify employer can add private notes to applications",
                    ["Log in", "Navigate to application", "Add note", "Save"]),
            TestCase("3.10", "Employer", "Update Company Profile",
                    "Verify employer can update company information",
                    ["Log in", "Navigate to company profile", "Update fields", "Save"]),
        ])
        
        # AI Features
        test_cases.extend([
            TestCase("4.1", "AI Features", "AI Resume Parsing",
                    "Verify AI can parse uploaded resumes",
                    ["Log in", "Upload resume", "Wait for parsing", "Review extracted data"]),
            TestCase("4.2", "AI Features", "AI Assistant Chat",
                    "Verify AI assistant provides helpful responses",
                    ["Log in", "Navigate to AI Assistant", "Ask questions", "Review responses"]),
            TestCase("4.3", "AI Features", "AI Cover Letter Generation",
                    "Verify AI can generate personalized cover letters",
                    ["Log in", "Apply to job", "Click Generate Cover Letter", "Review"]),
            TestCase("4.4", "AI Features", "AI Job Recommendations",
                    "Verify AI recommends relevant jobs to job seekers",
                    ["Log in", "View dashboard", "Review recommended jobs"]),
        ])
        
        # Edge Cases & Error Handling
        test_cases.extend([
            TestCase("5.1", "Edge Cases", "Form Validation",
                    "Verify all forms have proper validation",
                    ["Test empty fields", "Test invalid formats", "Test mismatches"]),
            TestCase("5.2", "Edge Cases", "Network Error Handling",
                    "Verify app handles network errors gracefully",
                    ["Go offline", "Try actions", "Go online", "Retry"]),
            TestCase("5.3", "Edge Cases", "Session Expiration",
                    "Verify app handles expired JWT tokens properly",
                    ["Wait for token expiry", "Try action", "Verify redirect"]),
            TestCase("5.4", "Edge Cases", "Large File Upload",
                    "Verify file upload handles large files appropriately",
                    ["Try uploading large file", "Verify error message"]),
            TestCase("5.5", "Edge Cases", "SQL Injection / XSS Prevention",
                    "Verify app is protected against common security vulnerabilities",
                    ["Try malicious input", "Verify sanitization"]),
            TestCase("5.6", "Edge Cases", "Concurrent Actions",
                    "Verify app handles concurrent user actions",
                    ["Open two tabs", "Perform same action", "Verify no conflicts"]),
            TestCase("5.7", "Edge Cases", "Duplicate Application Prevention",
                    "Verify users cannot apply to the same job twice",
                    ["Apply to job", "Try to apply again", "Verify prevention"]),
        ])
        
        # Responsive Design
        test_cases.extend([
            TestCase("6.1", "Responsive", "Mobile Responsiveness (375px)",
                    "Verify app works well on mobile devices",
                    ["Set width to 375px", "Navigate through pages", "Test functionality"]),
            TestCase("6.2", "Responsive", "Tablet Responsiveness (768px)",
                    "Verify app works well on tablet devices",
                    ["Set width to 768px", "Navigate through pages", "Test functionality"]),
            TestCase("6.3", "Responsive", "Desktop Responsiveness (1920px)",
                    "Verify app looks good on large screens",
                    ["Set to full screen", "Navigate through pages", "Check layout"]),
        ])
        
        # Performance
        test_cases.extend([
            TestCase("7.1", "Performance", "Page Load Time",
                    "Verify pages load within acceptable time",
                    ["Clear cache", "Navigate to pages", "Measure load times"]),
            TestCase("7.2", "Performance", "Search Performance",
                    "Verify search returns results quickly",
                    ["Perform various searches", "Measure response time"]),
            TestCase("7.3", "Performance", "Large Dataset Handling",
                    "Verify app handles large amounts of data",
                    ["Test with 1000+ jobs", "Test pagination", "Test filtering"]),
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
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Header
        self.create_header(main_container)
        
        # Left panel - Test list
        self.create_test_list(main_container)
        
        # Right panel - Test details
        self.create_test_details(main_container)
        
        # Bottom panel - Actions
        self.create_actions(main_container)
        
    def create_header(self, parent):
        """Create header section."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, text="TalentNest Testing Tracker",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Tester info
        info_frame = ttk.Frame(header_frame)
        info_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(info_frame, text="Tester:").grid(row=0, column=0, padx=5)
        self.tester_entry = ttk.Entry(info_frame, width=20)
        self.tester_entry.grid(row=0, column=1, padx=5)
        self.tester_entry.bind('<FocusOut>', self.save_tester_info)
        
        ttk.Label(info_frame, text="Browser:").grid(row=0, column=2, padx=5)
        self.browser_combo = ttk.Combobox(info_frame, width=15,
                                         values=["Chrome", "Firefox", "Safari", "Edge"])
        self.browser_combo.grid(row=0, column=3, padx=5)
        self.browser_combo.bind('<<ComboboxSelected>>', self.save_tester_info)
        
        # Progress
        progress_frame = ttk.Frame(header_frame)
        progress_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.progress_label = ttk.Label(progress_frame, text="Progress: 0/0 (0%)")
        self.progress_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        self.progress_bar.grid(row=0, column=1, padx=10)
        
    def create_test_list(self, parent):
        """Create test list section."""
        list_frame = ttk.LabelFrame(parent, text="Test Cases", padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(1, weight=1)
        
        # Jump to section dropdown
        jump_frame = ttk.Frame(list_frame)
        jump_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        ttk.Label(jump_frame, text="Jump to:").grid(row=0, column=0, padx=(0, 5))
        self.section_var = tk.StringVar()
        self.section_combo = ttk.Combobox(jump_frame, textvariable=self.section_var, 
                                         state="readonly", width=30)
        self.section_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.section_combo.bind('<<ComboboxSelected>>', self.on_section_jump)
        jump_frame.columnconfigure(1, weight=1)
        
        # Create treeview
        columns = ("ID", "Section", "Title", "Status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings", height=25)
        
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
        
        # Populate section dropdown
        section_names = list(sections.keys())
        self.section_combo['values'] = section_names
        
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
        
        # Expand all
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
        details_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        details_frame.columnconfigure(0, weight=1)
        details_frame.rowconfigure(4, weight=1)
        
        # Test ID and Title
        self.test_id_label = ttk.Label(details_frame, text="Select a test case",
                                       font=("Arial", 12, "bold"))
        self.test_id_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Description
        ttk.Label(details_frame, text="Description:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.description_label = ttk.Label(details_frame, text="", wraplength=600)
        self.description_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        # Steps
        ttk.Label(details_frame, text="Steps:", font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky=tk.W)
        self.steps_text = scrolledtext.ScrolledText(details_frame, height=6, wrap=tk.WORD)
        self.steps_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.steps_text.config(state=tk.DISABLED)
        
        # Status
        status_frame = ttk.Frame(details_frame)
        status_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(status_frame, text="Status:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.status_var = tk.StringVar(value="Not Started")
        statuses = ["Not Started", "Pass", "Fail", "Blocked"]
        for i, status in enumerate(statuses):
            ttk.Radiobutton(status_frame, text=status, variable=self.status_var,
                          value=status, command=self.on_status_change).grid(
                              row=0, column=i+1, padx=5)
        
        # Actual Results
        ttk.Label(details_frame, text="Actual Results:", font=("Arial", 10, "bold")).grid(
            row=6, column=0, sticky=tk.W)
        self.results_text = scrolledtext.ScrolledText(details_frame, height=6, wrap=tk.WORD)
        self.results_text.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Notes
        ttk.Label(details_frame, text="Notes:", font=("Arial", 10, "bold")).grid(
            row=8, column=0, sticky=tk.W)
        self.notes_text = scrolledtext.ScrolledText(details_frame, height=4, wrap=tk.WORD)
        self.notes_text.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
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
        actions_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Left side buttons
        left_frame = ttk.Frame(actions_frame)
        left_frame.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Button(left_frame, text="Save Progress", command=self.save_progress).grid(
            row=0, column=0, padx=5)
        ttk.Button(left_frame, text="Load Progress", command=self.load_progress).grid(
            row=0, column=1, padx=5)
        ttk.Button(left_frame, text="Export Report", command=self.export_report).grid(
            row=0, column=2, padx=5)
        
        # Right side buttons
        right_frame = ttk.Frame(actions_frame)
        right_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(right_frame, text="Previous", command=self.previous_test).grid(
            row=0, column=0, padx=5)
        ttk.Button(right_frame, text="Next", command=self.next_test).grid(
            row=0, column=1, padx=5)
        
        actions_frame.columnconfigure(1, weight=1)
    
    def on_test_select(self, event):
        """Handle test selection."""
        selection = self.tree.selection()
        if not selection:
            return
        
        # Save current test if any
        if self.current_test:
            self.save_current_test()
        
        # Get selected item
        item = selection[0]
        values = self.tree.item(item, 'values')
        tags = self.tree.item(item, 'tags')
        
        # Check if it's a section header
        if not values[0] and "section" in tags:
            # Section header clicked - select first test in that section
            children = self.tree.get_children(item)
            if children:
                first_child = children[0]
                self.tree.selection_set(first_child)
                self.tree.see(first_child)
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
    
    def on_section_jump(self, event):
        """Handle section jump from dropdown."""
        section = self.section_var.get()
        if section and section in self.section_items:
            section_item = self.section_items[section]
            # Get first test in section
            children = self.tree.get_children(section_item)
            if children:
                first_child = children[0]
                self.tree.selection_set(first_child)
                self.tree.see(first_child)
                # Trigger display
                child_values = self.tree.item(first_child, 'values')
                test_id = child_values[0]
                for test in self.test_cases:
                    if test.id == test_id:
                        self.current_test = test
                        self.display_test(test)
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
        
        # Update tree
        self.populate_tree()
        self.update_progress()
    
    def on_status_change(self):
        """Handle status change."""
        if self.current_test:
            self.save_current_test()
    
    def update_progress(self):
        """Update progress bar and label."""
        total = len(self.test_cases)
        completed = sum(1 for test in self.test_cases if test.status != "Not Started")
        percentage = (completed / total * 100) if total > 0 else 0
        
        self.progress_label.config(text=f"Progress: {completed}/{total} ({percentage:.1f}%)")
        self.progress_bar['value'] = percentage
    
    def previous_test(self):
        """Navigate to previous test."""
        if not self.current_test:
            return
        
        current_index = self.test_cases.index(self.current_test)
        if current_index > 0:
            self.select_test(self.test_cases[current_index - 1])
    
    def next_test(self):
        """Navigate to next test."""
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
    
    def save_tester_info(self, event=None):
        """Save tester information."""
        self.tester_info = {
            "name": self.tester_entry.get(),
            "browser": self.browser_combo.get(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    
    def load_tester_info(self):
        """Load tester information from previous session."""
        try:
            info_file = Path("tester_info.json")
            if info_file.exists():
                with open(info_file, 'r') as f:
                    self.tester_info = json.load(f)
                    self.tester_entry.insert(0, self.tester_info.get("name", ""))
                    self.browser_combo.set(self.tester_info.get("browser", "Chrome"))
        except Exception as e:
            print(f"Could not load tester info: {e}")
    
    def save_progress(self):
        """Save testing progress to file."""
        # Save current test first
        if self.current_test:
            self.save_current_test()
        
        # Save tester info
        self.save_tester_info()
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=f"test_progress_{self.tester_entry.get() or 'tester'}_{datetime.now().strftime('%Y%m%d')}.json"
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
            
            messagebox.showinfo("Success", f"Progress saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save progress:\n{str(e)}")
    
    def load_progress(self):
        """Load testing progress from file."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
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
            
            messagebox.showinfo("Success", f"Progress loaded from:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load progress:\n{str(e)}")
    
    def export_report(self):
        """Export testing report to markdown."""
        # Save current test first
        if self.current_test:
            self.save_current_test()
        
        # Ask for filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            initialfile=f"test_report_{self.tester_entry.get() or 'tester'}_{datetime.now().strftime('%Y%m%d')}.md"
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

