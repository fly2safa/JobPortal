# Team Testing Workflow Guide v2.0

## 🎯 MongoDB Database Integration

With v2.0, the testing tracker uses **MongoDB database** for centralized test result storage. This eliminates file conflicts and enables real-time collaboration.

---

## ✅ New Workflow: Database-Based Testing

### **Prerequisites**

1. **Backend Server Running:**
   ```bash
   cd JobPortal/backend
   python -m uvicorn app.main:app --reload
   ```

2. **MongoDB Atlas Configured:**
   - Backend `.env` file has `MONGODB_URL` set
   - Database connection is active

---

### **Workflow: Real-Time Collaboration**

**Best for:** Any team size, parallel testing

#### **Step 1: Start Testing**

```
Each Tester:
  1. git pull origin dev (get latest code)
  2. Start backend server (if not running)
  3. Run test_tracker.py
  4. Enter name and browser
  5. Click "📥 Load from Database" (loads TEAM_MASTER)
  6. Start testing!
```

#### **Step 2: Save Progress**

```
Each Tester (anytime):
  1. Complete some tests
  2. Click "💾 Save to Database"
  3. Done! Results saved to MongoDB
  
  No git commits needed for test results!
```

#### **Step 3: Continue Testing**

```
Any Tester (next day or session):
  1. Run test_tracker.py
  2. Enter name and browser
  3. Click "📥 Load from Database"
  4. See latest progress from all testers
  5. Continue testing from where team left off
```

---

## 🎯 Real/Mockup Mode

### **Real Mode** (Default)
- Saves to `test_sessions` collection
- For actual testing of JobPortal
- All team members see this data

### **Mockup Mode** (Practice)
- Saves to `test_sessions_mockup` collection
- For testing the testing tracker itself
- For training new team members
- Isolated from real testing data

**To Switch:**
- Use the mode toggle in the header: `🎯 REAL Testing` / `🧪 MOCKUP/Practice`

---

## 📊 Database Collections

### **MongoDB Structure:**

```
jobportal_db
├── test_sessions           (Real testing data)
│   ├── Session 1: Alice_20241113_143022
│   ├── Session 2: Bob_20241113_150000
│   └── TEAM_MASTER (is_master=true)
│
└── test_sessions_mockup    (Practice data)
    └── Practice sessions...
```

### **What Gets Saved:**

Each session contains:
- Session ID and timestamp
- Tester name and browser
- All 40 test case results (status, notes, actual results)
- All reported bugs
- Version number

---

## 🔄 Team Collaboration Scenarios

### **Scenario 1: Parallel Testing (Same Time)**

```
9:00 AM - Alice starts testing:
  - Loads TEAM_MASTER (0 tests done)
  - Completes tests 1-10
  - Saves to database

10:00 AM - Bob starts testing:
  - Loads TEAM_MASTER (10 tests done by Alice)
  - Completes tests 11-20
  - Saves to database

11:00 AM - Charlie starts testing:
  - Loads TEAM_MASTER (20 tests done by Alice + Bob)
  - Completes tests 21-30
  - Saves to database

Result: 30 tests completed collaboratively!
```

### **Scenario 2: Distributed Testing (Different Days)**

```
Monday - Alice:
  - Tests 1-15 → Saves to database

Tuesday - Bob:
  - Loads database (has Alice's 15 tests)
  - Tests 16-30 → Saves to database

Wednesday - Charlie:
  - Loads database (has Alice + Bob's 30 tests)
  - Tests 31-40 → Saves to database

Result: All 40 tests completed over 3 days!
```

### **Scenario 3: Overlapping Tests (Conflict Resolution)**

```
Alice and Bob both test #5:
  - Alice marks it as "Pass"
  - Bob marks it as "Fail"

Database keeps both sessions:
  - Alice's session: test #5 = Pass
  - Bob's session: test #5 = Fail

Coordinator reviews both and decides:
  - Investigate why results differ
  - Re-test if needed
  - Update TEAM_MASTER with final result
```

---

## 🛠️ Troubleshooting

### **Error: "Could not connect to backend server"**

**Solution:**
1. Check if backend is running: `http://localhost:8000/docs`
2. Start backend: `python -m uvicorn app.main:app --reload`
3. Check `.env` file has correct `MONGODB_URL`

### **Error: "No TEAM_MASTER in database yet"**

**Solution:**
- This is normal for first-time use
- Start testing and save to create TEAM_MASTER
- Next person will be able to load it

### **Want to reset all test data?**

**Option 1: Use Mockup Mode**
- Switch to Mockup mode
- Test there (won't affect real data)

**Option 2: Delete from MongoDB**
- Use MongoDB Atlas web interface
- Delete documents from `test_sessions` collection
- Or use API: `DELETE /api/v1/testing/test-sessions/{id}`

---

## 📝 Best Practices

### **✅ DO:**
- Save progress frequently (every 5-10 tests)
- Load from database before starting each session
- Use descriptive notes in test results
- Report bugs immediately when found
- Use Real mode for actual testing
- Use Mockup mode for practice/training

### **❌ DON'T:**
- Don't work offline (database needs connection)
- Don't skip saving (progress won't be shared)
- Don't test without loading latest (might duplicate work)
- Don't use Mockup mode for real testing

---

## 🎓 Training New Team Members

### **Step 1: Practice with Mockup Mode**
```
1. Run test_tracker.py
2. Switch to "🧪 MOCKUP/Practice" mode
3. Practice the workflow
4. Try all features
5. Reset mockup data when done
```

### **Step 2: Start Real Testing**
```
1. Switch to "🎯 REAL Testing" mode
2. Load TEAM_MASTER
3. Start with easy tests
4. Save frequently
5. Ask questions in team chat
```

---

## 🔐 Data Security

### **Database Access:**
- Only team members with backend access can save/load
- MongoDB Atlas credentials required
- Backend must be running locally

### **Data Backup:**
- MongoDB Atlas provides automatic backups
- No manual backup needed
- All sessions are versioned in database

---

## 📊 Viewing Test Progress

### **Option 1: Testing Tracker GUI**
- Load from database
- View progress bar and stats
- See detailed test results

### **Option 2: MongoDB Atlas**
- Log into MongoDB Atlas
- Browse `test_sessions` collection
- View all sessions and data

### **Option 3: API Endpoints**
- `GET /api/v1/testing/test-sessions` - All sessions
- `GET /api/v1/testing/test-sessions/master` - TEAM_MASTER
- `GET /api/v1/testing/test-sessions?tester_name=Alice` - Alice's sessions

---

## 🚀 Migration from v1.0 (File-Based)

### **If you have existing JSON files:**

1. **Load legacy files:**
   - Use "📂 Load File" button
   - Select your old JSON file
   - All data will be loaded

2. **Save to database:**
   - Click "💾 Save to Database"
   - Your old data is now in MongoDB

3. **Continue with database:**
   - From now on, use database buttons
   - Legacy file buttons still available if needed

---

## 📞 Support

### **Issues?**
- Check backend is running: `http://localhost:8000/docs`
- Check MongoDB connection in backend logs
- Ask in team chat

### **Questions?**
- See `README.md` for detailed usage
- See `VERSION_HISTORY.md` for changelog
- Check API docs: `http://localhost:8000/docs`

---

## 🎉 Benefits of Database Integration

✅ **No more file conflicts** - Everyone works in same database  
✅ **Real-time collaboration** - See team progress instantly  
✅ **Automatic backups** - MongoDB Atlas handles it  
✅ **Version history** - All sessions are saved  
✅ **Easy querying** - Find specific tests or sessions  
✅ **Scalable** - Works for any team size  
✅ **Professional** - Industry-standard approach  

---

**Happy Testing! 🧪**
