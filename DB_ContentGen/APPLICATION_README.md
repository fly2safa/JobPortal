#!/usr/bin/env python3
"""
TalentNest Application Generator - Complete Guide

Generates realistic job applications by matching candidates with jobs.
"""

# TalentNest Application Generator

The final piece! This script generates job applications that represent candidates applying to jobs, complete with status tracking and fast-track flags.

## Features

- **Database Integration**: Pulls candidates and jobs from MongoDB
- **Smart Matching**: Pairs candidates with relevant jobs
- **AI-Generated Descriptions**: Creates personalized application/resume summaries
- **Realistic Status Distribution**: Pending, Reviewed, Rejected, Accepted
- **Date Validation**: Application date >= Job posted date
- **Fast Track Logic**: Only 10% of accepted applications get fast-tracked
- **Duplicate Support**: AppID format allows duplicates (00001-1, 00001-2)
- **Interactive CLI**: Review and accept/reject applications

## Prerequisites

**Required data in MongoDB:**
1. ✅ Candidates (from `candidate_generator.py`)
2. ✅ Employers (from `employer_generator.py`)
3. ✅ Jobs (from `job_generator.py`)
4. ➡️ **Then** run `application_generator.py`

## Installation

Uses the same virtual environment:

```bash
cd /home/jason/Python/AzNext_VibeCoding/JobPortal/DB_ContentGen
source venv/bin/activate
```

## Usage

```bash
source venv/bin/activate
python application_generator.py
```

The script will:
1. Fetch candidates from MongoDB `Candidates` collection
2. Fetch jobs from MongoDB `Jobs` collection
3. Ask how many applications to generate
4. Create applications pairing candidates with jobs
5. Generate dates, statuses, and descriptions
6. Show preview and allow accept/reject

### Example Session

```
📝  TalentNest Application Generator  📝
✅ MongoDB configured: taskmanager

🔄 Fetching data from database...
✅ Fetched 40 candidates from database
✅ Fetched 75 jobs from database

📝 How many applications would you like to generate?
   Tip: Generate 2-5 applications per candidate for realism
👉 Number of applications: 150

Would you like to:
1. Review each application individually
2. Accept all applications
3. Reject all applications

👉 Enter choice (1/2/3): 2
```

## Application Fields

Each generated application includes:

- **username**: Candidate's username (from Candidates collection)
- **app_id**: Unique identifier with duplicate support (e.g., "00001-1", "00001-2")
- **application_date**: Date applied (YYYY-MM-DD, >= job posted date)
- **status**: Application status (pending, reviewed, rejected, accepted)
- **fast_track**: Fast track flag (yes/no) - only 10% of accepted get "yes"
- **description**: AI-generated application/resume summary (3-4 sentences)

**Additional Info (for reference)**:
- job_id, job_title, company_name, candidate_name

## Application Status Distribution

Realistic distribution based on typical hiring patterns:

| Status | Percentage | Description |
|--------|-----------|-------------|
| Pending | 30% | Awaiting review |
| Reviewed | 25% | Under consideration |
| Rejected | 30% | Not selected |
| Accepted | 15% | Offer extended |

## Fast Track Logic

**Rules**:
1. ❌ Cannot be "yes" if status is NOT "accepted"
2. ✅ CAN be "yes" if status IS "accepted"
3. 🎲 Only 10% chance of "yes" for accepted applications
4. ⚡ Fast track means expedited interview/hiring process

**Example**:
- 100 accepted applications → ~10 will have fast_track: "yes"
- 100 rejected applications → 0 will have fast_track: "yes"

## Application Date Logic

**Rules**:
1. Must be >= job posted date
2. Must be <= today
3. Weighted towards earlier dates (more applications right after posting)

**Example**:
- Job posted: 2024-09-15
- Valid application dates: 2024-09-15 to 2025-01-06
- Likely date: 2024-09-20 (weighted earlier)

## AppID Format

**Format**: `00001-1`

**Breakdown**:
- `00001`: Base sequential number (5 digits)
- `-1`: Duplicate counter

**Allows Duplicates**:
- `00001-1`: First application with base 00001
- `00001-2`: Second application with base 00001 (duplicate)
- `00002-1`: First application with base 00002

**Why?** Same candidate can apply to multiple jobs.

## Example Output

```
======================================================================
APPLICATION #1
======================================================================
👤 Candidate:        Sarah Connor (@sarah.connor)
🆔 App ID:           00012-1
💼 Position:         Senior Python Developer
🏢 Company:          Quantum Penguin Systems
📅 Applied:          2024-10-05
📊 Status:           ACCEPTED
⚡ Fast Track:       YES
📋 Description:      Experienced Senior Python Developer with 8 years of 
                     expertise in Django, PostgreSQL, and cloud technologies...
======================================================================
```

## How It Works

### 1. Data Fetching
```python
candidates = fetch_from_db("Candidates")  # All candidate profiles
jobs = fetch_from_db("Jobs")              # All job postings
```

### 2. Random Pairing
- Each application randomly pairs 1 candidate with 1 job
- Same candidate can apply to multiple jobs
- Same job can receive multiple applications

### 3. Date Generation
```python
# Must be after job posting
if job_posted == "2024-09-15":
    application_date = random_date("2024-09-15", today)
    # Weighted towards earlier dates
```

### 4. Status Assignment
```python
status = random.choice_weighted(
    ["pending", "reviewed", "rejected", "accepted"],
    [0.30, 0.25, 0.30, 0.15]
)
```

### 5. Fast Track Logic
```python
if status == "accepted":
    fast_track = "yes" if random() < 0.10 else "no"  # 10% chance
else:
    fast_track = "no"  # Always no for non-accepted
```

### 6. AI Description
- Uses candidate skills, experience, education
- References job requirements
- Creates personalized cover letter excerpt
- 3-4 sentences highlighting match

## MongoDB Collection

**Database**: Uses `project_db_name` from `.env`  
**Collection**: `Applications` (capital A)

### Data Flow

```
Candidates (username, skills, experience)
    ↓
    ↓ (randomly paired)
    ↓
Applications (generated) ← AI Processing
    ↑
    ↑ (job details, posted date)
Jobs (job_id, title, company, posted_date)
```

## Output

Accepted applications are saved to:
1. **JSON file**: `generated_applications.json` (always created as backup)
2. **MongoDB**: Inserted into the `Applications` collection (if configured)

## Generation Statistics

After generation, the script shows:

```
GENERATION SUMMARY
======================================================================
Pending     :  45 ( 30.0%)
Reviewed    :  38 ( 25.3%)
Rejected    :  45 ( 30.0%)
Accepted    :  22 ( 14.7%)
Fast Track  :   2 (  1.3%)
```

This helps verify realistic distribution.

## Realistic Scenarios

### Scenario 1: Fresh Graduate
**Candidate**: 0 years experience, Junior level  
**Application**: Multiple pending applications, likely rejected  
**Fast Track**: Unlikely (not experienced enough)

### Scenario 2: Experienced Professional
**Candidate**: 8 years experience, Senior level  
**Application**: Mix of reviewed/accepted  
**Fast Track**: 10% chance if accepted (could be great fit)

### Scenario 3: High Volume
**Generate**: 200 applications  
**Result**: 30 accepted, ~3 fast-tracked  
**Realistic**: Matches typical hiring funnel

## Testing

Before generating applications, verify you have data:

```bash
source venv/bin/activate
python test_mongodb.py
```

Look for:
- ✅ `Candidates` collection with documents
- ✅ `Employers` collection with documents
- ✅ `Jobs` collection with documents
- ➡️ Ready to generate `Applications`

## Workflow Integration

```bash
# Complete workflow
1. python candidate_generator.py     # Generate 40 candidates
2. python employer_generator.py      # Generate 15 employers
3. python job_generator.py           # Generate 75 jobs
4. python application_generator.py   # Generate 150 applications

# Result: Full job portal database!
```

## Recommended Ratios

For realistic data:

| Candidates | Employers | Jobs | Applications |
|-----------|-----------|------|--------------|
| 40 | 15 | 75 | 150-200 |
| 100 | 30 | 200 | 500-800 |

**Rule of Thumb**: 2-5 applications per candidate, 2-3 applications per job

## Notes

- Candidates can apply to multiple jobs (realistic)
- Same job gets multiple applications (realistic)
- Application dates respect job posting dates
- Fast track is rare (10% of accepted only)
- Status distribution matches real hiring patterns
- AppID format supports tracking duplicates
- Descriptions are AI-generated and personalized

## Troubleshooting

### "No candidates found in database"
**Solution**: Run `candidate_generator.py` first

### "No jobs found in database"
**Solution**: Run `job_generator.py` first (requires employers too)

### "All applications have same status"
**Solution**: Generate more applications. With small samples, randomness may cluster.

### "No fast track applications"
**Solution**: Normal! Only 10% of accepted (15% of total) get fast track. Need ~70+ applications to see any.

### "Application date before job posted date"
**Solution**: This shouldn't happen. If it does, there's a bug in date logic.

## Advanced Usage

### Generate Realistic Volume
```bash
python application_generator.py
# Enter: 300 (creates full hiring funnel)
```

### Check Distribution
After generating, query MongoDB:
```javascript
// Count by status
db.Applications.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } }
])

// Find fast tracked
db.Applications.find({ fast_track: "yes" })

// Find accepted applications
db.Applications.find({ status: "accepted" })
```

## Complete Database Schema

After all generators:

```
MongoDB Database
├── Candidates (40 documents)
├── Employers (15 documents)
├── Jobs (75 documents)
└── Applications (150 documents)
    ├── References Candidates (username)
    └── References Jobs (job_id)
```

## Success Metrics

Good generation shows:
- ✅ Status distribution ~30/25/30/15
- ✅ Fast track ~1-2% of total applications
- ✅ Application dates after job posted dates
- ✅ Varied AppIDs with some duplicates
- ✅ Personalized descriptions matching skills

You now have a complete, realistic job portal database! 🎉

