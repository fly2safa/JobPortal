# TalentNest Job Generator

A Python script that generates fictitious job postings for the TalentNest job portal by intelligently matching candidate skills with employer information from the database.

## Features

- **Database Integration**: Pulls candidates and employers from MongoDB
- **Smart Matching**: Creates relevant jobs based on candidate skills
- **AI-Powered Descriptions**: Uses OpenAI to generate realistic job descriptions
- **Salary Consistency**: Similar jobs have +/- 10% salary variance
- **Interactive CLI**: Review and accept/reject jobs individually or in bulk
- **Unique Job IDs**: Auto-generated IDs starting with "JID"
- **Realistic Dates**: Posted dates within past 6 months
- **Persistent Storage**: Saves to JSON file and MongoDB

## Prerequisites

**You must have data in MongoDB first:**
1. Run `candidate_generator.py` to create candidates
2. Run `employer_generator.py` to create employers
3. Then run `job_generator.py` to create jobs

## Installation

Uses the same virtual environment:

```bash
cd /home/jason/Python/AzNext_VibeCoding/JobPortal/DB_ContentGen
source venv/bin/activate
```

## Usage

```bash
source venv/bin/activate
python job_generator.py
```

The script will:
1. Fetch candidates from MongoDB `Candidates` collection
2. Fetch employers from MongoDB `Employers` collection
3. Ask how many jobs to generate
4. Create jobs by matching candidate skills with employers
5. Show preview and allow accept/reject

### Example Session

```
💼  TalentNest Job Generator  💼
✅ MongoDB configured: taskmanager

🔄 Fetching data from database...
✅ Fetched 30 candidates from database
✅ Fetched 15 employers from database

📝 How many job postings would you like to generate?
👉 Number of jobs: 20

Would you like to:
1. Review each job individually
2. Accept all jobs
3. Reject all jobs

👉 Enter choice (1/2/3): 2
```

## Job Fields

Each generated job includes:

- **job_id**: Unique identifier (e.g., "JID12345")
- **job_title**: Role title based on primary skill (e.g., "Senior Python Developer")
- **company_name**: Pulled from employer database
- **description**: 3-4 sentence AI-generated description
- **requirements**: List of 5-7 specific requirements matching candidate skills
- **salary_range**: Based on experience level with consistency (+/- 10%)
- **location**: Matches employer's location
- **remote**: On-site, Remote, or Hybrid
- **employment_type**: Full-Time, Part-Time, or Contract
- **posted_date**: Random date within past 6 months (YYYY-MM-DD)
- **app_ids_received**: Empty array (for future applicant tracking)

## Salary Ranges by Experience Level

The script automatically determines salary based on candidate experience:

| Level | Years Experience | Salary Range |
|-------|-----------------|--------------|
| Junior | 0-2 years | $45,000 - $75,000 |
| Mid | 2-5 years | $75,000 - $120,000 |
| Senior | 5-8 years | $120,000 - $180,000 |
| Lead | 8-12 years | $150,000 - $220,000 |
| Principal | 12+ years | $180,000 - $280,000 |

**Consistency**: Similar job titles get similar salaries with only +/- 10% variance.

## Example Output

```
======================================================================
JOB POSTING #1
======================================================================
🆔 Job ID:           JID12456
💼 Title:            Senior Python Developer
🏢 Company:          Quantum Penguin Systems
📋 Description:      Quantum Penguin Systems is seeking a Senior Python Developer 
                     to join our AI team...
✅ Requirements:     7 items
                     1. 5+ years of Python development experience
                     2. Strong knowledge of Django or Flask frameworks
                     3. Experience with PostgreSQL and MongoDB
                     ... and 4 more
💰 Salary:           $125,000 - $175,000
📍 Location:         San Francisco, CA
🏠 Remote:           Hybrid
⏰ Type:             Full-Time
📅 Posted:           2024-09-15
======================================================================
```

## How It Works

### 1. Data Fetching
```python
candidates = fetch_from_db("Candidates")  # Gets skills, experience
employers = fetch_from_db("Employers")    # Gets company info, location
```

### 2. Intelligent Matching
- Randomly pairs a candidate with an employer
- Uses candidate's primary skills for job title
- Matches employer's location to job location
- Correlates experience level with job seniority

### 3. AI Generation
- Sends skills + company context to OpenAI
- Generates realistic job title, description, requirements
- Ensures company name appears in description

### 4. Salary Calculation
- Determines level from candidate experience
- Uses base ranges with +/- 10% variance
- Caches similar jobs for consistency
- Rounds to nearest $5,000

### 5. Date Generation
- Random date between today and 6 months ago
- Format: YYYY-MM-DD
- Realistic distribution

## MongoDB Collection

**Database**: Uses `project_db_name` from `.env`  
**Collection**: `Jobs` (capital J)

### Data Dependencies

```
Candidates (collection)
    ↓ (pulls skills, experience)
    ↓
Jobs (generated) ← AI Processing
    ↑
    ↑ (pulls company, location)
Employers (collection)
```

## Output

Accepted jobs are saved to:
1. **JSON file**: `generated_jobs.json` (always created as backup)
2. **MongoDB**: Inserted into the `Jobs` collection (if configured)

## Testing

Before generating jobs, verify you have data:

```bash
source venv/bin/activate
python test_mongodb.py
```

Look for:
- ✅ `Candidates` collection with documents
- ✅ `Employers` collection with documents

## Example Matching Logic

**Candidate**:
- Skills: Python, Django, PostgreSQL
- Experience: 6 years
- Level: Senior

**Employer**:
- Company: Quantum Penguin Systems
- Location: San Francisco, CA
- Industry: Technology

**Generated Job**:
- Title: Senior Python Developer
- Requirements: Python, Django, PostgreSQL, 5+ years, etc.
- Salary: $125,000 - $175,000 (senior level)
- Location: San Francisco, CA (matches employer)
- Remote: Hybrid (random)

## Remote Options

- **On-site**: Must be in office
- **Remote**: Work from anywhere
- **Hybrid**: Mix of office and remote

## Employment Types

- **Full-Time**: Standard 40 hours/week
- **Part-Time**: Less than 40 hours/week
- **Contract**: Fixed-term engagement

## Notes

- Requires existing candidates and employers in database
- Each job matches real candidate skills with real employer info
- Salary consistency ensures similar roles have similar pay
- Location always matches the employer's location
- Posted dates are realistic (past 6 months)
- Job IDs are unique and sequential (JID prefix)

## Workflow

```bash
# 1. Generate candidates first
python candidate_generator.py
# Enter: 30

# 2. Generate employers
python employer_generator.py
# Enter: 15

# 3. Generate jobs (this script)
python job_generator.py
# Enter: 50

# Result: 50 jobs matching 30 candidates with 15 employers
```

## Advanced Usage

### Generate Many Jobs
```bash
python job_generator.py
# Enter: 100 (creates 100 unique job postings)
```

### Check Distribution
After generating, check the variety:
- Different job titles
- Various salary ranges
- Mix of remote options
- Different companies
- Various locations

## Troubleshooting

### "No candidates found in database"
**Solution**: Run `candidate_generator.py` first

### "No employers found in database"
**Solution**: Run `employer_generator.py` first

### "All jobs have same salary"
**Solution**: This shouldn't happen due to caching with variance. If it does, check that candidates have varied experience levels.

### "Jobs don't match candidate skills"
**Solution**: Verify candidates have skills populated. Check `test_mongodb.py` output.

