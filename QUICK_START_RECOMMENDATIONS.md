# Quick Start Guide: AI Recommendations

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.10+ installed
- Node.js 18+ installed
- MongoDB running
- OpenAI API key (optional but recommended)

---

## Step 1: Backend Setup

### 1.1 Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 1.2 Configure Environment
Create or update `.env` file:
```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=jobportal

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256

# OpenAI (Required for AI features)
OPENAI_API_KEY=sk-your-openai-api-key-here

# CORS
CORS_ORIGINS=http://localhost:3000
```

### 1.3 Start Backend
```bash
cd backend
python -m app.main
```

Backend will start at: `http://localhost:8000`

Check health: `http://localhost:8000/health`  
API Docs: `http://localhost:8000/docs`

---

## Step 2: Frontend Setup

### 2.1 Install Dependencies
```bash
cd frontend
npm install
```

### 2.2 Configure Environment
Create or update `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2.3 Start Frontend
```bash
cd frontend
npm run dev
```

Frontend will start at: `http://localhost:3000`

---

## Step 3: Initialize System

### 3.1 Ensure Data Exists

**Create a user:**
1. Go to `http://localhost:3000/register`
2. Create a job seeker account
3. Add skills to your profile (Settings → Profile)

**Ensure jobs exist:**
- Run the job migration script if needed:
```bash
cd DB_ContentGen
python migrate_jobs.py
```

### 3.2 Initialize Vector Store

**Option A: Via API (Recommended)**
```bash
# Login first to get token, then:
curl -X POST http://localhost:8000/api/v1/recommendations/initialize \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Option B: Automatic**
- Vector store initializes automatically on first recommendation request

---

## Step 4: Test Recommendations

### 4.1 Access Recommendations Page
1. Login as job seeker: `http://localhost:3000/login`
2. Navigate to: `http://localhost:3000/dashboard/recommendations`
3. Recommendations will load automatically

### 4.2 Expected Behavior

**With OpenAI API Key:**
- ✅ AI-powered match scores (0-100%)
- ✅ Intelligent match reasons
- ✅ Semantic similarity matching
- ✅ High-quality recommendations

**Without OpenAI API Key:**
- ✅ Basic skill matching
- ✅ Generic match reasons
- ✅ Lower quality but functional
- ⚠️ Warning logged in backend

---

## Step 5: Verify Integration

### 5.1 Check Backend Logs
You should see:
```
INFO: OpenAI client initialized successfully
INFO: Vector store initialized with X jobs
INFO: Generating job recommendations for user@example.com
INFO: Generated Y recommendations for user@example.com
```

### 5.2 Check Frontend
You should see:
- Page loads without errors
- Recommendations display with match scores
- AI reasons show for each job
- Filters and sorting work
- Refresh button works

### 5.3 Check API Response
```bash
curl http://localhost:8000/api/v1/recommendations/jobs \
  -H "Authorization: Bearer YOUR_TOKEN" | jq
```

Expected response:
```json
[
  {
    "job": {
      "id": "...",
      "title": "Software Engineer",
      "company_name": "TechCorp",
      ...
    },
    "match_score": 0.85,
    "reasons": [
      "Strong Python skills match",
      "Experience level aligns perfectly",
      "Remote work opportunity"
    ]
  }
]
```

---

## Troubleshooting

### Issue: No recommendations appear

**Check 1: User has skills?**
```bash
# Check user profile
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Solution:** Add skills in profile settings

**Check 2: Jobs exist in database?**
```bash
curl http://localhost:8000/api/v1/jobs?page_size=5
```

**Solution:** Run job migration script

**Check 3: Vector store initialized?**
```bash
curl http://localhost:8000/api/v1/recommendations/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Solution:** Call initialize endpoint

---

### Issue: Backend errors

**Error: "OpenAI client not available"**
- **Cause:** OPENAI_API_KEY not set
- **Solution:** Add to .env or continue with fallback matching

**Error: "Vector store is empty"**
- **Cause:** No active jobs in database
- **Solution:** Run job migration script

**Error: "ModuleNotFoundError: No module named 'numpy'"**
- **Cause:** Dependencies not installed
- **Solution:** `pip install -r requirements.txt`

---

### Issue: Frontend errors

**Error: "Network Error" or CORS error**
- **Cause:** Backend not running or CORS misconfigured
- **Solution:** Check backend is running, verify CORS_ORIGINS in .env

**Error: "401 Unauthorized"**
- **Cause:** Not logged in or token expired
- **Solution:** Login again

**Error: No components display**
- **Cause:** Build error or missing imports
- **Solution:** Check console for errors, rebuild: `npm run dev`

---

## Testing Checklist

### ✅ Backend Tests
- [ ] Backend starts without errors
- [ ] Health check returns 200 OK
- [ ] API docs accessible at /docs
- [ ] OpenAI client initializes (or logs warning)
- [ ] Vector store can be initialized
- [ ] Recommendations endpoint returns data
- [ ] Match scores between 0 and 1
- [ ] Reasons array populated

### ✅ Frontend Tests
- [ ] Frontend starts without errors
- [ ] Login works
- [ ] Recommendations page loads
- [ ] API call succeeds
- [ ] Recommendations display
- [ ] Match scores show as percentages
- [ ] Reasons display correctly
- [ ] Filters work
- [ ] Sorting works
- [ ] Refresh button works
- [ ] Save job functionality works

### ✅ Integration Tests
- [ ] End-to-end flow works
- [ ] Error handling works
- [ ] Performance acceptable (<1s load)
- [ ] Multiple users can get recommendations
- [ ] Vector store updates reflect in recommendations

---

## Quick Commands Reference

### Backend
```bash
# Start backend
cd backend && python -m app.main

# Check health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs

# Initialize vector store
curl -X POST http://localhost:8000/api/v1/recommendations/initialize \
  -H "Authorization: Bearer TOKEN"

# Get recommendations
curl http://localhost:8000/api/v1/recommendations/jobs \
  -H "Authorization: Bearer TOKEN"

# Check system status
curl http://localhost:8000/api/v1/recommendations/status \
  -H "Authorization: Bearer TOKEN"
```

### Frontend
```bash
# Start frontend
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# View build
cd frontend && npm start
```

### Database
```bash
# Start MongoDB (if using Docker)
docker run -d -p 27017:27017 --name mongodb mongo

# Populate jobs
cd DB_ContentGen && python migrate_jobs.py
```

---

## Performance Tips

### Optimize Vector Store
```python
# Initialize vector store on startup (in app/main.py lifespan)
from app.services.recommendation_service import recommendation_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    await recommendation_service.initialize_vector_store()  # Add this
    yield
    await close_mongo_connection()
```

### Cache Recommendations (Optional)
```typescript
// In recommendations page, add caching
const [cachedRecs, setCachedRecs] = useState<JobRecommendation[]>([]);
const [lastFetch, setLastFetch] = useState<number>(0);

// Only fetch if >5 minutes since last fetch
if (Date.now() - lastFetch > 5 * 60 * 1000) {
  await fetchRecommendations();
  setLastFetch(Date.now());
}
```

---

## Next Steps

1. **Test with Real Data**
   - Create multiple user profiles
   - Add diverse job postings
   - Verify recommendation quality

2. **Monitor Performance**
   - Check API response times
   - Monitor OpenAI API costs
   - Track user engagement

3. **Gather Feedback**
   - Ask users about recommendation quality
   - Track click-through rates
   - Measure application rates

4. **Iterate**
   - Adjust match score thresholds
   - Improve prompt engineering
   - Add more features

---

## Support

### Documentation
- Implementation: `AI_RECOMMENDATIONS_IMPLEMENTATION.md`
- Integration: `FRONTEND_BACKEND_INTEGRATION_COMPLETE.md`
- API Docs: `http://localhost:8000/docs`

### Logs
- Backend: Console output
- Frontend: Browser console
- API: Check Network tab in DevTools

### Debug Mode
Enable debug logging:
```env
# In backend .env
DEBUG=True
```

---

## Success! 🎉

If everything is working:
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ✅ Users can get AI recommendations
- ✅ Match scores and reasons display
- ✅ Filters and sorting work

**You're ready to go!**

