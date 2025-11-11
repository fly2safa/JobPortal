# JobPortal (TalentNest)

A secure, scalable, and user-friendly platform connecting job seekers and employers.

## 🚀 Features

### For Job Seekers
- 📝 Create and manage profiles
- 📄 Upload and parse resumes with AI
- 🔍 Search and filter jobs by location, type, and experience level
- 💼 Apply to jobs with AI-generated cover letters
- 📊 Track application status
- 🤖 Get personalized job recommendations
- 💬 AI career assistant for guidance

### For Employers
- 📢 Post and manage job listings
- 👥 Review and manage applications
- ✅ Shortlist and reject candidates
- 📧 Send email notifications
- 🎯 AI-powered candidate matching
- 📅 Schedule interviews

### AI-Powered Features
- 🧠 Resume parsing and information extraction
- 📝 AI cover letter generation
- 🎯 Job recommendations based on skills and experience
- 🤝 Candidate-job matching
- 💬 RAG-based AI assistant with job portal knowledge

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: MongoDB Atlas with Beanie ODM
- **Authentication**: JWT with bcrypt
- **AI**: OpenAI GPT-4o
- **Email**: SMTP with aiosmtplib

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios

## 📦 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Node.js 20 or higher
- MongoDB Atlas account (or local MongoDB)
- Docker & Docker Compose (for containerized deployment)

### Option 1: Docker Setup (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd JobPortal
   ```

2. **Set up environment variables**:
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env with your actual values
   
   # Frontend
   cp frontend/.env.example frontend/.env.local
   # Edit frontend/.env.local with your actual values
   ```

3. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

5. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Run the backend**:
   ```bash
   # Python 3.13+ on Windows (no auto-reload)
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   
   # Python < 3.13 or Linux/Mac (with auto-reload)
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your actual values
   ```

4. **Run the frontend**:
   ```bash
   npm run dev
   ```

5. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🔧 Configuration

### Backend Environment Variables

Required variables in `backend/.env`:
- `MONGODB_URI`: MongoDB connection string
- `DATABASE_NAME`: Database name (default: TalentNest)
- `SECRET_KEY`: JWT secret key (generate a strong random string)
- `CORS_ORIGINS`: Allowed origins (e.g., http://localhost:3000)

Optional variables:
- `OPENAI_API_KEY`: For AI features (cover letter, assistant)
- `SMTP_*`: For email notifications

See `backend/.env.example` for all available options.

### Frontend Environment Variables

Required variables in `frontend/.env.local`:
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🐳 Docker Commands

### Build images
```bash
docker-compose build
```

### Run in detached mode
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f
```

### Stop containers
```bash
docker-compose down
```

### Remove volumes
```bash
docker-compose down -v
```

### Rebuild and restart
```bash
docker-compose up --build --force-recreate
```

## 📁 Project Structure

```
JobPortal/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── ai/             # AI features (RAG, prompts)
│   │   └── main.py         # Application entry point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # Reusable components
│   ├── features/          # Feature-specific components
│   ├── lib/               # Utilities and API client
│   ├── store/             # State management
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml     # Docker orchestration

```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/feature-name`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feat/feature-name`)
5. Open a Pull Request

## 📝 License

This project is part of an academic assignment.

## 👥 Team

Developed as part of a collaborative software engineering project.

## 🔗 Links

- [Implementation Plan](./JobPortal%20Implementation%20Plan.md)
- [Testing Documentation](./TESTING_REPORT.md)
- [Backend Testing Guide](./backend/TESTING_BACKEND.md)

---

**Note**: This is a development setup. For production deployment, additional security measures, environment configurations, and optimizations are required.
