# n8n Workflow Automation for JobPortal

This document describes the n8n workflows used in the JobPortal application for AI orchestration and automation.

## Overview

n8n is used to orchestrate complex AI workflows and automate repetitive tasks. The JobPortal integrates with n8n through webhook triggers and API calls.

## Prerequisites

1. **n8n Installation**: Install n8n locally or use n8n Cloud
   ```bash
   npm install -g n8n
   n8n start
   ```
   Default URL: http://localhost:5678

2. **API Key**: Generate an API key in n8n Settings → API

3. **Configuration**: Add n8n settings to `.env`:
   ```bash
   N8N_BASE_URL=http://localhost:5678
   N8N_API_KEY=your-n8n-api-key-here
   N8N_JOB_RECOMMENDATION_WORKFLOW_ID=job-recommendation
   N8N_CANDIDATE_MATCHING_WORKFLOW_ID=candidate-matching
   N8N_RESUME_PARSING_WORKFLOW_ID=resume-parsing
   N8N_EMAIL_NOTIFICATION_WORKFLOW_ID=email-notification
   ```

## Workflows

### 1. Job Recommendation Workflow

**ID**: `job-recommendation`  
**Purpose**: Generate personalized job recommendations using AI

**Trigger**: Webhook POST `/webhook/job-recommendation`

**Input**:
```json
{
  "user_id": "user123",
  "user_profile": {
    "skills": ["Python", "FastAPI", "MongoDB"],
    "experience": "5 years",
    "education": "Bachelor's in CS"
  },
  "job_ids": ["job1", "job2", "job3"],
  "action": "generate_recommendations"
}
```

**Workflow Steps**:
1. Receive webhook trigger
2. Fetch job details from JobPortal API
3. Generate embeddings for user profile (OpenAI)
4. Perform vector similarity search (ChromaDB)
5. Score matches with LLM (GPT-4o)
6. Return ranked recommendations

**Output**:
```json
{
  "user_id": "user123",
  "recommendations": [
    {
      "job_id": "job1",
      "match_score": 95,
      "reasons": ["Strong Python skills", "Experience matches"]
    }
  ]
}
```

---

### 2. Candidate Matching Workflow

**ID**: `candidate-matching`  
**Purpose**: Rank candidates for a job using AI

**Trigger**: Webhook POST `/webhook/candidate-matching`

**Input**:
```json
{
  "job_id": "job123",
  "job_requirements": {
    "title": "Senior Python Developer",
    "skills": ["Python", "FastAPI", "Docker"],
    "experience_level": "Senior"
  },
  "candidate_ids": ["user1", "user2", "user3"],
  "action": "rank_candidates"
}
```

**Workflow Steps**:
1. Receive webhook trigger
2. Fetch candidate profiles from JobPortal API
3. Generate embeddings for job requirements (OpenAI)
4. Perform vector similarity search (ChromaDB)
5. Score candidates with LLM (GPT-4o)
6. Return ranked candidates

**Output**:
```json
{
  "job_id": "job123",
  "ranked_candidates": [
    {
      "user_id": "user1",
      "match_score": 92,
      "reasons": ["Excellent Python skills", "Senior experience"]
    }
  ]
}
```

---

### 3. Resume Parsing Workflow

**ID**: `resume-parsing`  
**Purpose**: Extract structured data from resumes using AI

**Trigger**: Webhook POST `/webhook/resume-parsing`

**Input**:
```json
{
  "resume_id": "resume123",
  "file_url": "https://storage.example.com/resumes/resume123.pdf",
  "user_id": "user123",
  "action": "parse_resume"
}
```

**Workflow Steps**:
1. Receive webhook trigger
2. Download resume file
3. Extract text (PyPDF2 for PDF, python-docx for DOCX)
4. Parse with LLM (GPT-4o)
5. Extract skills, experience, education
6. Update resume in JobPortal database

**Output**:
```json
{
  "resume_id": "resume123",
  "parsed_data": {
    "skills": ["Python", "JavaScript", "React"],
    "experience": "5 years as Software Engineer",
    "education": "BS in Computer Science",
    "summary": "Experienced full-stack developer..."
  }
}
```

---

### 4. Email Notification Workflow

**ID**: `email-notification`  
**Purpose**: Send templated emails for various events

**Trigger**: Webhook POST `/webhook/email-notification`

**Input**:
```json
{
  "notification_type": "application_submitted",
  "recipient_email": "user@example.com",
  "template_data": {
    "user_name": "John Doe",
    "job_title": "Senior Python Developer",
    "company_name": "Tech Corp"
  },
  "action": "send_email"
}
```

**Workflow Steps**:
1. Receive webhook trigger
2. Select email template based on notification_type
3. Populate template with data
4. Send email via SMTP
5. Log delivery status

**Notification Types**:
- `application_submitted` - Confirmation to job seeker
- `application_received` - Notification to employer
- `interview_scheduled` - Interview invitation
- `application_status_changed` - Status update
- `job_recommendation` - New job matches

**Output**:
```json
{
  "status": "sent",
  "recipient": "user@example.com",
  "notification_type": "application_submitted",
  "sent_at": "2024-01-15T10:30:00Z"
}
```

---

## Workflow Creation Guide

### Step 1: Create Workflow in n8n

1. Open n8n UI (http://localhost:5678)
2. Click "New Workflow"
3. Add "Webhook" node as trigger
4. Configure webhook path (e.g., `/webhook/job-recommendation`)
5. Add processing nodes (HTTP Request, OpenAI, Code, etc.)
6. Add response node
7. Save workflow

### Step 2: Get Workflow ID

- The workflow ID is in the webhook URL
- Example: `http://localhost:5678/webhook/job-recommendation`
- ID: `job-recommendation`

### Step 3: Configure in JobPortal

Add workflow ID to `.env`:
```bash
N8N_JOB_RECOMMENDATION_WORKFLOW_ID=job-recommendation
```

### Step 4: Test Integration

```python
from app.integrations import get_n8n_client

n8n = get_n8n_client()
result = await n8n.trigger_job_recommendation_workflow(
    user_id="test123",
    user_profile={"skills": ["Python"]},
    job_ids=["job1", "job2"]
)
print(result)
```

---

## Usage in JobPortal

### Job Recommendations

```python
from app.integrations import get_n8n_client

async def get_recommendations_with_n8n(user, jobs):
    n8n = get_n8n_client()
    
    if n8n.is_enabled():
        result = await n8n.trigger_job_recommendation_workflow(
            user_id=str(user.id),
            user_profile={
                "skills": user.skills,
                "experience": user.experience_years,
            },
            job_ids=[str(job.id) for job in jobs]
        )
        return result
    else:
        # Fallback to direct AI processing
        return await process_recommendations_directly(user, jobs)
```

### Candidate Matching

```python
from app.integrations import get_n8n_client

async def rank_candidates_with_n8n(job, candidates):
    n8n = get_n8n_client()
    
    if n8n.is_enabled():
        result = await n8n.trigger_candidate_matching_workflow(
            job_id=str(job.id),
            job_requirements={
                "title": job.title,
                "skills": job.skills,
            },
            candidate_ids=[str(c.id) for c in candidates]
        )
        return result
    else:
        # Fallback to direct AI processing
        return await rank_candidates_directly(job, candidates)
```

---

## Benefits of n8n Integration

1. **Visual Workflow Design**: Easy to understand and modify workflows
2. **No-Code/Low-Code**: Non-developers can create and update workflows
3. **Scalability**: Offload AI processing to separate service
4. **Monitoring**: Built-in execution logs and error handling
5. **Flexibility**: Easy to add new AI providers or change logic
6. **Reusability**: Workflows can be shared across projects

---

## Troubleshooting

### n8n Not Responding

- Check if n8n is running: `curl http://localhost:5678/healthz`
- Verify API key in `.env`
- Check n8n logs for errors

### Workflow Not Triggering

- Verify webhook URL is correct
- Check workflow is activated in n8n UI
- Ensure API key has proper permissions

### Slow Performance

- Use async/await for non-blocking calls
- Set `wait_for_completion=False` for fire-and-forget workflows
- Consider using n8n Cloud for better performance

---

## Optional: Advanced Workflows

### Multi-Stage Job Matching

1. Vector similarity search (ChromaDB)
2. AI scoring (GPT-4o)
3. Skills verification (external API)
4. Culture fit analysis (Claude)
5. Final ranking with weighted scores

### Automated Interview Scheduling

1. Candidate accepts interview
2. Check employer calendar availability
3. Send calendar invites
4. Create meeting link (Zoom/Google Meet)
5. Send reminder emails

---

## Notes

- n8n integration is **optional** - JobPortal works without it
- If n8n is not configured, the system falls back to direct AI processing
- Workflows can be exported/imported as JSON for version control
- Consider using n8n Cloud for production deployments

For more information, visit: https://docs.n8n.io/









