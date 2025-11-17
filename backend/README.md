# JobPortal Backend

FastAPI-based backend for the JobPortal application.

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Database**: MongoDB with Beanie ODM
- **Authentication**: JWT with python-jose
- **AI**: OpenAI GPT-4o, LangChain, ChromaDB
- **Server**: Uvicorn

## Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account (or local MongoDB installation)
- OpenAI API key
- pip (Python package installer)

## Setup Instructions

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

#### Windows (PowerShell)
```powershell
python -m venv venv
```

#### Windows (Command Prompt)
```cmd
python -m venv venv
```

#### macOS/Linux
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment

#### Windows (PowerShell)
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Windows (Command Prompt)
```cmd
venv\Scripts\activate.bat
```

#### macOS/Linux
```bash
source venv/bin/activate
```

**Note**: You should see `(venv)` prefix in your terminal when the virtual environment is active.

### Step 4: Install Dependencies

#### All Operating Systems
```bash
pip install -r requirements.txt
```

If you encounter issues, try upgrading pip first:
```bash
python -m pip install --upgrade pip
```

### Step 5: Configure Environment Variables

#### Windows (PowerShell)
```powershell
Copy-Item .env.example .env
```

#### Windows (Command Prompt)
```cmd
copy .env.example .env
```

#### macOS/Linux
```bash
cp .env.example .env
```

Then edit the `.env` file with your actual credentials:
- `MONGODB_URI`: Your MongoDB connection string
- `SECRET_KEY`: Generate with `openssl rand -hex 32` (or use any secure random string)
- `OPENAI_API_KEY`: Your OpenAI API key
- `SMTP_*`: Email configuration (Gmail, SendGrid, etc.)

### Step 6: Run the Development Server

#### All Operating Systems
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or alternatively:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: **http://localhost:8000**

### Step 7: Verify Installation

Open your browser and navigate to:
- **Health Check**: http://localhost:8000/health
- **API Root**: http://localhost:8000/

## API Documentation

Once running, access the interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py              # Application entry point
│   ├── api/                 # API routes
│   │   └── v1/
│   │       └── routes/      # Route handlers
│   ├── core/                # Core configuration
│   ├── models/              # Database models (Beanie)
│   ├── schemas/             # Pydantic schemas
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic
│   ├── ai/                  # AI/ML features
│   ├── workers/             # Background tasks
│   ├── db/                  # Database setup
│   └── utils/               # Utilities
├── requirements.txt         # Python dependencies
└── .env.example            # Environment template
```

