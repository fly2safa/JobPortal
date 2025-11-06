# Quick Start Guide - TalentNest Data Generators

Generate both **Candidates** and **Employers** for your TalentNest job portal!

## ✅ Setup Checklist

### 1. Check Your .env File
Make sure `/home/jason/Python/AzNext_VibeCoding/JobPortal/DB_ContentGen/.env` contains:

```bash
OPENAI_API_KEY=your_actual_openai_key_here
project_db_url=mongodb://your_connection_string_here
project_db_name=your_database_name_here
```

### 2. Activate Virtual Environment
```bash
cd /home/jason/Python/AzNext_VibeCoding/JobPortal/DB_ContentGen
source venv/bin/activate
```

### 3. Test MongoDB Connection (Optional but Recommended)
```bash
python test_mongodb.py
```

This will show:
- ✅ If MongoDB connection works
- 📚 List of collections in your database
- 👥 Number of existing candidates

### 4. Generate Data

**For Candidates:**
```bash
python candidate_generator.py
```

**For Employers:**
```bash
python employer_generator.py
```

## 🚀 Usage Examples

### Candidates

### Generate a Single Candidate
```
👉 Your input: Senior Python developer with 5 years experience in ML
```

### Generate Multiple Candidates
```
👉 Your input: 10
```

Then choose:
1. Review each individually
2. Accept all
3. Reject all

### Employers

### Generate a Single Employer
```
👉 Your input: Tech startup focused on AI and machine learning
```

### Generate Multiple Employers
```
👉 Your input: 5
```

Then choose to review individually or accept/reject all.

## 🔍 Troubleshooting

### Issue: "Unable to connect to MongoDB"

**Check:**
1. Is your MongoDB server running?
2. Is the `project_db_url` correct in `.env`?
3. Can you access MongoDB from your machine?

**Test with:**
```bash
python test_mongodb.py
```

### Issue: "OPENAI_API_KEY not found"

**Fix:**
1. Create or edit `.env` file in DB_ContentGen directory
2. Add: `OPENAI_API_KEY=sk-...your-key...`
3. Save the file

### Issue: Import errors

**Fix:**
```bash
cd /home/jason/Python/AzNext_VibeCoding/JobPortal/DB_ContentGen
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 Where Is My Data?

Your accepted data is saved to **TWO** locations:

### Candidates
1. **JSON File**: `generated_candidates.json`
   - Always created as a backup
   - Human-readable format
   - Located in DB_ContentGen directory

2. **MongoDB**: Database collection named `Candidates`
   - Only if MongoDB is configured in `.env`
   - Check with: `python test_mongodb.py`
   - Refresh your MongoDB client to see new entries

### Employers
1. **JSON File**: `generated_employers.json`
   - Always created as a backup
   - Human-readable format
   - Located in DB_ContentGen directory

2. **MongoDB**: Database collection named `Employers`
   - Only if MongoDB is configured in `.env`
   - Refresh your MongoDB client to see new entries

## 🎯 Expected Output When Saving

```
✅ Saved 1 candidate(s) to generated_candidates.json
📊 Total candidates in file: 5

🔄 Connecting to MongoDB...
✅ Connected to MongoDB successfully!
✅ Inserted 1 candidate into MongoDB
   Document ID: 507f1f77bcf86cd799439011
📊 Total candidates in MongoDB collection: 5
```

If you see this output, your candidates ARE in MongoDB! 

Refresh your MongoDB client (Compass, Studio 3T, etc.) to see them.

## 💡 Pro Tips

1. **Always activate venv first**: `source venv/bin/activate`
2. **Test MongoDB before generating**: `python test_mongodb.py`
3. **Check JSON file if unsure**: `cat generated_candidates.json`
4. **Generate test data**: Create 1 candidate first to test the flow

