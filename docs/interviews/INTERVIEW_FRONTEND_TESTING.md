# Interview Scheduling - Frontend UI Testing Guide

## 🎯 Testing Status
**Date:** November 12, 2025  
**Feature:** Interview Scheduling UI (Phase 3, Team Member 6)  
**Branch:** `feat/interview-scheduling`

---

## 📋 Pre-Testing Setup

### ✅ Prerequisites
- [x] Backend API running on `http://localhost:8000`
- [x] Frontend running on `http://localhost:3000`
- [x] Test users created (employer and job seeker)
- [x] Sample data populated (companies, jobs, applications)

### Test Users
```
Employer:
- Email: test_employer_1731345074@example.com
- Password: TestPassword123!

Job Seeker:
- Email: test_jobseeker_1731345074@example.com
- Password: TestPassword123!
```

---

## 🧪 Frontend Testing Scenarios

### 1️⃣ **Employer Interview Management Page**
**URL:** `http://localhost:3000/employer/interviews`

#### Test Case 1.1: View Interviews List
- [ ] Navigate to `/employer/interviews`
- [ ] Verify page loads without errors
- [ ] Check if interviews are displayed in list view by default
- [ ] Verify each `InterviewCard` displays:
  - [ ] Candidate name and email
  - [ ] Job title and company
  - [ ] Interview date/time
  - [ ] Duration
  - [ ] Interview type badge
  - [ ] Status badge
  - [ ] Meeting link (if available)
  - [ ] Action buttons (Join/Reschedule/Cancel/Complete)

#### Test Case 1.2: Calendar View
- [ ] Click "Calendar" view mode button
- [ ] Verify calendar renders correctly
- [ ] Check if interviews are shown on their scheduled dates
- [ ] Verify clicking a date highlights interviews for that day
- [ ] Switch back to "List" view

#### Test Case 1.3: Filter by Status
- [ ] Test "All" filter - shows all interviews
- [ ] Test "Scheduled" filter - shows only scheduled
- [ ] Test "Rescheduled" filter - shows rescheduled interviews
- [ ] Test "Completed" filter - shows completed interviews
- [ ] Test "Cancelled" filter - shows cancelled interviews

#### Test Case 1.4: Search Functionality
- [ ] Enter candidate name in search box
- [ ] Verify results filter in real-time
- [ ] Test searching by job title
- [ ] Clear search and verify all interviews return

#### Test Case 1.5: Schedule New Interview
- [ ] Click "Schedule Interview" button
- [ ] Verify modal opens with form
- [ ] Check form fields:
  - [ ] Application selector (dropdown)
  - [ ] Date/Time picker
  - [ ] Duration (minutes)
  - [ ] Interview type selector
  - [ ] Meeting link input
  - [ ] Meeting location input
  - [ ] Meeting instructions textarea
  - [ ] Notes textarea
- [ ] Fill out form with valid data
- [ ] Submit form
- [ ] Verify success message
- [ ] Check if new interview appears in list
- [ ] Verify email notifications were sent (check console logs)

#### Test Case 1.6: Reschedule Interview
- [ ] Find a "scheduled" interview
- [ ] Click "Reschedule" button
- [ ] Verify reschedule modal opens
- [ ] Enter new date/time
- [ ] Add optional reason
- [ ] Submit reschedule
- [ ] Verify success message
- [ ] Check interview status changed to "rescheduled"
- [ ] Verify updated time is displayed

#### Test Case 1.7: Cancel Interview
- [ ] Find an active interview
- [ ] Click "Cancel" button
- [ ] Verify confirmation modal
- [ ] Add cancellation reason
- [ ] Confirm cancellation
- [ ] Verify success message
- [ ] Check status changed to "cancelled"
- [ ] Verify interview still visible in list but marked cancelled

#### Test Case 1.8: Complete Interview
- [ ] Find a past scheduled interview
- [ ] Click "Complete" button
- [ ] Verify completion modal opens
- [ ] Add feedback and interviewer notes
- [ ] Submit completion
- [ ] Verify success message
- [ ] Check status changed to "completed"

#### Test Case 1.9: Join Interview
- [ ] Find interview with meeting link
- [ ] Click "Join Interview" button
- [ ] Verify meeting link opens in new tab (if external)
- [ ] Check button only shows for interviews with meeting links

---

### 2️⃣ **Job Seeker Interview Page**
**URL:** `http://localhost:3000/dashboard/interviews`

#### Test Case 2.1: View My Interviews
- [ ] Login as job seeker
- [ ] Navigate to `/dashboard/interviews`
- [ ] Verify page loads correctly
- [ ] Check only candidate's own interviews are shown
- [ ] Verify `InterviewCard` displays:
  - [ ] Company name and employer contact
  - [ ] Job title
  - [ ] Interview date/time
  - [ ] Duration and type
  - [ ] Status badge
  - [ ] Meeting details
  - [ ] Action buttons (Join/Cancel only)

#### Test Case 2.2: Calendar View (Job Seeker)
- [ ] Switch to Calendar view
- [ ] Verify interviews are shown on calendar
- [ ] Check date highlighting works
- [ ] Verify no "Schedule Interview" button visible

#### Test Case 2.3: Filter Interviews (Job Seeker)
- [ ] Test all status filters
- [ ] Verify filtering works correctly
- [ ] Check search functionality

#### Test Case 2.4: Join Interview (Job Seeker)
- [ ] Find upcoming interview with meeting link
- [ ] Click "Join Interview" button
- [ ] Verify link opens correctly
- [ ] Check button is disabled for past interviews

#### Test Case 2.5: Cancel Interview Request (Job Seeker)
- [ ] Find scheduled interview
- [ ] Click "Cancel" button
- [ ] Enter cancellation reason in modal
- [ ] Confirm cancellation
- [ ] Verify success message
- [ ] Check status updated to "cancelled"

#### Test Case 2.6: Read-Only Actions
- [ ] Verify job seeker CANNOT:
  - [ ] Schedule new interviews
  - [ ] Reschedule interviews (employer only)
  - [ ] Complete interviews (employer only)
  - [ ] Edit interview details

---

### 3️⃣ **UI/UX Testing**

#### Test Case 3.1: Responsive Design
- [ ] Test on desktop (1920x1080)
- [ ] Test on laptop (1366x768)
- [ ] Test on tablet (768px width)
- [ ] Test on mobile (375px width)
- [ ] Verify modals are responsive
- [ ] Check calendar view on mobile

#### Test Case 3.2: Loading States
- [ ] Verify loading spinners appear while fetching interviews
- [ ] Check skeleton loaders or placeholders
- [ ] Verify "No interviews found" message when empty

#### Test Case 3.3: Error Handling
- [ ] Test with backend down - verify error messages
- [ ] Submit invalid form data - check validation errors
- [ ] Test network timeout scenarios
- [ ] Verify user-friendly error messages

#### Test Case 3.4: Visual Design
- [ ] Verify status badges have correct colors:
  - [ ] Scheduled - Blue
  - [ ] Rescheduled - Orange/Yellow
  - [ ] Completed - Green
  - [ ] Cancelled - Red/Gray
  - [ ] No Show - Red
- [ ] Check interview type badges styling
- [ ] Verify proper spacing and alignment
- [ ] Check hover effects on buttons
- [ ] Verify modal animations

#### Test Case 3.5: Accessibility
- [ ] Tab navigation works through all interactive elements
- [ ] Form inputs have proper labels
- [ ] Buttons have descriptive text
- [ ] Color contrast meets WCAG standards
- [ ] Screen reader compatibility (if possible)

---

### 4️⃣ **Integration Testing**

#### Test Case 4.1: Data Consistency
- [ ] Schedule interview in frontend
- [ ] Verify it appears in backend API (`GET /api/v1/interviews`)
- [ ] Update interview in frontend
- [ ] Check updates reflect in backend
- [ ] Cancel interview and verify database update

#### Test Case 4.2: Real-Time Updates
- [ ] Open employer page in one browser
- [ ] Open job seeker page in another browser
- [ ] Schedule interview as employer
- [ ] Verify job seeker sees new interview (may need refresh)

#### Test Case 4.3: Email Notifications
- [ ] Schedule interview and check backend logs for email sent
- [ ] Reschedule and verify reschedule email logged
- [ ] Cancel and verify cancellation email logged
- [ ] Check email content in console output

#### Test Case 4.4: Navigation
- [ ] Navigate to interviews page from dashboard
- [ ] Use breadcrumbs (if available)
- [ ] Test back button behavior
- [ ] Verify proper authentication redirects

---

### 5️⃣ **Edge Cases & Error Scenarios**

#### Test Case 5.1: Past Interviews
- [ ] Verify past interviews show "Complete" button
- [ ] Check "Join" button disabled for past interviews
- [ ] Verify cannot reschedule past completed interviews

#### Test Case 5.2: Concurrent Actions
- [ ] Try to reschedule already cancelled interview
- [ ] Try to complete already cancelled interview
- [ ] Verify proper error handling

#### Test Case 5.3: Empty States
- [ ] Test page with no interviews
- [ ] Verify helpful empty state message
- [ ] Check if "Schedule Interview" CTA is prominent (employer)

#### Test Case 5.4: Long Text Handling
- [ ] Enter very long meeting instructions
- [ ] Add long feedback text
- [ ] Verify text truncation or proper wrapping

#### Test Case 5.5: Date/Time Edge Cases
- [ ] Schedule interview for today
- [ ] Try scheduling in the past (should be prevented)
- [ ] Test timezone handling
- [ ] Verify date formatting is correct

---

## 🎨 Components to Test

### InterviewCard Component
**Location:** `frontend/features/interviews/InterviewCard.tsx`

- [ ] Props are passed correctly
- [ ] Conditional rendering based on user role
- [ ] Action buttons show/hide appropriately
- [ ] Status and type badges render correctly
- [ ] Meeting details display properly
- [ ] Click handlers work for all actions

### InterviewCalendar Component
**Location:** `frontend/features/interviews/InterviewCalendar.tsx`

- [ ] Calendar grid renders correctly
- [ ] Current month/year displayed
- [ ] Navigation buttons (prev/next month) work
- [ ] Interviews appear on correct dates
- [ ] Today's date is highlighted
- [ ] Clicking dates filters interviews

---

## 📊 Browser Compatibility

Test on multiple browsers:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (if on Mac)
- [ ] Edge (latest)

---

## ✅ Testing Checklist Summary

### Critical Functionality
- [ ] Employer can schedule interviews
- [ ] Employer can reschedule interviews
- [ ] Employer can cancel interviews
- [ ] Employer can complete interviews
- [ ] Job seeker can view their interviews
- [ ] Job seeker can join interviews (via meeting link)
- [ ] Job seeker can cancel interview requests
- [ ] Status badges display correctly
- [ ] Filters work properly
- [ ] Search functionality works
- [ ] Calendar view displays interviews

### UI/UX
- [ ] Responsive on all screen sizes
- [ ] Loading states implemented
- [ ] Error messages are clear
- [ ] Forms validate input properly
- [ ] Modals work correctly
- [ ] Buttons disabled when appropriate

### Integration
- [ ] Frontend communicates with backend API
- [ ] Authentication works correctly
- [ ] Role-based access control enforced
- [ ] Email notifications triggered

---

## 🐛 Known Issues / Notes
_(Document any issues found during testing)_

---

## 📝 Test Results

### Manual Testing Session 1
**Date:** _______  
**Tester:** _______  
**Pass Rate:** ___/___  
**Issues Found:** _______  

---

## 🔗 Related Documentation
- [INTERVIEW_SCHEDULING_IMPLEMENTATION.md](./INTERVIEW_SCHEDULING_IMPLEMENTATION.md)
- [INTERVIEW_API_TEST_RESULTS.md](./INTERVIEW_API_TEST_RESULTS.md)
- [Frontend Guide](./FRONTEND_GUIDE.md)

---

## 📞 Support
If you encounter any issues during testing, please:
1. Check browser console for errors
2. Verify backend is running and accessible
3. Check network tab for failed API calls
4. Document the issue with screenshots
5. Report to development team

