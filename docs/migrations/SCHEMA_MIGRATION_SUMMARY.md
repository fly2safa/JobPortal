# Job Schema Migration Summary

## Overview
Successfully migrated the Job schema across the entire stack to ensure alignment between Database, Backend, and Frontend.

## Changes Made

### 1. Database Generator (`DB_ContentGen/job_generator.py`) ✅

**Updated job generation to match new backend schema:**

- Changed `job_title` → `title`
- Changed `salary_range` (string) → `salary_min`, `salary_max` (floats)
- Changed `remote` (string) → `is_remote` (boolean)
- Changed `employment_type` → `job_type` (enum: `full_time`, `part_time`, `contract`, etc.)
- Added `status` field (set to `"active"`)
- Added `skills`, `required_skills`, `preferred_skills` arrays
- Added `experience_level` enum (`entry`, `junior`, `mid`, `senior`, `lead`, `executive`)
- Added `experience_years_min`, `experience_years_max`
- Added `company_id`, `employer_id` (references)
- Added `application_count`, `view_count` (tracking fields)
- Added `created_at`, `updated_at` (timestamps)
- Changed collection name from `"Jobs"` → `"jobs"` (lowercase)

### 2. Database Migration Script (`DB_ContentGen/migrate_jobs.py`) ✅

**Created migration script to transform existing data:**

- Parses old salary range strings to min/max floats
- Maps employment types to backend enums
- Converts remote string to boolean
- Determines experience level from job title/requirements
- Extracts experience years from requirements
- Converts requirements array to formatted string
- Sets all existing jobs to `status="active"`
- Preserves legacy data with `_legacy_` prefixed fields
- Supports both `Jobs` and `jobs` collections
- Includes dry-run mode for safe testing

**Usage:**
```bash
# Dry run (preview only)
python3 migrate_jobs.py

# Execute migration
python3 migrate_jobs.py --execute
```

### 3. Frontend Types (`frontend/types/index.ts`) ✅

**Updated Job interface to match backend exactly:**

```typescript
export interface Job {
  // Core fields
  id: string;
  title: string;
  description: string;
  requirements?: string;  // Now string format
  responsibilities?: string;
  
  // Skills
  skills: string[];
  required_skills?: string[];
  preferred_skills?: string[];
  
  // Location
  location: string;
  is_remote: boolean;  // Was missing
  
  // Company/Employer
  company_id: string;
  company_name: string;
  employer_id: string;  // Was missing
  
  // Salary
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;  // Was missing
  
  // Job details
  job_type: 'full_time' | 'part_time' | 'contract' | 'internship' | 'temporary';  // Changed from hyphens
  experience_level: 'entry' | 'junior' | 'mid' | 'senior' | 'lead' | 'executive';  // Added junior, executive
  experience_years_min?: number;  // Was missing
  experience_years_max?: number;  // Was missing
  
  // Status
  status: 'draft' | 'active' | 'closed' | 'archived';  // Added archived
  posted_date?: string;
  closing_date?: string;  // Was missing
  
  // Tracking
  application_count: number;  // Was missing
  view_count: number;  // Was missing
  
  // Additional
  benefits?: string[];
  application_instructions?: string;  // Was missing
  
  // Metadata
  created_at: string;  // Was missing
  updated_at: string;  // Was missing
}
```

### 4. Frontend API Response Handling ✅

**Fixed API response property access:**

Changed in all files:
- ❌ `response.data` → ✅ `response.jobs` (for list endpoints)
- ❌ `response.data` → ✅ `response` (for single job endpoints)

**Files Updated:**
- `frontend/app/jobs/page.tsx`
- `frontend/app/jobs/[id]/page.tsx`
- `frontend/app/dashboard/applications/page.tsx`
- `frontend/app/dashboard/recommendations/page.tsx`
- `frontend/app/dashboard/interviews/page.tsx`
- `frontend/app/employer/jobs/[id]/applications/page.tsx`
- `frontend/app/employer/interviews/page.tsx`

### 5. Frontend Job Type Values ✅

**Changed all job_type values from hyphens to underscores:**

- ❌ `'full-time'` → ✅ `'full_time'`
- ❌ `'part-time'` → ✅ `'part_time'`

**Updated in:**
- All mock data in `frontend/app/jobs/page.tsx`
- All mock data in `frontend/app/jobs/[id]/page.tsx`
- All mock data in `frontend/app/employer/jobs/page.tsx`
- All mock data in `frontend/app/dashboard/recommendations/page.tsx`

### 6. Frontend Mock Data ✅

**Updated all mock data to include new required fields:**
- Added `is_remote` boolean
- Added `employer_id` string
- Added `application_count` number
- Added `view_count` number
- Added `created_at` timestamp
- Added `updated_at` timestamp
- Changed `requirements` from array to formatted string

## Schema Alignment Summary

### Field Mapping

| Old Schema (DB) | New Schema (All Layers) | Type | Notes |
|----------------|-------------------------|------|-------|
| `job_title` | `title` | string | Renamed |
| `salary_range` | `salary_min`, `salary_max` | float | Split into two fields |
| `remote` | `is_remote` | boolean | Type changed |
| `employment_type` | `job_type` | enum | Values changed to underscores |
| N/A | `status` | enum | **Critical - was missing!** |
| N/A | `skills` | array | **Critical - was missing!** |
| N/A | `experience_level` | enum | **Critical - was missing!** |
| N/A | `company_id` | string | **Required reference** |
| N/A | `employer_id` | string | **Required reference** |
| `requirements` | `requirements` | string | Format changed to multiline string |

## Backend Schema (Reference)

The backend uses:
- **Model:** `backend/app/models/job.py` - Job document with Beanie ODM
- **Schema:** `backend/app/schemas/job.py` - JobResponse, JobListResponse
- **Repository:** `backend/app/repositories/job_repository.py` - All queries filter by `status == "active"`
- **Routes:** `backend/app/api/v1/routes/jobs.py` - Returns JobListResponse

**Critical Backend Requirements:**
1. Jobs **must** have `status` field (default: `"draft"`, active jobs: `"active"`)
2. All queries filter by `status == JobStatus.ACTIVE`
3. Collections use lowercase `"jobs"` not `"Jobs"`

## API Response Structure

### List Endpoints (e.g., `/api/v1/jobs`)
```json
{
  "jobs": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```
Frontend accesses: `response.jobs`

### Single Job Endpoints (e.g., `/api/v1/jobs/{id}`)
```json
{
  "id": "...",
  "title": "...",
  ...
}
```
Frontend accesses: `response` directly

## Next Steps

### To Apply Database Migration:

1. Ensure dependencies are installed:
```bash
cd /Users/dari/Documents/Revature/JobPortal/DB_ContentGen
pip3 install pymongo python-dotenv
```

2. Set environment variables in `.env`:
```
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=your_database_name
```

3. Run dry-run first:
```bash
python3 migrate_jobs.py
```

4. If preview looks good, execute:
```bash
python3 migrate_jobs.py --execute
```

### To Generate New Jobs:

1. Use the updated job_generator.py:
```bash
cd /Users/dari/Documents/Revature/JobPortal/DB_ContentGen
python3 job_generator.py
```

New jobs will automatically be created with the correct schema.

### To Test Frontend:

1. Start backend server:
```bash
cd /Users/dari/Documents/Revature/JobPortal/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

2. Start frontend:
```bash
cd /Users/dari/Documents/Revature/JobPortal/frontend
npm run dev
```

3. Navigate to `http://localhost:3000/jobs` to see jobs

## Verification Checklist

- ✅ Database generator creates new schema
- ✅ Migration script transforms old data
- ✅ Frontend types match backend exactly
- ✅ API response handling is correct
- ✅ Job type values use underscores
- ✅ Mock data includes all required fields
- ⏳ Run database migration
- ⏳ Test end-to-end: DB → API → Frontend
- ⏳ Verify jobs display correctly

## Common Issues & Solutions

### Issue: Jobs not showing up
**Cause:** Missing `status` field in database
**Solution:** Run migration script to add `status="active"`

### Issue: Type errors in frontend
**Cause:** Interface mismatch
**Solution:** All fixed - types now match backend exactly

### Issue: API returns data but frontend shows empty
**Cause:** Accessing wrong property (`response.data` vs `response.jobs`)
**Solution:** All fixed - using correct properties now

### Issue: Job type validation errors
**Cause:** Frontend using hyphens, backend expecting underscores
**Solution:** All fixed - using underscored values now

## Files Modified

### Backend (No Changes Needed ✅)
The backend was already correctly implemented.

### Database
- ✅ `DB_ContentGen/job_generator.py` - Updated to generate new schema
- ✅ `DB_ContentGen/migrate_jobs.py` - Created migration script

### Frontend
- ✅ `frontend/types/index.ts` - Updated Job interface
- ✅ `frontend/app/jobs/page.tsx` - Fixed API handling & mock data
- ✅ `frontend/app/jobs/[id]/page.tsx` - Fixed API handling & mock data
- ✅ `frontend/app/dashboard/applications/page.tsx` - Fixed API handling
- ✅ `frontend/app/dashboard/recommendations/page.tsx` - Fixed API handling & mock data
- ✅ `frontend/app/dashboard/interviews/page.tsx` - Fixed API handling
- ✅ `frontend/app/employer/jobs/page.tsx` - Fixed mock data
- ✅ `frontend/app/employer/jobs/[id]/applications/page.tsx` - Fixed API handling
- ✅ `frontend/app/employer/interviews/page.tsx` - Fixed API handling

## Documentation
- ✅ `SCHEMA_MIGRATION_SUMMARY.md` - This file

