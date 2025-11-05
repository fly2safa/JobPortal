# JobPortal Implementation Plan

## Timeline: 2 Weeks | Team: 6 Developers | Branch Strategy: Feature branches → dev → main

---

## Phase 1: Foundation & Infrastructure (Days 1-3)

### Goals
- Project scaffolding (backend + frontend)
- Database models and authentication
- Docker setup
- Core UI components

### Team Split (Parallel Work)

**Team Member 1 & 2: Backend Foundation**
- Branch: `feat/backend-setup`
- Initialize FastAPI project structure following spec
- Set up `app/main.py`, `app/core/config.py`, `app/core/security.py`, `app/core/logging.py`
- Configure MongoDB connection in `app/db/init_db.py`
- Create base models: `app/models/user.py`, `app/models/company.py`
- Implement JWT authentication in `app/api/v1/routes/auth.py`
- Create user registration/login endpoints
- Add password hashing (bcrypt) and token generation
- Set up Swagger docs at `/docs`

**Team Member 3 & 4: Frontend Foundation**
- Branch: `feat/frontend-setup`
- Initialize Next.js 14 with App Router and TypeScript
- Configure Tailwind CSS
- Create folder structure: `app/`, `components/`, `features/`, `hooks/`, `lib/`, `store/`, `types/`
- Build reusable components: Button, Input, Card, Modal, Navbar
- Implement auth store (Zustand/Redux) for token management
- Create auth pages: `/app/login/page.tsx`, `/app/register/page.tsx`
- Set up API client in `lib/api.ts` with JWT interceptor
- Create auth feature: `features/auth/` with login/register forms

**Team Member 5: Database Models**
- Branch: `feat/database-models`
- Create all Beanie models in `app/models/`:
  - `job.py` (title, description, skills, location, company_id, salary, posted_date, status)
  - `application.py` (job_id, user_id, resume_id, status, applied_date, cover_letter)
  - `resume.py` (user_id, file_url, parsed_text, skills_extracted, created_date)
  - `conversation.py` (user_id, messages, created_date)
- Register all models in `app/db/init_db.py`
- Create indexes in `app/db/indexes.py`

**Team Member 6: Docker & DevOps**
- Branch: `feat/docker-setup`
- Create `backend/Dockerfile` (Python 3.11+, FastAPI, Uvicorn)
- Create `frontend/Dockerfile` (Node.js, Next.js build)
- Create `docker-compose.yml` (backend, frontend, optional local MongoDB)
- Create `.env.example` for both backend and frontend
- Document setup instructions in root `README.md`

**Deliverables:**
- Working auth system (register, login, JWT)
- Database models registered
- Docker containers running
- Basic UI components and auth pages

---

## Phase 2: Core Features - Job Seeker & Employer (Days 4-7)

### Goals
- Job seeker profile and job search
- Employer job posting and application review
- Resume upload and parsing (AI)
- Application submission

### Team Split (Parallel Work)

**Team Member 1: Job Seeker Profile & Resume**
- Branch: `feat/job-seeker-profile`
- Backend:
  - `app/api/v1/routes/users.py` - profile CRUD
  - `app/services/resume_parser.py` - AI resume parsing using OpenAI GPT-4o
  - `app/repositories/resume_repository.py`
  - Resume upload endpoint (parse PDF/DOCX, extract skills, experience)
- Frontend:
  - `features/profile/` - profile form, resume upload component
  - `app/dashboard/profile/page.tsx`

**Team Member 2: Job Search & Listings**
- Branch: `feat/job-search`
- Backend:
  - `app/api/v1/routes/jobs.py` - search, filter, get job details
  - `app/services/search_service.py` - search by title, skills, location, company
  - `app/repositories/job_repository.py`
- Frontend:
  - `features/jobs/` - job card, job list, search filters
  - `app/jobs/page.tsx` - job listings with search/filter
  - `app/jobs/[id]/page.tsx` - job details page

**Team Member 3: Job Application System**
- Branch: `feat/job-applications`
- Backend:
  - `app/api/v1/routes/applications.py` - apply, view status, history
  - `app/services/application_service.py`
  - `app/repositories/application_repository.py`
- Frontend:
  - `features/applications/` - application form, status tracker
  - `app/dashboard/applications/page.tsx` - application history
  - Apply button integration on job details page

**Team Member 4: Employer Job Posting**
- Branch: `feat/employer-job-posting`
- Backend:
  - Extend `app/api/v1/routes/jobs.py` - create, update, delete jobs
  - Add employer-specific endpoints
- Frontend:
  - `features/employer/` - job post form, job management
  - `app/employer/dashboard/page.tsx`
  - `app/employer/jobs/new/page.tsx` - create job posting
  - `app/employer/jobs/[id]/edit/page.tsx`

**Team Member 5: Employer Application Review**
- Branch: `feat/employer-applications`
- Backend:
  - Extend `app/api/v1/routes/applications.py` - view applications per job, shortlist, reject
  - Application status updates
- Frontend:
  - `features/employer/applications/` - application list, candidate cards
  - `app/employer/jobs/[id]/applications/page.tsx`
  - Shortlist/reject actions

**Team Member 6: Email Notifications**
- Branch: `feat/email-notifications`
- Backend:
  - `app/services/email_service.py` - send emails via SMTP or SendGrid
  - `app/workers/tasks/email_tasks.py` - background email sending
  - Trigger emails on: application submitted, status change, job alert
- Create email templates for notifications

**Deliverables:**
- Job seekers can create profiles, upload resumes (AI parsed), search jobs, apply
- Employers can post jobs, view applications, shortlist candidates
- Email notifications working

---

## Phase 3: AI Features & Advanced Functionality (Days 8-11)

### Goals
- AI job recommendations for job seekers
- AI candidate matching for employers
- Cover letter generation
- RAG-based AI assistant
- Interview scheduling

### Team Split (Parallel Work)

**Team Member 1 & 2: AI Recommendations (Job Seeker)**
- Branch: `feat/ai-job-recommendations`
- Backend:
  - `app/ai/providers/openai_client.py` - OpenAI API client
  - `app/ai/chains/recommendation_chain.py` - LangChain prompt chain
  - `app/ai/rag/embeddings.py` - text-embedding-3-small for job embeddings
  - `app/ai/rag/vectorstore.py` - ChromaDB setup
  - `app/services/recommendation_service.py` - match user profile to jobs
  - `app/api/v1/routes/recommendations.py` - get personalized recommendations
- Frontend:
  - `features/recommendations/` - recommendation cards
  - `app/dashboard/recommendations/page.tsx`

**Team Member 3 & 4: AI Candidate Matching (Employer)**
- Branch: `feat/ai-candidate-matching`
- Backend:
  - Extend `app/ai/chains/` - candidate matching chain
  - `app/services/candidate_matching_service.py` - rank candidates by job requirements
  - Endpoint: `/api/v1/jobs/{job_id}/recommended-candidates`
- Frontend:
  - `features/employer/candidate-recommendations/`
  - Display ranked candidates on employer job detail page

**Team Member 5: AI Assistant & Cover Letter**
- Branch: `feat/ai-assistant`
- Backend:
  - `app/ai/rag/loader.py`, `splitter.py`, `retriever.py`, `qa_chain.py` - RAG pipeline
  - `app/models/conversation.py` - store chat history
  - `app/api/v1/routes/assistant.py` - chat endpoint
  - Cover letter generation endpoint using GPT-4o
- Frontend:
  - `features/assistant/` - chat interface
  - `app/dashboard/assistant/page.tsx`
  - Cover letter generator in application form

**Team Member 6: Interview Scheduling**
- Branch: `feat/interview-scheduling`
- Backend:
  - `app/models/interview.py` - interview model (job_id, application_id, scheduled_time, status)
  - `app/api/v1/routes/interviews.py` - schedule, update, cancel
  - Email notifications for interview invites
- Frontend:
  - `features/interviews/` - calendar view, interview cards
  - `app/employer/interviews/page.tsx`
  - `app/dashboard/interviews/page.tsx` (job seeker view)

**Deliverables:**
- AI job recommendations for job seekers
- AI candidate matching for employers
- RAG-based AI assistant
- Cover letter generation
- Interview scheduling with email notifications

---

## Phase 4: Polish, Testing & Deployment (Days 12-14)

### Goals
- UI/UX refinement
- Error handling and validation
- Testing (manual + basic automated)
- Documentation (ERD, Architecture Diagram)
- Deployment preparation

### Team Split (Parallel Work)

**Team Member 1 & 2: Testing & Bug Fixes**
- Branch: `fix/testing-bugs`
- Manual testing of all features
- Fix bugs, edge cases, validation errors
- Add input validation across all forms
- Implement proper error handling and user feedback (toasts, error messages)
- Test Docker deployment locally

**Team Member 3 & 4: UI/UX Polish**
- Branch: `feat/ui-polish`
- Responsive design testing (mobile, tablet, desktop)
- Consistent styling with Tailwind
- Loading states, skeleton screens
- Empty states for lists
- Accessibility improvements (ARIA labels, keyboard navigation)
- Dark mode (optional, if time permits)

**Team Member 5: Documentation**
- Branch: `docs/diagrams-readme`
- Create ERD diagram (MongoDB collections and relationships)
- Create Architecture Diagram (frontend ↔ backend ↔ MongoDB ↔ OpenAI/ChromaDB)
- Update root `README.md` with:
  - Project overview
  - Tech stack
  - Setup instructions
  - Environment variables
  - Running with Docker
  - API documentation link
- Create `CONTRIBUTING.md` with branch strategy and PR guidelines

**Team Member 6: Deployment Preparation**
- Branch: `feat/deployment`
- Set up structured logging across backend
- Add health check endpoints (`/health`, `/ready`)
- Optimize Docker images (multi-stage builds)
- Prepare deployment scripts
- Environment variable validation on startup
- Rate limiting on critical endpoints
- Security headers (CORS, CSP)

**Final Integration:**
- All branches merge to `dev`
- Full team testing on `dev`
- Create PR from `dev` to `main`
- Tag release `v1.0.0`

**Deliverables:**
- Fully tested, polished application
- ERD and Architecture diagrams
- Complete documentation
- Docker deployment ready
- Demo-ready application

---

## Branch Strategy

### Workflow
1. All features branch from `dev`
2. Branch naming: `feat/<feature-name>`, `fix/<bug-name>`, `docs/<doc-name>`
3. Daily: Pull latest `dev`, rebase feature branches
4. PR to `dev` with at least 1 reviewer approval
5. Squash and merge to keep history clean
6. After Phase 4: PR `dev` → `main` for release

### Example Commands
```bash
# Start new feature
git checkout dev && git pull --ff-only
git checkout -b feat/job-search
# ... work, commit ...
git push -u origin HEAD
# Open PR to dev on GitHub

# Keep feature branch updated
git fetch origin
git rebase origin/dev
git push --force-with-lease
```

---

## Key Technical Decisions

### Backend
- **FastAPI** with async/await for high performance
- **Beanie ODM** for MongoDB with Pydantic validation
- **JWT** authentication with httpOnly cookies or Bearer tokens
- **LangChain** for AI orchestration
- **ChromaDB** for vector storage (embeddings)
- **OpenAI GPT-4o** for AI features, **text-embedding-3-small** for embeddings

### Frontend
- **Next.js 14 App Router** for modern React patterns
- **TypeScript** for type safety
- **Tailwind CSS** for rapid, consistent styling
- **Zustand** or **Redux** for state management
- **React Hook Form** for form handling
- **Axios** or **fetch** with JWT interceptor

### Database Schema (MongoDB Collections)
- `users` - job seeker/employer accounts
- `companies` - employer company profiles
- `jobs` - job postings
- `applications` - job applications
- `resumes` - uploaded resumes with parsed data
- `conversations` - AI assistant chat history
- `interviews` - scheduled interviews

---

## Environment Variables

### Backend `.env`
```
MONGODB_URI=mongodb+srv://...
DATABASE_NAME=jobportal
SECRET_KEY=<jwt-secret>
OPENAI_API_KEY=sk-...
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASSWORD=...
```

### Frontend `.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Success Criteria (Definition of Done)

✅ Fully working demo with all core features  
✅ Job seekers can register, create profiles, upload resumes, search jobs, apply  
✅ Employers can register, post jobs, review applications, schedule interviews  
✅ AI recommendations and candidate matching working  
✅ Email notifications functional  
✅ Docker deployment ready  
✅ ERD and Architecture diagrams in repo  
✅ Clean, documented code with proper error handling  
✅ Responsive UI with Tailwind CSS  

---

## Risk Mitigation

- **AI API rate limits**: Cache embeddings, implement retry logic
- **Time constraints**: Prioritize core features; AI assistant is lower priority if time runs short
- **Merge conflicts**: Daily syncs with `dev`, small PRs
- **Testing gaps**: Focus manual testing on critical paths (auth, apply, post job)

---

## Daily Standups (Recommended)

- **What did you complete yesterday?**
- **What are you working on today?**
- **Any blockers?**
- **Merge conflicts or dependencies?**

Keep PRs small, merge frequently to `dev`, and communicate blockers immediately in your team channel.

