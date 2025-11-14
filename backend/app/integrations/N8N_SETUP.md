# n8n Workflow Automation Setup

## Overview

This document describes how to set up and use n8n for AI workflow orchestration in the JobPortal application.

## What is n8n?

n8n is an open-source workflow automation tool that allows you to connect different services and automate complex processes. In JobPortal, we use n8n to orchestrate AI workflows for:

- Job recommendations
- Candidate matching
- Resume parsing
- Email notifications
- Complex multi-step AI processes

## Installation

### Option 1: Docker (Recommended)

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Option 2: npm

```bash
npm install n8n -g
n8n start
```

### Option 3: Docker Compose (with JobPortal)

Add to your `docker-compose.yml`:

```yaml
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=your_secure_password
      - WEBHOOK_URL=http://localhost:5678/
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# n8n Configuration
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=your_n8n_api_key_here

# Workflow IDs (created in n8n)
N8N_JOB_RECOMMENDATION_WORKFLOW_ID=job-recommendation
N8N_CANDIDATE_MATCHING_WORKFLOW_ID=candidate-matching
N8N_RESUME_PARSING_WORKFLOW_ID=resume-parsing
N8N_EMAIL_NOTIFICATION_WORKFLOW_ID=email-notification
```

### Generate API Key

1. Open n8n UI: `http://localhost:5678`
2. Go to Settings → API
3. Create a new API key
4. Copy the key to your `.env` file

## Workflow Templates

### 1. Job Recommendation Workflow

**Workflow ID**: `job-recommendation`

**Trigger**: Webhook
**Nodes**:
1. Webhook (Trigger)
2. HTTP Request to OpenAI (Get embeddings)
3. ChromaDB Query (Similarity search)
4. LangChain LLM (Rank and analyze)
5. Respond to Webhook

**Input**:
```json
{
  "user_id": "string",
  "user_profile": {
    "skills": ["Python", "FastAPI"],
    "experience": "5 years",
    "bio": "..."
  },
  "job_ids": ["job1", "job2", "job3"]
}
```

**Output**:
```json
{
  "recommendations": [
    {
      "job_id": "job1",
      "match_score": 95,
      "match_reason": "..."
    }
  ]
}
```

### 2. Candidate Matching Workflow

**Workflow ID**: `candidate-matching`

**Trigger**: Webhook
**Nodes**:
1. Webhook (Trigger)
2. HTTP Request to OpenAI (Analyze requirements)
3. ChromaDB Query (Find similar profiles)
4. LangChain LLM (Rank candidates)
5. Respond to Webhook

**Input**:
```json
{
  "job_id": "string",
  "job_details": {
    "title": "Senior Software Engineer",
    "required_skills": ["Python", "FastAPI"],
    "description": "..."
  },
  "candidate_ids": ["user1", "user2", "user3"]
}
```

**Output**:
```json
{
  "rankings": [
    {
      "candidate_id": "user1",
      "match_score": 92,
      "match_reason": "..."
    }
  ]
}
```

### 3. Resume Parsing Workflow

**Workflow ID**: `resume-parsing`

**Trigger**: Webhook
**Nodes**:
1. Webhook (Trigger)
2. HTTP Request (Download resume)
3. OpenAI GPT-4o (Extract information)
4. Structured Data Parser
5. Respond to Webhook

### 4. Email Notification Workflow

**Workflow ID**: `email-notification`

**Trigger**: Webhook
**Nodes**:
1. Webhook (Trigger)
2. Template Renderer
3. SMTP Email Node
4. Respond to Webhook

## Usage in Code

### Trigger Job Recommendations

```python
from app.integrations.n8n_client import n8n_client

result = await n8n_client.trigger_job_recommendation_workflow(
    user_id="user123",
    user_profile={
        "skills": ["Python", "FastAPI"],
        "experience": "5 years"
    },
    job_ids=["job1", "job2", "job3"]
)
```

### Trigger Candidate Matching

```python
result = await n8n_client.trigger_candidate_matching_workflow(
    job_id="job123",
    job_details={
        "title": "Senior Software Engineer",
        "required_skills": ["Python", "FastAPI"]
    },
    candidate_ids=["user1", "user2", "user3"]
)
```

## Benefits of Using n8n

1. **Visual Workflow Design**: Create complex AI workflows with a drag-and-drop interface
2. **No Code Required**: Non-technical team members can modify workflows
3. **Extensive Integrations**: Connect to 200+ services (Slack, Gmail, etc.)
4. **Error Handling**: Built-in retry logic and error notifications
5. **Monitoring**: Track workflow executions and performance
6. **Scalability**: Run workflows in parallel and handle high volumes

## When to Use n8n vs Direct Implementation

### Use n8n for:
- Complex multi-step workflows
- Workflows that change frequently
- Integration with external services
- Workflows that need visual monitoring
- Processes that require non-developer input

### Use Direct Implementation for:
- Simple, single-step operations
- Performance-critical paths
- Core application logic
- Real-time requirements

## Troubleshooting

### n8n Not Responding

1. Check if n8n is running: `docker ps` or `curl http://localhost:5678`
2. Verify API key in `.env`
3. Check n8n logs: `docker logs n8n`

### Workflow Execution Failed

1. Check workflow status in n8n UI
2. Review execution logs
3. Verify webhook URL is correct
4. Check input data format

### API Key Issues

1. Regenerate API key in n8n UI
2. Update `.env` file
3. Restart backend application

## Production Considerations

1. **Security**: Use strong API keys and enable HTTPS
2. **Scaling**: Run multiple n8n instances behind a load balancer
3. **Monitoring**: Set up alerts for failed workflows
4. **Backup**: Regularly backup n8n data volume
5. **Rate Limiting**: Configure rate limits for webhook triggers

## Additional Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [Workflow Templates](https://n8n.io/workflows/)
- [LangChain Integration](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain/)

## Example Workflow JSON

See `n8n_workflows/` directory for exportable workflow JSON files that you can import directly into n8n.

