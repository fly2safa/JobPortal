# Manual Testing Guide - TalentNest Job Portal

## Overview

This guide provides step-by-step instructions for manually testing all features of the TalentNest Job Portal application. Follow each test case carefully and document any bugs or issues found.

---

## Table of Contents

1. [Pre-Testing Setup](#pre-testing-setup)
2. [Authentication & Authorization](#authentication--authorization)
3. [Job Seeker Features](#job-seeker-features)
4. [Employer Features](#employer-features)
5. [AI Features](#ai-features)
6. [Edge Cases & Error Handling](#edge-cases--error-handling)
7. [Responsive Design Testing](#responsive-design-testing)
8. [Performance Testing](#performance-testing)
9. [Bug Reporting Template](#bug-reporting-template)

---

## Pre-Testing Setup

### Prerequisites

Before starting testing, ensure:

- [ ] Backend server is running on `http://localhost:8000`
- [ ] Frontend server is running on `http://localhost:3000`
- [ ] MongoDB Atlas connection is active
- [ ] Database has been seeded with test data (optional)
- [ ] You have cleared browser cache and cookies
- [ ] You're using a modern browser (Chrome, Firefox, Safari, or Edge)

### Test Accounts

Create or use these test accounts:

**Job Seeker Account:**
- Email: `jobseeker@test.com`
- Password: `Test123!`
- Role: Job Seeker

**Employer Account:**
- Email: `employer@test.com`
- Password: `Test123!`
- Role: Employer
- Company: Test Company Inc.

**Admin Account (if applicable):**
- Email: `admin@test.com`
- Password: `Admin123!`
- Role: Admin

### Testing Environment

- **Browser:** Chrome (latest version)
- **Screen Resolutions to Test:**
  - Desktop: 1920x1080
  - Tablet: 768x1024
  - Mobile: 375x667 (iPhone SE)

---

## Authentication & Authorization

### Test Case 1.1: User Registration (Job Seeker)

**Objective:** Verify job seeker can register successfully

**Steps:**
1. Navigate to `http://localhost:3000`
2. Click "Sign Up" or "Register" button
3. Select "Job Seeker" role
4. Fill in the registration form:
   - First Name: `John`
   - Last Name: `Doe`
   - Email: `john.doe@test.com`
   - Password: `Test123!`
   - Confirm Password: `Test123!`
5. Click "Register" or "Sign Up" button

**Expected Results:**
- [ ] Form validates all fields
- [ ] Password strength indicator shows (if implemented)
- [ ] Registration succeeds with success message
- [ ] User is redirected to dashboard or login page
- [ ] Confirmation email sent (if email is configured)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 1.2: User Registration (Employer)

**Objective:** Verify employer can register successfully

**Steps:**
1. Navigate to `http://localhost:3000`
2. Click "Sign Up" or "Register" button
3. Select "Employer" role
4. Fill in the registration form:
   - First Name: `Jane`
   - Last Name: `Smith`
   - Email: `jane.smith@test.com`
   - Password: `Test123!`
   - Company Name: `Tech Innovations Inc.`
   - Job Title: `HR Manager`
5. Click "Register" or "Sign Up" button

**Expected Results:**
- [ ] Form validates all fields
- [ ] Company information fields appear for employer
- [ ] Registration succeeds with success message
- [ ] User is redirected to employer dashboard
- [ ] Company profile is created

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 1.3: User Login

**Objective:** Verify users can log in with valid credentials

**Steps:**
1. Navigate to `http://localhost:3000`
2. Click "Login" or "Sign In" button
3. Enter credentials:
   - Email: `jobseeker@test.com`
   - Password: `Test123!`
4. Click "Login" button

**Expected Results:**
- [ ] Login succeeds with success message
- [ ] User is redirected to appropriate dashboard (job seeker dashboard)
- [ ] User's name appears in header/navigation
- [ ] JWT token is stored (check browser dev tools → Application → Local Storage)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 1.4: Login with Invalid Credentials

**Objective:** Verify proper error handling for invalid login

**Steps:**
1. Navigate to login page
2. Enter invalid credentials:
   - Email: `invalid@test.com`
   - Password: `WrongPassword123!`
3. Click "Login" button

**Expected Results:**
- [ ] Login fails with appropriate error message
- [ ] Error message is user-friendly (e.g., "Invalid email or password")
- [ ] No sensitive information leaked in error message
- [ ] User remains on login page

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 1.5: Logout

**Objective:** Verify users can log out successfully

**Steps:**
1. Log in as any user
2. Navigate to user menu (usually top-right corner)
3. Click "Logout" or "Sign Out" button

**Expected Results:**
- [ ] User is logged out successfully
- [ ] Redirected to home page or login page
- [ ] JWT token is removed from local storage
- [ ] Attempting to access protected routes redirects to login

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 1.6: Protected Routes (Authorization)

**Objective:** Verify unauthorized users cannot access protected routes

**Steps:**
1. Log out (or open incognito window)
2. Try to access these URLs directly:
   - `http://localhost:3000/dashboard`
   - `http://localhost:3000/jobs/new`
   - `http://localhost:3000/employer/jobs`

**Expected Results:**
- [ ] User is redirected to login page
- [ ] Appropriate message displayed (e.g., "Please login to continue")
- [ ] After login, user is redirected to originally requested page

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

## Job Seeker Features

### Test Case 2.1: Browse Jobs (Unauthenticated)

**Objective:** Verify anyone can browse job listings

**Steps:**
1. Log out or open incognito window
2. Navigate to `http://localhost:3000` or jobs page
3. View the list of available jobs

**Expected Results:**
- [ ] Job listings are visible
- [ ] Each job shows: title, company, location, salary (if available)
- [ ] Pagination works (if implemented)
- [ ] "Apply" button prompts login

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 2.2: Job Search and Filters

**Objective:** Verify job search and filtering functionality

**Steps:**
1. Navigate to jobs page
2. Test search functionality:
   - Search by keyword: `Python`
   - Search by location: `San Francisco`
3. Test filters:
   - Filter by job type: `Full Time`
   - Filter by experience level: `Mid`
   - Filter by salary range: `$80k - $120k`
   - Filter by remote: `Remote Only`

**Expected Results:**
- [ ] Search returns relevant results
- [ ] Filters narrow down results appropriately
- [ ] Multiple filters can be applied simultaneously
- [ ] "Clear Filters" button resets all filters
- [ ] Results update without page reload (if using client-side filtering)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 2.3: View Job Details

**Objective:** Verify job detail page displays all information

**Steps:**
1. Navigate to jobs page
2. Click on any job listing
3. Review the job detail page

**Expected Results:**
- [ ] All job information is displayed:
  - Job title
  - Company name
  - Location
  - Job type (Full Time, Part Time, etc.)
  - Experience level
  - Salary range
  - Description
  - Requirements
  - Responsibilities
  - Skills required
  - Benefits
  - Application instructions
- [ ] "Apply Now" button is visible
- [ ] Company logo/branding displayed (if available)
- [ ] Posted date shown

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 2.4: Apply for a Job

**Objective:** Verify job seeker can apply for a job

**Steps:**
1. Log in as job seeker
2. Navigate to a job detail page
3. Click "Apply Now" button
4. Fill in the application form:
   - Select resume (upload if needed)
   - Write cover letter (or generate with AI)
   - Add any additional information
5. Click "Submit Application" button

**Expected Results:**
- [ ] Application form opens (modal or new page)
- [ ] Resume can be uploaded (PDF, DOCX)
- [ ] Cover letter field is available
- [ ] Form validates required fields
- [ ] Application submits successfully
- [ ] Success message displayed
- [ ] User cannot apply to the same job twice
- [ ] Email notification sent (if configured)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 2.5: Upload Resume

**Objective:** Verify resume upload and parsing functionality

**Steps:**
1. Log in as job seeker
2. Navigate to profile or resume section
3. Click "Upload Resume" button
4. Select a resume file (PDF or DOCX)
5. Upload the file

**Expected Results:**
- [ ] File upload succeeds
- [ ] Supported formats: PDF, DOCX
- [ ] File size limit enforced (e.g., max 5MB)
- [ ] Resume is parsed automatically (if AI parsing is enabled)
- [ ] Extracted information displayed:
  - Skills
  - Experience years
  - Education
  - Work history summary
- [ ] Parsing confidence score shown (if available)
- [ ] User can view/download uploaded resume

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 2.6: View My Applications

**Objective:** Verify job seeker can view their application history

**Steps:**
1. Log in as job seeker (who has submitted applications)
2. Navigate to "My Applications" page
3. Review the list of applications

**Expected Results:**
- [ ] All submitted applications are listed
- [ ] Each application shows:
  - Job title
  - Company name
  - Application date
  - Current status (Pending, Reviewing, Shortlisted, etc.)
- [ ] Applications can be filtered by status
- [ ] User can view application details
- [ ] User can withdraw application (if status allows)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 2.7: Update Profile

**Objective:** Verify job seeker can update their profile

**Steps:**
1. Log in as job seeker
2. Navigate to profile/settings page
3. Update profile information:
   - Phone number
   - Location
   - Skills (add/remove)
   - Experience years
   - Education
   - Bio
   - LinkedIn URL
   - Portfolio URL
4. Click "Save" or "Update Profile" button

**Expected Results:**
- [ ] All fields are editable
- [ ] Form validates input (e.g., valid URLs, phone format)
- [ ] Changes save successfully
- [ ] Success message displayed
- [ ] Updated information reflects immediately

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

## Employer Features

### Test Case 3.1: View Employer Dashboard

**Objective:** Verify employer dashboard displays relevant information

**Steps:**
1. Log in as employer
2. View the employer dashboard

**Expected Results:**
- [ ] Dashboard shows key metrics:
  - Total jobs posted
  - Active jobs
  - Total applications received
  - Pending applications
- [ ] Quick actions available:
  - Post New Job
  - View Applications
  - Manage Jobs
- [ ] Recent applications listed
- [ ] Charts/graphs for analytics (if implemented)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 3.2: Create Job Posting

**Objective:** Verify employer can create a new job posting

**Steps:**
1. Log in as employer
2. Navigate to "Post a Job" or "Create Job" page
3. Fill in the job posting form:
   - Job Title: `Senior Software Engineer`
   - Description: `[Detailed job description]`
   - Requirements: `[Job requirements]`
   - Responsibilities: `[Job responsibilities]`
   - Location: `San Francisco, CA`
   - Remote: `Yes`
   - Job Type: `Full Time`
   - Experience Level: `Senior`
   - Salary Range: `$120,000 - $180,000`
   - Skills: `Python, FastAPI, React, MongoDB`
   - Benefits: `Health Insurance, 401k, Remote Work`
4. Save as draft or publish immediately

**Expected Results:**
- [ ] All fields are available and functional
- [ ] Form validates required fields
- [ ] Skills can be added/removed (tag input)
- [ ] Salary range validates (min < max)
- [ ] Option to save as draft
- [ ] Option to publish immediately
- [ ] Success message displayed
- [ ] Redirected to job detail or jobs list

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 3.3: Edit Job Posting

**Objective:** Verify employer can edit existing job postings

**Steps:**
1. Log in as employer
2. Navigate to "My Jobs" page
3. Click "Edit" on an existing job
4. Modify some fields (e.g., salary range, description)
5. Click "Save Changes" button

**Expected Results:**
- [ ] Edit form pre-fills with existing data
- [ ] All fields are editable
- [ ] Changes save successfully
- [ ] Success message displayed
- [ ] Updated information reflects immediately

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 3.4: Close/Archive Job Posting

**Objective:** Verify employer can close or archive job postings

**Steps:**
1. Log in as employer
2. Navigate to "My Jobs" page
3. Find an active job
4. Click "Close" or "Archive" button
5. Confirm the action

**Expected Results:**
- [ ] Confirmation dialog appears
- [ ] Job status changes to "Closed" or "Archived"
- [ ] Job no longer appears in public job listings
- [ ] Existing applications remain accessible
- [ ] Success message displayed

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 3.5: View Applications for a Job

**Objective:** Verify employer can view all applications for a specific job

**Steps:**
1. Log in as employer
2. Navigate to "My Jobs" page
3. Click on a job that has applications
4. Click "View Applications" button
5. Review the applications list

**Expected Results:**
- [ ] All applications for the job are listed
- [ ] Application statistics shown:
  - Total applications
  - Pending
  - Reviewing
  - Shortlisted
  - Rejected
- [ ] Each application shows:
  - Applicant name
  - Application date
  - Status
  - Resume (download link)
- [ ] Applications can be filtered by status
- [ ] Applications can be sorted (by date, name, etc.)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 3.6: Review Application Details

**Objective:** Verify employer can view detailed application information

**Steps:**
1. Log in as employer
2. Navigate to applications for a job
3. Click on an individual application
4. Review the application details

**Expected Results:**
- [ ] All application information displayed:
  - Applicant name and contact info
  - Resume (viewable/downloadable)
  - Cover letter
  - Application date
  - Current status
  - Status history
- [ ] Applicant profile information shown:
  - Skills
  - Experience
  - Education
  - LinkedIn/Portfolio links
- [ ] Action buttons available:
  - Shortlist
  - Reject
  - Schedule Interview
  - Add Notes

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 3.7: Shortlist Candidate

**Objective:** Verify employer can shortlist candidates

**Steps:**
1. Log in as employer
2. Navigate to an application
3. Click "Shortlist" button
4. Confirm the action (if confirmation required)

**Expected Results:**
- [ ] Application status changes to "Shortlisted"
- [ ] Status history updated
- [ ] Success message displayed
- [ ] Email notification sent to candidate (if configured)
- [ ] Application appears in "Shortlisted" filter

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 3.8: Reject Candidate

**Objective:** Verify employer can reject candidates with reason

**Steps:**
1. Log in as employer
2. Navigate to an application
3. Click "Reject" button
4. Enter rejection reason (optional or required)
5. Confirm the action

**Expected Results:**
- [ ] Rejection modal/form appears
- [ ] Rejection reason field available
- [ ] Application status changes to "Rejected"
- [ ] Status history updated with reason
- [ ] Success message displayed
- [ ] Email notification sent to candidate (if configured)
- [ ] Application appears in "Rejected" filter

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 3.9: Add Employer Notes

**Objective:** Verify employer can add private notes to applications

**Steps:**
1. Log in as employer
2. Navigate to an application
3. Find the "Notes" or "Employer Notes" section
4. Add a note: `Great candidate, strong Python skills`
5. Save the note

**Expected Results:**
- [ ] Note saves successfully
- [ ] Note is visible only to employer (not candidate)
- [ ] Multiple notes can be added
- [ ] Notes show timestamp and author
- [ ] Notes can be edited/deleted

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 3.10: Update Company Profile

**Objective:** Verify employer can update company information

**Steps:**
1. Log in as employer
2. Navigate to company profile/settings
3. Update company information:
   - Company description
   - Industry
   - Company size
   - Website
   - Locations
   - Social media links
   - Logo (upload)
4. Click "Save Changes" button

**Expected Results:**
- [ ] All fields are editable
- [ ] Form validates input (e.g., valid URLs)
- [ ] Logo can be uploaded (image file)
- [ ] Changes save successfully
- [ ] Success message displayed
- [ ] Updated information reflects on job postings

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

## AI Features

### Test Case 4.1: AI Resume Parsing

**Objective:** Verify AI can parse uploaded resumes

**Steps:**
1. Log in as job seeker
2. Upload a resume (PDF or DOCX)
3. Wait for AI parsing to complete
4. Review extracted information

**Expected Results:**
- [ ] Resume uploads successfully
- [ ] AI parsing completes within reasonable time (< 30 seconds)
- [ ] Extracted information is accurate:
  - Skills
  - Experience years
  - Education
  - Work history
- [ ] Parsing confidence score shown
- [ ] User can edit extracted information
- [ ] Parsing method indicated (algorithmic, AI, or hybrid)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 4.2: AI Assistant Chat

**Objective:** Verify AI assistant provides helpful responses

**Steps:**
1. Log in as job seeker
2. Navigate to AI Assistant page
3. Start a conversation with these prompts:
   - `How do I write a good resume?`
   - `What skills should I learn for a software engineering role?`
   - `How do I prepare for a technical interview?`
4. Review the AI responses

**Expected Results:**
- [ ] Chat interface is user-friendly
- [ ] AI responds within reasonable time (< 10 seconds)
- [ ] Responses are relevant and helpful
- [ ] Conversation history is maintained
- [ ] User can start new conversations
- [ ] Previous conversations are accessible
- [ ] Responses are formatted properly (markdown, lists, etc.)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 4.3: AI Cover Letter Generation

**Objective:** Verify AI can generate personalized cover letters

**Steps:**
1. Log in as job seeker
2. Navigate to a job detail page
3. Click "Apply Now" button
4. In the cover letter section, click "Generate with AI" button
5. Wait for AI to generate cover letter
6. Review the generated cover letter

**Expected Results:**
- [ ] AI generates cover letter within reasonable time (< 15 seconds)
- [ ] Cover letter is personalized:
  - Mentions job title
  - Mentions company name
  - References user's skills and experience
  - Relevant to job description
- [ ] User can regenerate if not satisfied
- [ ] User can edit the generated cover letter
- [ ] User can copy or insert the cover letter

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 4.4: AI Job Recommendations (if implemented)

**Objective:** Verify AI recommends relevant jobs to job seekers

**Steps:**
1. Log in as job seeker with complete profile
2. Navigate to dashboard or "Recommended Jobs" section
3. Review the recommended jobs

**Expected Results:**
- [ ] Recommendations are displayed
- [ ] Recommended jobs match user's:
  - Skills
  - Experience level
  - Location preferences
  - Job type preferences
- [ ] Recommendations are diverse (not all from same company)
- [ ] User can dismiss recommendations
- [ ] Recommendations update based on profile changes

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

## Edge Cases & Error Handling

### Test Case 5.1: Form Validation

**Objective:** Verify all forms have proper validation

**Test these scenarios across all forms:**

**Registration Form:**
- [ ] Empty fields show error messages
- [ ] Invalid email format rejected
- [ ] Weak password rejected
- [ ] Password mismatch detected
- [ ] Duplicate email rejected

**Job Posting Form:**
- [ ] Required fields enforced
- [ ] Salary min < max validation
- [ ] Date validations (closing date > posted date)
- [ ] Character limits enforced

**Application Form:**
- [ ] Resume required
- [ ] File type validation (only PDF/DOCX)
- [ ] File size limit enforced

**Expected Results:**
- [ ] All validation errors are user-friendly
- [ ] Errors appear near the relevant field
- [ ] Multiple errors can be shown simultaneously
- [ ] Errors clear when field is corrected

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 5.2: Network Error Handling

**Objective:** Verify app handles network errors gracefully

**Steps:**
1. Log in to the application
2. Open browser DevTools → Network tab
3. Set network throttling to "Offline"
4. Try to perform actions (search jobs, submit application, etc.)
5. Re-enable network
6. Retry the action

**Expected Results:**
- [ ] Appropriate error message shown when offline
- [ ] No unhandled errors in console
- [ ] App doesn't crash
- [ ] Actions retry successfully when online
- [ ] Loading states shown during requests

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 5.3: Session Expiration

**Objective:** Verify app handles expired JWT tokens properly

**Steps:**
1. Log in to the application
2. Wait for token to expire (or manually delete token from local storage)
3. Try to perform an authenticated action

**Expected Results:**
- [ ] User is redirected to login page
- [ ] Appropriate message shown (e.g., "Session expired, please login again")
- [ ] After re-login, user returns to previous page
- [ ] No data loss

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 5.4: Large File Upload

**Objective:** Verify file upload handles large files appropriately

**Steps:**
1. Log in as job seeker
2. Try to upload a very large resume (> 10MB)
3. Try to upload a resume exactly at the limit (e.g., 5MB)

**Expected Results:**
- [ ] Files over limit are rejected with clear error message
- [ ] Files at or under limit upload successfully
- [ ] Upload progress indicator shown
- [ ] User can cancel upload

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 5.5: SQL Injection / XSS Prevention

**Objective:** Verify app is protected against common security vulnerabilities

**Steps:**
1. Try to inject malicious code in various input fields:
   - Search: `<script>alert('XSS')</script>`
   - Job Title: `'; DROP TABLE jobs; --`
   - Description: `<img src=x onerror=alert('XSS')>`
2. Submit the forms
3. Check if code is executed or stored

**Expected Results:**
- [ ] Malicious code is sanitized/escaped
- [ ] No JavaScript execution from user input
- [ ] No database errors from injection attempts
- [ ] Input is displayed as plain text, not executed

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 5.6: Concurrent Actions

**Objective:** Verify app handles concurrent user actions

**Steps:**
1. Open the same application in two browser tabs
2. Log in as the same user in both tabs
3. In Tab 1: Start editing profile
4. In Tab 2: Update and save profile
5. In Tab 1: Try to save profile

**Expected Results:**
- [ ] No data corruption
- [ ] Appropriate conflict resolution (last write wins, or conflict warning)
- [ ] User is notified of conflicts

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 5.7: Duplicate Application Prevention

**Objective:** Verify users cannot apply to the same job twice

**Steps:**
1. Log in as job seeker
2. Apply to a job
3. Navigate back to the same job
4. Try to apply again

**Expected Results:**
- [ ] "Apply" button is disabled or shows "Already Applied"
- [ ] If user tries to apply again, error message shown
- [ ] Application count doesn't increase

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

## Responsive Design Testing

### Test Case 6.1: Mobile Responsiveness (375px width)

**Objective:** Verify app works well on mobile devices

**Steps:**
1. Open Chrome DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select "iPhone SE" or set width to 375px
4. Navigate through all major pages:
   - Home page
   - Job listings
   - Job details
   - Login/Register
   - Dashboard
   - Profile

**Expected Results:**
- [ ] All content is visible (no horizontal scroll)
- [ ] Navigation menu adapts (hamburger menu)
- [ ] Buttons are touch-friendly (min 44x44px)
- [ ] Forms are usable
- [ ] Images scale appropriately
- [ ] Text is readable (not too small)
- [ ] No overlapping elements

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 6.2: Tablet Responsiveness (768px width)

**Objective:** Verify app works well on tablet devices

**Steps:**
1. Set device width to 768px (iPad)
2. Navigate through all major pages
3. Test both portrait and landscape orientations

**Expected Results:**
- [ ] Layout adapts appropriately
- [ ] Good use of screen space
- [ ] Touch-friendly interface
- [ ] No layout issues

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 6.3: Desktop Responsiveness (1920px width)

**Objective:** Verify app looks good on large screens

**Steps:**
1. Set browser to full screen on 1920x1080 monitor
2. Navigate through all major pages

**Expected Results:**
- [ ] Content is centered or well-distributed
- [ ] No excessive white space
- [ ] Images don't pixelate
- [ ] Text lines aren't too long (max ~75 characters)

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

## Performance Testing

### Test Case 7.1: Page Load Time

**Objective:** Verify pages load within acceptable time

**Steps:**
1. Open Chrome DevTools → Network tab
2. Clear cache (Ctrl+Shift+Delete)
3. Navigate to various pages
4. Record load times

**Expected Results:**
- [ ] Home page loads in < 3 seconds
- [ ] Job listings load in < 3 seconds
- [ ] Dashboard loads in < 3 seconds
- [ ] No unnecessary network requests
- [ ] Images are optimized

**Actual Results:**
```
Page | Load Time | Status
-----|-----------|-------
Home | [X]s | [Pass/Fail]
Jobs | [X]s | [Pass/Fail]
Dashboard | [X]s | [Pass/Fail]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 7.2: Search Performance

**Objective:** Verify search returns results quickly

**Steps:**
1. Navigate to jobs page
2. Perform various searches
3. Measure response time

**Expected Results:**
- [ ] Search results return in < 2 seconds
- [ ] Filters apply quickly
- [ ] No lag when typing in search box
- [ ] Debouncing implemented for live search

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

### Test Case 7.3: Large Dataset Handling

**Objective:** Verify app handles large amounts of data

**Steps:**
1. Create/seed database with large dataset:
   - 1000+ jobs
   - 100+ applications
2. Navigate to job listings
3. Navigate to applications list
4. Test pagination and filtering

**Expected Results:**
- [ ] Pages load without significant delay
- [ ] Pagination works smoothly
- [ ] Filtering doesn't cause lag
- [ ] No browser freezing

**Actual Results:**
```
[Document your findings here]
```

**Status:** ⬜ Pass | ⬜ Fail | ⬜ Blocked

---

## Bug Reporting Template

When you find a bug, document it using this template:

### Bug Report #[Number]

**Title:** [Brief description of the bug]

**Severity:** 
- [ ] Critical (app crashes, data loss)
- [ ] High (major feature broken)
- [ ] Medium (feature partially works)
- [ ] Low (cosmetic issue)

**Priority:**
- [ ] P0 (fix immediately)
- [ ] P1 (fix before release)
- [ ] P2 (fix soon)
- [ ] P3 (fix when possible)

**Environment:**
- Browser: [Chrome 120.0]
- OS: [Windows 11]
- Screen Size: [1920x1080]
- User Role: [Job Seeker / Employer]

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Screenshots:**
[Attach screenshots if applicable]

**Console Errors:**
```
[Paste any console errors here]
```

**Additional Notes:**
[Any other relevant information]

---

## Testing Checklist Summary

### Authentication & Authorization
- [ ] Job Seeker Registration
- [ ] Employer Registration
- [ ] Login (valid credentials)
- [ ] Login (invalid credentials)
- [ ] Logout
- [ ] Protected Routes

### Job Seeker Features
- [ ] Browse Jobs
- [ ] Job Search and Filters
- [ ] View Job Details
- [ ] Apply for Job
- [ ] Upload Resume
- [ ] View My Applications
- [ ] Update Profile

### Employer Features
- [ ] View Dashboard
- [ ] Create Job Posting
- [ ] Edit Job Posting
- [ ] Close/Archive Job
- [ ] View Applications
- [ ] Review Application Details
- [ ] Shortlist Candidate
- [ ] Reject Candidate
- [ ] Add Employer Notes
- [ ] Update Company Profile

### AI Features
- [ ] AI Resume Parsing
- [ ] AI Assistant Chat
- [ ] AI Cover Letter Generation
- [ ] AI Job Recommendations

### Edge Cases & Error Handling
- [ ] Form Validation
- [ ] Network Error Handling
- [ ] Session Expiration
- [ ] Large File Upload
- [ ] SQL Injection / XSS Prevention
- [ ] Concurrent Actions
- [ ] Duplicate Application Prevention

### Responsive Design
- [ ] Mobile (375px)
- [ ] Tablet (768px)
- [ ] Desktop (1920px)

### Performance
- [ ] Page Load Time
- [ ] Search Performance
- [ ] Large Dataset Handling

---

## Testing Completion

**Tester Name:** ___________________________

**Date Started:** ___________________________

**Date Completed:** ___________________________

**Total Test Cases:** 50+

**Passed:** _____

**Failed:** _____

**Blocked:** _____

**Pass Rate:** _____%

**Critical Bugs Found:** _____

**Total Bugs Found:** _____

---

## Notes and Recommendations

```
[Add any additional notes, observations, or recommendations here]
```

---

**Last Updated:** November 2024  
**Version:** 1.0  
**Maintained By:** TalentNest QA Team

