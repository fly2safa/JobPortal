# AI Features Testing Guide

## Overview

This guide provides comprehensive testing procedures for all AI-powered features in the JobPortal application, including LangChain, ChromaDB, and n8n integrations.

---

## Prerequisites

### 1. Environment Setup

Ensure these environment variables are set in `backend/.env`:

```bash
# OpenAI API Key (Required)
OPENAI_API_KEY=sk-...

# n8n Configuration (Optional)
N8N_BASE_URL=http://localhost:5678
N8N_API_KEY=your_api_key_here

# MongoDB (Required)
MONGODB_URI=mongodb+srv://...
DATABASE_NAME=jobportal
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Verify AI dependencies are installed:
```bash
python -c "import langchain; import chromadb; import openai; print('✓ All AI dependencies installed')"
```

### 3. Start Services

**Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

**n8n (Optional):**
```bash
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

---

## Test Cases

### 1. Vector Store & Embeddings

#### Test 1.1: ChromaDB Initialization
**Objective**: Verify ChromaDB vector store initializes correctly

**Steps**:
1. Start the backend
2. Check logs for: `"Initialized ChromaDB vector store"`
3. Navigate to `http://localhost:8000/api/v1/recommendations/health`

**Expected Result**:
```json
{
  "status": "healthy",
  "indexed_jobs": 0,
  "ai_enabled": true
}
```

#### Test 1.2: OpenAI Embeddings
**Objective**: Test embedding generation

**Python Test**:
```python
from app.ai.rag.embeddings import embedding_service

# Test single text embedding
text = "Python developer with 5 years experience"
embedding = embedding_service.embed_text(text)

assert len(embedding) == 1536  # text-embedding-3-small dimension
print("✓ Embedding generation successful")
```

#### Test 1.3: Vector Similarity Search
**Objective**: Test semantic search functionality

**Python Test**:
```python
from app.ai.rag.vectorstore import job_vectorstore
from langchain.schema import Document

# Add test documents
docs = [
    Document(page_content="Python FastAPI developer", metadata={"id": "1"}),
    Document(page_content="Java Spring Boot developer", metadata={"id": "2"}),
    Document(page_content="Frontend React developer", metadata={"id": "3"})
]
job_vectorstore.add_documents(docs)

# Search
results = job_vectorstore.similarity_search("Python backend engineer", k=2)

assert len(results) >= 1
assert "Python" in results[0].page_content
print("✓ Vector similarity search working")
```

---

### 2. Job Recommendations (Job Seeker)

#### Test 2.1: Get Recommendations API
**Objective**: Test AI-powered job recommendations endpoint

**API Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/recommendations/?limit=5&use_ai=true" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Response**:
```json
{
  "recommendations": [
    {
      "job_id": "...",
      "job_title": "Senior Python Developer",
      "company": "Tech Corp",
      "match_score": 95,
      "match_reason": "Your 5 years of Python experience...",
      "skills_alignment": ["Python", "FastAPI", "MongoDB"],
      "growth_potential": "High - Senior role with leadership"
    }
  ],
  "total": 5
}
```

**Validation**:
- ✓ Match scores are between 0-100
- ✓ Recommendations are sorted by match score (highest first)
- ✓ Match reasons are personalized and relevant
- ✓ Skills alignment shows matching skills

#### Test 2.2: Frontend Recommendations Page
**Objective**: Test job seeker recommendations UI

**Steps**:
1. Login as job seeker: `jobseeker@test.com` / `Test123!`
2. Navigate to `/dashboard/recommendations`
3. Verify recommendations load
4. Toggle "AI-Powered Ranking" switch
5. Click "Refresh" button
6. Click "View Job Details" on a recommendation

**Expected Behavior**:
- ✓ Recommendations display with match scores
- ✓ Skills are color-coded (green for matches)
- ✓ AI toggle changes ranking method
- ✓ Refresh reloads recommendations
- ✓ Job details page opens correctly

#### Test 2.3: Similar Jobs Feature
**Objective**: Test similar jobs recommendation

**API Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/recommendations/similar/JOB_ID?limit=5" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Response**:
```json
{
  "similar_jobs": [
    {
      "job_id": "...",
      "job_title": "Python Backend Engineer",
      "company": "StartupXYZ",
      "similarity_score": 0.92,
      "location": "Remote"
    }
  ],
  "total": 5
}
```

---

### 3. Candidate Matching (Employer)

#### Test 3.1: Get Recommended Candidates API
**Objective**: Test AI-powered candidate matching endpoint

**API Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/JOB_ID/recommended-candidates?limit=10&use_ai=true" \
  -H "Authorization: Bearer EMPLOYER_JWT_TOKEN"
```

**Expected Response**:
```json
{
  "rankings": [
    {
      "candidate_id": "...",
      "candidate_name": "John Doe",
      "current_role": "Software Engineer",
      "match_score": 92,
      "match_reason": "John has 5 years of Python...",
      "skills_match": {
        "matched": ["Python", "FastAPI"],
        "missing": ["Kubernetes"],
        "additional": ["AWS", "Docker"]
      },
      "experience_relevance": "Highly relevant - 5 years backend",
      "concerns": "Limited Kubernetes experience"
    }
  ],
  "total": 10,
  "job_id": "...",
  "job_title": "Senior Backend Engineer"
}
```

**Validation**:
- ✓ Candidates ranked by match score
- ✓ Skills analysis shows matched/missing/additional
- ✓ Experience relevance is assessed
- ✓ Concerns are identified

#### Test 3.2: Frontend Candidate Rankings Page
**Objective**: Test employer candidate recommendations UI

**Steps**:
1. Login as employer: `employer@test.com` / `Test123!`
2. Navigate to `/employer/jobs`
3. Click on a job posting
4. Click "View Recommended Candidates" or navigate to `/employer/jobs/JOB_ID/candidates`
5. Verify candidates load with rankings
6. Toggle "AI-Powered Ranking"
7. Toggle "Applicants Only"
8. Click "Refresh"

**Expected Behavior**:
- ✓ Candidates display with rank badges (1st = gold, 2nd = silver, 3rd = bronze)
- ✓ Match scores shown prominently
- ✓ Skills analysis color-coded (green = matched, red = missing, blue = bonus)
- ✓ AI toggle changes ranking method
- ✓ Applicants Only filter works
- ✓ Refresh reloads rankings

#### Test 3.3: Applicants Only Mode
**Objective**: Test filtering to only rank existing applicants

**API Request**:
```bash
curl -X GET "http://localhost:8000/api/v1/jobs/JOB_ID/recommended-candidates?applicants_only=true" \
  -H "Authorization: Bearer EMPLOYER_JWT_TOKEN"
```

**Expected Behavior**:
- ✓ Only returns candidates who have applied to this job
- ✓ Rankings still use AI analysis
- ✓ Empty result if no applicants

---

### 4. LangChain Integration

#### Test 4.1: Job Recommendation Chain
**Objective**: Test LangChain recommendation chain

**Python Test**:
```python
from app.ai.chains.recommendation_chain import job_recommendation_chain

user_profile = {
    "skills": ["Python", "FastAPI", "MongoDB"],
    "experience": "5 years backend development",
    "bio": "Passionate about building scalable APIs"
}

jobs = [
    {
        "id": "1",
        "title": "Senior Python Developer",
        "company_name": "Tech Corp",
        "description": "Build scalable APIs with Python and FastAPI",
        "required_skills": ["Python", "FastAPI", "Docker"]
    }
]

recommendations = await job_recommendation_chain.get_recommendations(
    user_profile=user_profile,
    available_jobs=jobs,
    top_k=5
)

assert len(recommendations) > 0
assert recommendations[0]["match_score"] >= 60
print("✓ LangChain recommendation chain working")
```

#### Test 4.2: Candidate Matching Chain
**Objective**: Test LangChain candidate matching chain

**Python Test**:
```python
from app.ai.chains.candidate_matching_chain import candidate_matching_chain

job = {
    "id": "1",
    "title": "Senior Python Developer",
    "description": "Build scalable APIs",
    "required_skills": ["Python", "FastAPI", "MongoDB"]
}

candidates = [
    {
        "id": "1",
        "name": "John Doe",
        "skills": ["Python", "FastAPI", "Docker"],
        "experience": "5 years backend development"
    }
]

rankings = await candidate_matching_chain.rank_candidates(
    job=job,
    candidates=candidates,
    top_k=10
)

assert len(rankings) > 0
assert rankings[0]["match_score"] >= 50
print("✓ LangChain candidate matching chain working")
```

---

### 5. n8n Workflow Automation

#### Test 5.1: n8n Client Initialization
**Objective**: Verify n8n client initializes

**Python Test**:
```python
from app.integrations.n8n_client import n8n_client

assert n8n_client.base_url == "http://localhost:5678"
print(f"✓ n8n client initialized - Enabled: {n8n_client.enabled}")
```

#### Test 5.2: Trigger Job Recommendation Workflow
**Objective**: Test n8n workflow trigger

**Python Test**:
```python
from app.integrations.n8n_client import n8n_client

result = await n8n_client.trigger_job_recommendation_workflow(
    user_id="user123",
    user_profile={"skills": ["Python"]},
    job_ids=["job1", "job2"]
)

print(f"Workflow result: {result}")
# Note: Will return {"status": "skipped"} if n8n not configured
```

#### Test 5.3: n8n Workflow Status
**Objective**: Test workflow execution status check

**Steps**:
1. Ensure n8n is running on port 5678
2. Create a test workflow in n8n UI
3. Trigger workflow via API
4. Check execution status

---

### 6. RAG (Retrieval-Augmented Generation)

#### Test 6.1: Vector-based Document Retrieval
**Objective**: Test RAG retriever with ChromaDB

**Python Test**:
```python
from app.ai.rag.retriever import Retriever
from langchain.schema import Document

docs = [
    Document(page_content="How to apply for jobs", metadata={"category": "job_seeker"}),
    Document(page_content="How to post a job", metadata={"category": "employer"})
]

retriever = Retriever(docs)
results = retriever.retrieve("applying for positions", top_k=1)

assert len(results) > 0
assert "apply" in results[0].page_content.lower()
print("✓ RAG retriever working with vector search")
```

#### Test 6.2: AI Assistant with RAG
**Objective**: Test AI assistant endpoint with context retrieval

**API Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/assistant/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How do I apply for a job?",
    "conversation_id": null
  }'
```

**Expected Response**:
```json
{
  "message": "To apply for a job on TalentNest, follow these steps...",
  "conversation_id": "...",
  "timestamp": "..."
}
```

---

## Performance Testing

### Test P.1: Recommendation Response Time
**Objective**: Ensure recommendations load within acceptable time

**Benchmark**:
- First request (cold start): < 5 seconds
- Subsequent requests: < 2 seconds

**Test**:
```bash
time curl -X GET "http://localhost:8000/api/v1/recommendations/?limit=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Test P.2: Vector Search Performance
**Objective**: Test ChromaDB query speed

**Benchmark**:
- 1000 documents: < 100ms
- 10000 documents: < 500ms

**Python Test**:
```python
import time
from app.ai.rag.vectorstore import job_vectorstore

start = time.time()
results = job_vectorstore.similarity_search("Python developer", k=10)
duration = time.time() - start

assert duration < 0.5  # 500ms
print(f"✓ Vector search completed in {duration:.3f}s")
```

---

## Error Handling Tests

### Test E.1: Missing OpenAI API Key
**Expected**: Fallback to HuggingFace embeddings or graceful degradation

### Test E.2: ChromaDB Connection Failure
**Expected**: Return empty results with error message

### Test E.3: n8n Unavailable
**Expected**: Skip workflow, continue with direct implementation

### Test E.4: Invalid Job/User Data
**Expected**: Return validation error with clear message

---

## Integration Testing Checklist

- [ ] All AI dependencies installed
- [ ] OpenAI API key configured
- [ ] ChromaDB initializes successfully
- [ ] Vector embeddings generate correctly
- [ ] Job recommendations API works
- [ ] Candidate matching API works
- [ ] Frontend recommendations page loads
- [ ] Frontend candidate rankings page loads
- [ ] LangChain chains execute successfully
- [ ] n8n client initializes (if configured)
- [ ] RAG retriever uses vector search
- [ ] Performance benchmarks met
- [ ] Error handling works correctly

---

## Troubleshooting

### Issue: "No module named 'langchain'"
**Solution**: `pip install langchain langchain-openai langchain-community`

### Issue: "ChromaDB not found"
**Solution**: `pip install chromadb`

### Issue: "OpenAI API key not set"
**Solution**: Add `OPENAI_API_KEY=sk-...` to `.env`

### Issue: "n8n connection refused"
**Solution**: Start n8n: `docker run -p 5678:5678 n8nio/n8n`

### Issue: "Recommendations return empty"
**Solution**: Index jobs first: `POST /api/v1/recommendations/index-jobs`

---

## Test Accounts

**Job Seeker:**
- Email: `jobseeker@test.com`
- Password: `Test123!`
- Skills: Python, FastAPI, MongoDB, Docker

**Employer:**
- Email: `employer@test.com`
- Password: `Test123!`
- Company: Test Company Inc.

---

## Automated Test Script

Run all tests:
```bash
cd backend
pytest tests/test_ai_features.py -v
```

---

## Success Criteria

✅ All API endpoints return 200 status
✅ Recommendations have match scores 60-100
✅ Candidate rankings are properly ordered
✅ Vector search returns relevant results
✅ LangChain chains execute without errors
✅ Frontend pages load and display data
✅ Performance benchmarks are met
✅ Error handling is graceful

---

## Next Steps

1. Run all test cases
2. Document any failures
3. Fix identified issues
4. Re-test until all pass
5. Deploy to staging for QA testing

