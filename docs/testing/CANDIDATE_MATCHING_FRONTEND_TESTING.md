# Candidate Matching Frontend Testing Guide

## Overview
This guide will help you test the newly implemented AI Candidate Matching frontend feature. This feature allows employers to view AI-ranked candidates for their job postings.

## Prerequisites

1. **Backend Server Running**
   - Backend should be running on `http://localhost:8000`
   - Verify: Open `http://localhost:8000/docs` in your browser

2. **Frontend Server Running**
   - Frontend should be running on `http://localhost:3000`
   - Verify: Open `http://localhost:3000` in your browser

3. **Test Data Setup**
   - You need at least one employer account
   - You need at least one job posting created by that employer
   - You need at least one job seeker who has applied to that job
   - Job seekers should have profiles with skills and resumes uploaded

## Step-by-Step Testing Instructions

### Step 1: Login as Employer

1. Navigate to `http://localhost:3000/login`
2. Login with an employer account
3. You should be redirected to `/employer/dashboard`

**Expected Result:** ✅ You see the employer dashboard

---

### Step 2: Navigate to Job Applications Page

**Option A: Via Dashboard**
1. From the employer dashboard, click on "My Jobs" or navigate to `/employer/jobs`
2. Find a job that has applications
3. Click on the job to view details
4. Click on "View Applications" or navigate to `/employer/jobs/[job_id]/applications`

**Option B: Direct URL**
1. If you know a job ID, navigate directly to:
   ```
   http://localhost:3000/employer/jobs/[JOB_ID]/applications
   ```
   Replace `[JOB_ID]` with an actual job ID from your database

**Expected Result:** ✅ You see the applications page with:
- Stats cards (Total, Pending, Reviewing, Shortlisted, Rejected)
- Filter buttons
- **AI-Recommended Candidates section** (purple gradient card)
- List of all applications

---

### Step 3: Test AI Recommendations Section

#### 3.1 Initial Load
- The AI recommendations section should appear near the top of the page
- It should have a purple gradient background
- Look for the section with:
  - Sparkles icon (✨)
  - Title: "AI-Recommended Candidates"
  - Description about AI-powered matching
  - Refresh and Show/Hide buttons

**Expected Result:** ✅ Section is visible and styled correctly

#### 3.2 Loading State
- When the page first loads, you should see a loading spinner in the recommendations section
- The refresh button should be disabled during loading

**Expected Result:** ✅ Loading state displays correctly

#### 3.3 Recommendations Display

**If Recommendations Exist:**
- You should see candidate cards in a grid layout (2 columns on desktop)
- Each card should show:
  - **Match Score** (0-100%) in the top right corner with color coding:
    - Green (80-100%): Excellent match
    - Blue (60-79%): Good match
    - Yellow (40-59%): Moderate match
    - Gray (<40%): Low match
  - **Candidate Avatar** (initials in colored circle)
  - **Candidate Name** with sparkles icon
  - **Email Address**
  - **Application Status Badge** (pending, reviewing, shortlisted, etc.)
  - **Applied Date** (time ago format)
  - **Skills** (if available from resume)
  - **Match Reasons** section (AI-powered insights explaining why the candidate matches)
  - **Action Buttons**:
    - View Resume (if resume available)
    - View Application
    - Shortlist (if status is "reviewing")
    - Schedule Interview (if status is "shortlisted")

**Expected Result:** ✅ Candidate cards display with all information

**If No Recommendations:**
- You should see an empty state message:
  - "No AI recommendations available yet"
  - Helpful message about candidates appearing once they apply

**Expected Result:** ✅ Empty state displays correctly

---

### Step 4: Test Interactive Features

#### 4.1 Refresh Button
1. Click the "Refresh" button
2. The refresh icon should spin during loading
3. The button should be disabled during refresh
4. Recommendations should reload

**Expected Result:** ✅ Refresh functionality works correctly

#### 4.2 Show/Hide Toggle
1. Click the "Hide" button
2. The recommendations list should collapse
3. The button should change to "Show"
4. Click "Show" again
5. The recommendations should expand

**Expected Result:** ✅ Show/Hide toggle works correctly

#### 4.3 View Application
1. Click "View Application" on a candidate card
2. A modal should open showing full application details
3. The modal should include:
   - Candidate information
   - Cover letter (if available)
   - Resume link
   - Application status
   - Action buttons

**Expected Result:** ✅ Application modal opens correctly

#### 4.4 View Resume
1. Click "View Resume" on a candidate card (if resume is available)
2. Resume should open in a new tab/window

**Expected Result:** ✅ Resume opens correctly

#### 4.5 Shortlist Action
1. Find a candidate with status "reviewing"
2. Click "Shortlist" button
3. The application status should update
4. The candidate should move to "shortlisted" status

**Expected Result:** ✅ Shortlist action works correctly

#### 4.6 Schedule Interview
1. Find a candidate with status "shortlisted"
2. Click "Schedule Interview" button
3. Should navigate to interview scheduling page (or open modal)

**Expected Result:** ✅ Schedule interview action works correctly

---

### Step 5: Test Error Handling

#### 5.1 Network Error
1. Stop the backend server
2. Try to refresh recommendations
3. You should see an error message in red
4. Error should be user-friendly

**Expected Result:** ✅ Error handling displays correctly

#### 5.2 Empty State
1. Navigate to a job with no applications
2. Recommendations section should show empty state
3. Message should be helpful

**Expected Result:** ✅ Empty state displays correctly

---

### Step 6: Test Dark Mode

1. Toggle dark mode using the theme switcher in the navbar
2. Verify that:
   - Recommendations section adapts to dark mode
   - Candidate cards have proper contrast
   - Text is readable
   - Colors are appropriate for dark theme

**Expected Result:** ✅ Dark mode works correctly

---

### Step 7: Test Responsive Design

1. Resize your browser window or use browser dev tools
2. Test on different screen sizes:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1920px)
3. Verify:
   - Grid layout adjusts (1 column on mobile, 2 on desktop)
   - Cards are readable
   - Buttons are accessible
   - Text doesn't overflow

**Expected Result:** ✅ Responsive design works correctly

---

## API Testing (Optional)

If you want to test the API directly:

### Test Endpoint
```bash
GET http://localhost:8000/api/v1/jobs/{job_id}/recommended-candidates?limit=10
```

**Headers:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/YOUR_JOB_ID/recommended-candidates?limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Response:**
```json
{
  "job_id": "job_id_here",
  "job_title": "Software Engineer",
  "total_candidates": 5,
  "candidates": [
    {
      "user_id": "user_id",
      "full_name": "John Doe",
      "email": "john@example.com",
      "match_score": 85,
      "reasons": [
        "Strong match in Python and JavaScript skills",
        "Relevant experience in web development",
        "Education aligns with job requirements"
      ],
      "application_id": "app_id",
      "application_status": "reviewing",
      "applied_at": "2024-01-15T10:30:00",
      "resume": {
        "resume_id": "resume_id",
        "file_url": "http://...",
        "skills": ["Python", "JavaScript", "React"],
        "uploaded_at": "2024-01-10T09:00:00"
      }
    }
  ]
}
```

---

## Common Issues & Troubleshooting

### Issue: No recommendations showing
**Possible Causes:**
1. No candidates have applied to the job
2. Candidate profiles haven't been synced to vector store
3. Vector store is empty

**Solution:**
- Ensure candidates have applied to the job
- Check if profiles need to be synced (may need to call sync endpoint)
- Verify vector store is initialized

### Issue: Error loading recommendations
**Possible Causes:**
1. Backend server not running
2. Authentication token expired
3. Job doesn't belong to current employer
4. Vector store not initialized

**Solution:**
- Check backend server status
- Re-login to get fresh token
- Verify job ownership
- Check backend logs for errors

### Issue: Match scores seem incorrect
**Possible Causes:**
1. Vector store not synced with latest profiles
2. Job requirements not properly indexed

**Solution:**
- Sync profiles to vector store
- Verify job posting has proper skills/requirements

---

## Test Checklist

- [ ] Can access employer applications page
- [ ] AI recommendations section is visible
- [ ] Recommendations load on page load
- [ ] Loading state displays correctly
- [ ] Candidate cards display with all information
- [ ] Match scores show with correct colors
- [ ] Match reasons are displayed
- [ ] Refresh button works
- [ ] Show/Hide toggle works
- [ ] View Application opens modal
- [ ] View Resume opens resume
- [ ] Shortlist action works
- [ ] Schedule Interview action works
- [ ] Error handling displays correctly
- [ ] Empty state displays correctly
- [ ] Dark mode works
- [ ] Responsive design works

---

## Success Criteria

✅ **Feature is working correctly if:**
1. Recommendations section appears on employer job applications page
2. Candidate cards display with match scores and reasons
3. All interactive features work (refresh, show/hide, actions)
4. Error handling is user-friendly
5. Dark mode and responsive design work correctly
6. No console errors in browser dev tools

---

## Notes

- The feature uses ChromaDB vector similarity search + AI scoring
- Match scores are calculated using 70% vector similarity + 30% AI scoring
- Recommendations are only shown for candidates who have applied to the job
- The feature requires candidate profiles to be synced to the vector store









