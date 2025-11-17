# TalentNest Data Generators - Complete Summary

## 📁 Files Created

### Core Scripts
1. **`candidate_generator.py`** (17KB)
   - Generates job candidates with AI
   - Saves to `Candidates` collection in MongoDB
   - Creates `generated_candidates.json` backup

2. **`employer_generator.py`** (15KB)
   - Generates employers/companies with AI
   - Saves to `Employers` collection in MongoDB
   - Creates `generated_employers.json` backup

3. **`job_generator.py`**
   - Generates job postings based on candidate skills + employer data
   - Pulls from `Candidates` and `Employers` collections
   - Saves to `Jobs` collection in MongoDB
   - Creates `generated_jobs.json` backup

4. **`application_generator.py`** (FINAL PIECE!)
   - Generates job applications matching candidates to jobs
   - Pulls from `Candidates` and `Jobs` collections
   - Saves to `Applications` collection in MongoDB
   - Creates `generated_applications.json` backup
   - **Completes the minimum viable job portal database!**

### Testing & Utilities
3. **`test_mongodb.py`**
   - Tests MongoDB connection
   - Shows collections and document counts
   - Displays sample data

4. **`test_employers.py`**
   - Tests employer name generation
   - Shows sample outputs

### Documentation
5. **`README.md`** - Candidate generator docs
6. **`EMPLOYER_README.md`** - Employer generator docs
7. **`QUICK_START.md`** - Quick reference guide
8. **`SUMMARY.md`** - This file

### Configuration
9. **`requirements.txt`** - Python dependencies
10. **`.env`** - Environment variables (your API keys)
11. **`env_example.txt`** - Template for .env

## 🗄️ MongoDB Collections

### Applications Collection (FINAL!)
**Collection Name**: `Applications` (capital A)

**Fields**:
- `username` (from Candidates)
- `app_id` (unique with duplicate support: 00001-1, 00001-2)
- `application_date` (>= job posted date, YYYY-MM-DD)
- `status` (pending, reviewed, rejected, accepted)
- `fast_track` (yes/no - only 10% of accepted)
- `description` (AI-generated application/resume summary)
- `job_id`, `job_title`, `company_name`, `candidate_name` (references)

**Status Distribution**:
- Pending: 30%
- Reviewed: 25%
- Rejected: 30%
- Accepted: 15%
- Fast Track: ~1-2% (10% of accepted)

**Key Rules**:
- Application date must be >= job posted date
- Fast track can ONLY be "yes" if status is "accepted"
- Even then, only 10% chance of fast track
- AppID format allows same candidate to apply to multiple jobs

### Jobs Collection
**Collection Name**: `Jobs` (capital J)

**Fields**:
- `job_id` (unique, starts with JID)
- `job_title` (based on candidate skills)
- `company_name` (from Employers collection)
- `description` (AI-generated)
- `requirements` (array, matches candidate skills)
- `salary_range` (consistent +/- 10%)
- `location` (matches employer location)
- `remote` (On-site/Remote/Hybrid)
- `employment_type` (Full-Time/Part-Time/Contract)
- `posted_date` (past 6 months, YYYY-MM-DD)
- `app_ids_received` (empty array)

**Data Dependencies**:
- Pulls from `Candidates` (skills, experience)
- Pulls from `Employers` (company, location)

**Salary Levels**:
- Junior (0-2 yrs): $45K-$75K
- Mid (2-5 yrs): $75K-$120K
- Senior (5-8 yrs): $120K-$180K
- Lead (8-12 yrs): $150K-$220K
- Principal (12+ yrs): $180K-$280K

### Candidates Collection
**Collection Name**: `Candidates` (capital C)

**Fields**:
- `firstname`, `lastname`
- `username` (generated from name/skills)
- `password` (plaintext)
- `application` (role seeking)
- `phone_number` (555-XXXX format)
- `email` (numbers@revpro.com)
- `github_account` (github.com/numbers)
- `skills` (array)
- `experience_years` (number)
- `education` (string)
- `bio` (string)
- `apps_submitted` (empty array)
- `interview_status` (null)
- `jobs_bookmarked` (empty array)

**Example Username Patterns**:
- `john.smith`
- `sarah_connor`
- `alex_python`
- `maria_data`

### Employers Collection
**Collection Name**: `Employers` (capital E)

**Fields**:
- `company_name` (funny/creative names)
- `password` (plaintext)
- `company_description` (2-3 sentences)
- `industry` (Technology, Healthcare, etc.)
- `employee_size` (range like "51-200")
- `location` (full string: "City, State")
- `city` (string)
- `state` (abbreviation)

**Example Company Names**:
- `Quantum Penguin Systems`
- `TurboPhoenix`
- `Ninja Technologies`
- `Cyber Unicorn LLC`
- `Mega Dragon Corp`

## 🚀 Quick Commands

### Setup (One Time)
```bash
cd /home/jason/Python/AzNext_VibeCoding/JobPortal/DB_ContentGen
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Test MongoDB Connection
```bash
source venv/bin/activate
python test_mongodb.py
```

### Generate Candidates
```bash
source venv/bin/activate
python candidate_generator.py
```

### Generate Employers
```bash
source venv/bin/activate
python employer_generator.py
```

### Generate Jobs (Requires Candidates + Employers First!)
```bash
source venv/bin/activate
python job_generator.py
```

## 📊 Usage Patterns

### Single Item with Description
```
👉 Your input: Senior Python developer with ML experience
```

### Multiple Items with Number
```
👉 Your input: 10
```

Then choose:
1. Review each individually
2. Accept all
3. Reject all

## 🔑 Environment Variables Required

In `.env` file:
```bash
OPENAI_API_KEY=sk-...your-key...
project_db_url=mongodb://localhost:27017
project_db_name=taskmanager
```

## ✨ Key Features

### Both Generators Support:
- ✅ AI-powered generation with OpenAI GPT-4o-mini
- ✅ Interactive CLI with accept/reject options
- ✅ Bulk or individual generation
- ✅ Automatic MongoDB insertion
- ✅ JSON file backup
- ✅ Unique data (no duplicates)
- ✅ Realistic, diverse profiles
- ✅ Error handling and fallbacks

### Candidate-Specific:
- ✅ Smart username generation from name/skills
- ✅ Movie character alternatives
- ✅ Skill-based usernames

### Employer-Specific:
- ✅ Funny company name generation
- ✅ 30+ real US cities
- ✅ Multiple industries
- ✅ Employee size ranges

## 📈 Data Output Locations

### JSON Files (Always Created)
- `generated_candidates.json`
- `generated_employers.json`

### MongoDB Collections (If Configured)
- `Candidates` collection
- `Employers` collection

## 🎯 Typical Workflow

1. **Setup** (one time)
   ```bash
   cd DB_ContentGen
   source venv/bin/activate
   ```

2. **Test connection**
   ```bash
   python test_mongodb.py
   ```

3. **Generate employers** (10-20 companies)
   ```bash
   python employer_generator.py
   # Enter: 15
   # Choose: Accept all
   ```

4. **Generate candidates** (30-50 people)
   ```bash
   python candidate_generator.py
   # Enter: 40
   # Choose: Accept all
   ```

5. **Generate jobs** (75-200 postings)
   ```bash
   python job_generator.py
   # Enter: 100
   # Choose: Accept all
   ```

6. **Generate applications** (150-400 applications)
   ```bash
   python application_generator.py
   # Enter: 250
   # Choose: Accept all
   ```

7. **Verify in MongoDB**
   - Refresh your MongoDB client
   - Check all 4 collections: `Candidates`, `Employers`, `Jobs`, `Applications`
   - View the generated documents and relationships
   - **You now have a complete job portal database!** 🎉

## 🔧 Troubleshooting

### "MongoDB not configured"
- Check `.env` has `project_db_url` and `project_db_name`
- Not `MONGODB_URI`

### "Unable to connect to MongoDB"
- Ensure MongoDB is running
- Test with: `python test_mongodb.py`
- Check connection string

### "name 'candidates' is not defined"
- Fixed! Parameter names must match variable usage
- Both use lowercase parameters now

### Import errors in IDE
- Normal! IDE doesn't see virtual environment
- Script works fine when run with `source venv/bin/activate`

## 📝 Next Steps

1. Generate initial test data (5-10 of each)
2. Verify data appears in MongoDB
3. Generate production data volume
4. Connect to your application

## 💡 Pro Tips

- Generate employers first, then candidates
- Use "Accept all" for bulk generation to save time
- JSON files serve as backup if MongoDB fails
- Company names are unique per session
- Usernames are unique per session
- All phone numbers use 555 prefix (fictitious)
- All emails use @revpro.com domain

