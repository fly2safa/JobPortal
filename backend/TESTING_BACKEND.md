# Backend Testing Guide

This guide provides instructions for testing the JobPortal backend API.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Database Connection Testing](#database-connection-testing)
- [Running the Development Server](#running-the-development-server)
- [Testing Authentication Endpoints](#testing-authentication-endpoints)
- [Using Swagger UI (Interactive Testing)](#using-swagger-ui-interactive-testing)
- [Using Command Line (PowerShell/Bash)](#using-command-line-powershellbash)
- [Common Issues and Solutions](#common-issues-and-solutions)

---

## Prerequisites

1. **Virtual Environment Activated**
   
   **Windows PowerShell:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

2. **Dependencies Installed**
   
   **Windows PowerShell:**
   ```powershell
   pip install -r requirements.txt
   ```
   
   **macOS/Linux:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables Configured**
   - Copy `.env.example` to `.env` (if exists) or create `.env` file
   - Required variables:
     ```env
     MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
     DATABASE_NAME=TalentNest
     SECRET_KEY=your-secret-key-here-change-in-production
     ```
   - Optional variables (can be omitted for basic testing):
     ```env
     OPENAI_API_KEY=your-openai-key
     SMTP_USER=your-email@example.com
     SMTP_PASSWORD=your-password
     SMTP_FROM_EMAIL=noreply@jobportal.com
     ```

---

## Database Connection Testing

### Test Script: `test_connectivity_to_mongoDB.py`

This script verifies that the backend can connect to MongoDB Atlas.

**Run the test:**

**Windows PowerShell:**
```powershell
python test_connectivity_to_mongoDB.py
```

**macOS/Linux:**
```bash
python test_connectivity_to_mongoDB.py
```

**Expected Output:**
```
INFO - Testing MongoDB connection...
INFO - Connecting to MongoDB at <YourDatabaseName>...
INFO - Successfully connected to MongoDB and initialized Beanie
INFO - Database connection test PASSED!
INFO - MongoDB connection closed
```

**If you see errors:**
- Check your `MONGODB_URI` in `.env` file
- Verify MongoDB Atlas credentials are correct
- Ensure your IP address is whitelisted in MongoDB Atlas (Network Access)
- Check if special characters in password are URL-encoded

---

## Running the Development Server

### Start the Server

**Windows PowerShell:**
```powershell
# From the backend directory
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**macOS/Linux:**
```bash
# From the backend directory
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Verify Server is Running

**Health Check:**

**Windows PowerShell:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
```

**macOS/Linux:**
```bash
curl http://127.0.0.1:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "app": "JobPortal",
  "version": "1.0.0"
}
```

---

## Testing Authentication Endpoints

### Test Script: `test_auth_endpoint.py`

This script tests user creation directly in the database.

**Run the test:**

**Windows PowerShell:**
```powershell
python test_auth_endpoint.py
```

**macOS/Linux:**
```bash
python test_auth_endpoint.py
```

**Expected Output:**
```
INFO - Connecting to MongoDB...
INFO - Connected successfully!
INFO - Creating test user...
INFO - User created successfully! ID: <user_id>
INFO - Total users in database: 1
INFO - Test completed successfully!
```

---

## Using Swagger UI (Interactive Testing)

Swagger UI provides an interactive interface to test all API endpoints.

### Access Swagger UI

1. Start the development server
2. Open your browser and navigate to: **http://127.0.0.1:8000/docs**
3. You'll see all available endpoints with documentation

### Test User Registration

1. Find **POST /api/v1/auth/register**
2. Click **"Try it out"**
3. Fill in the request body:
   ```json
   {
     "email": "test@example.com",
     "password": "SecurePass123",
     "first_name": "John",
     "last_name": "Doe",
     "role": "job_seeker"
   }
   ```
4. Click **"Execute"**
5. Check the response (should be 201 Created with user data)

### Test User Login

1. Find **POST /api/v1/auth/login**
2. Click **"Try it out"**
3. Fill in the request body:
   ```json
   {
     "email": "test@example.com",
     "password": "SecurePass123"
   }
   ```
4. Click **"Execute"**
5. Copy the `access_token` from the response

### Test Protected Endpoint (Get Current User)

1. Click the **"Authorize"** button at the top of Swagger UI
2. Enter: `Bearer <your_access_token>`
3. Click **"Authorize"** then **"Close"**
4. Find **GET /api/v1/auth/me**
5. Click **"Try it out"** then **"Execute"**
6. You should see your user information

---

## Using Command Line

### Windows PowerShell

**Register a User:**
```powershell
$body = @{
    email = "test@example.com"
    password = "SecurePass123"
    first_name = "John"
    last_name = "Doe"
    role = "job_seeker"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/auth/register" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

**Login:**
```powershell
$body = @{
    email = "test@example.com"
    password = "SecurePass123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/auth/login" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

$token = $response.access_token
Write-Host "Token: $token"
```

**Get Current User (Protected Route):**
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/v1/auth/me" `
    -Method Get `
    -Headers $headers
```

### macOS/Linux (Bash/cURL)

**Register a User:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "role": "job_seeker"
  }'
```

**Login:**
```bash
TOKEN=$(curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123"
  }' | jq -r '.access_token')

echo "Token: $TOKEN"
```

**Get Current User:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Common Issues and Solutions

### Issue 1: "Module not found" errors

**Solution:**

**Windows PowerShell:**
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: "Authentication failed" when connecting to MongoDB

**Possible causes:**
1. Incorrect username/password in `MONGODB_URI`
2. Special characters in password not URL-encoded
3. IP address not whitelisted in MongoDB Atlas

**Solution:**
- Verify credentials in MongoDB Atlas
- URL-encode special characters in password:
  - `@` → `%40`
  - `#` → `%23`
  - `$` → `%24`
  - `:` → `%3A`
  - `/` → `%2F`
- Add `0.0.0.0/0` to IP whitelist in MongoDB Atlas (for testing)

### Issue 3: "Internal Server Error" (500) on authentication endpoints

**Possible causes:**
1. `bcrypt` version incompatibility with `passlib`
2. Database connection not established

**Solution:**

**Windows PowerShell:**
```powershell
# Ensure bcrypt version 4.1.2 is installed
pip install bcrypt==4.1.2

# Restart the server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**macOS/Linux:**
```bash
# Ensure bcrypt version 4.1.2 is installed
pip install bcrypt==4.1.2

# Restart the server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Issue 4: "Field required" errors for SMTP or OpenAI

**Solution:**
These fields are optional. Make sure your `app/core/config.py` has them marked as `Optional`:
```python
OPENAI_API_KEY: Optional[str] = None
SMTP_USER: Optional[str] = None
SMTP_PASSWORD: Optional[str] = None
SMTP_FROM_EMAIL: Optional[str] = None
```

### Issue 5: Server not accessible from other machines

**Solution:**
Change host from `127.0.0.1` to `0.0.0.0`:

**Windows PowerShell:**
```powershell
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**macOS/Linux:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Issue 6: Port 8000 already in use

**Solution:**

**Windows PowerShell:**
```powershell
# Find and kill process using port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# Or use a different port
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

**macOS/Linux:**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

---

## API Documentation

- **Swagger UI (Interactive)**: http://127.0.0.1:8000/docs
- **ReDoc (Read-only)**: http://127.0.0.1:8000/redoc

---

## Testing Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `.env` file configured with MongoDB URI
- [ ] Database connection test passes (`test_connectivity_to_mongoDB.py`)
- [ ] Server starts without errors
- [ ] Health endpoint responds
- [ ] User registration works
- [ ] User login returns JWT token
- [ ] Protected endpoint (`/me`) works with JWT token
- [ ] Swagger UI accessible and functional

---

## Need Help?

If you encounter issues not covered here:
1. Check the server logs for detailed error messages
2. Verify all environment variables are set correctly
3. Ensure MongoDB Atlas is accessible (check Network Access settings)
4. Review the main `README.md` for setup instructions
5. Contact the team for assistance

---

**Happy Testing! 🚀**

