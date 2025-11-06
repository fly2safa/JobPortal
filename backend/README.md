# JobPortal Backend

FastAPI-based backend for the JobPortal application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure your environment variables:
```bash
cp .env.example .env
```

4. Run the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

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

