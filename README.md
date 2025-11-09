# JobPortal

An AI-powered job portal platform connecting job seekers with employers, featuring intelligent job matching, resume parsing, and personalized recommendations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Docker Deployment](#docker-deployment)
- [Development Setup](#development-setup)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## 🎯 Overview

The JobPortal project aims to develop a secure, scalable, and user-friendly platform connecting job seekers and employers. The core functionalities for job seekers include creating profiles, uploading resumes, searching and applying for jobs, and receiving notifications. Employers can post jobs, review applications, schedule interviews, and communicate with candidates.

The system leverages AI for personalized job recommendations, resume parsing, and candidate matching.

## ✨ Features

### For Job Seekers
- 👤 Profile creation and management
- 📄 Resume upload with AI-powered parsing
- 🔍 Advanced job search and filtering
- 🤖 AI-powered job recommendations
- 📝 One-click job applications
- 📊 Application tracking dashboard
- 💬 AI career assistant chatbot
- 📅 Interview scheduling

### For Employers
- 🏢 Company profile management
- 📢 Job posting creation and management
- 👥 Application review and candidate filtering
- 🎯 AI-powered candidate matching
- 📧 Automated email notifications
- 📅 Interview scheduling
- 📈 Analytics and reporting

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** MongoDB 7.0 with Beanie ODM
- **Authentication:** JWT with Bearer tokens
- **AI/ML:** OpenAI GPT-4o, LangChain, ChromaDB
- **Server:** Uvicorn (ASGI)

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State Management:** Zustand
- **HTTP Client:** Axios

### DevOps
- **Containerization:** Docker & Docker Compose
- **Database:** MongoDB Atlas (Cloud) or Local MongoDB

## 📦 Prerequisites

- **Docker Desktop** 4.0+ (for Docker deployment)
- **Node.js** 18+ (for local development)
- **Python** 3.11+ (for local development)
- **MongoDB Atlas Account** or Local MongoDB
- **OpenAI API Key** (for AI features)

## 🚀 Quick Start

### Using Startup Scripts (Recommended for Development)

```bash
# Clone the repository
git clone <repository-url>
cd jobpotal_greenfield

# Start both backend and frontend
./start.sh  # macOS/Linux
# or
start.bat   # Windows

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🐳 Docker Deployment

### Production Deployment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd jobpotal_greenfield
   ```

2. **Set up environment variables:**
   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env with your MongoDB URI and secrets

   # Frontend
   cp frontend/.env.local.example frontend/.env.local
   # Edit frontend/.env.local if needed
   ```

3. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - MongoDB Express (optional): http://localhost:8081

5. **View logs:**
   ```bash
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

6. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Development with Docker

For development with hot-reload:

```bash
# Start in development mode
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Rebuild after dependency changes
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### Using Local MongoDB

The `docker-compose.yml` includes an optional MongoDB service. To use it:

1. Update `backend/.env`:
   ```env
   MONGODB_URI=mongodb://admin:admin123@mongodb:27017/jobportal?authSource=admin
   ```

2. Start all services including MongoDB:
   ```bash
   docker-compose up -d
   ```

### Optional: Mongo Express (Database UI)

To access the MongoDB admin interface:

```bash
docker-compose --profile tools up -d mongo-express
```

Access at: http://localhost:8081 (username: admin, password: admin)

## 💻 Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.local.example .env.local
# Edit .env.local if needed

# Run development server
npm run dev
```

## 🔧 Environment Variables

### Backend (.env)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `MONGODB_URI` | MongoDB connection string | ✅ | - |
| `DATABASE_NAME` | Database name | ✅ | jobportal |
| `SECRET_KEY` | JWT secret key | ✅ | - |
| `OPENAI_API_KEY` | OpenAI API key for AI features | ✅ | - |
| `SMTP_HOST` | Email server host | ❌ | smtp.gmail.com |
| `SMTP_USER` | Email username | ❌ | - |
| `SMTP_PASSWORD` | Email password | ❌ | - |

### Frontend (.env.local)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | ✅ | http://localhost:8000 |
| `NEXT_PUBLIC_APP_NAME` | Application name | ❌ | JobPortal |

## 📚 API Documentation

Once the backend is running, you can access:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

### Key Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/jobs` - List jobs with filters
- `POST /api/v1/jobs` - Create job posting (employer)
- `POST /api/v1/applications` - Submit job application
- `GET /api/v1/recommendations` - Get AI job recommendations

## 📁 Project Structure

```
jobpotal_greenfield/
├── backend/                # FastAPI backend
│   ├── app/
│   │   ├── main.py        # Application entry point
│   │   ├── api/           # API routes
│   │   ├── core/          # Config, security, logging
│   │   ├── models/        # Database models (Beanie)
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── repositories/  # Data access layer
│   │   ├── ai/            # AI/ML features
│   │   └── db/            # Database setup
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/              # Next.js frontend
│   ├── app/              # Next.js pages (App Router)
│   ├── components/       # Reusable UI components
│   ├── features/         # Feature-specific components
│   ├── lib/              # Utilities and API client
│   ├── store/            # State management
│   ├── Dockerfile
│   ├── package.json
│   └── .env.local.example
│
├── docker-compose.yml     # Production Docker setup
├── docker-compose.dev.yml # Development Docker setup
├── start.sh              # Startup script (macOS/Linux)
├── start.bat             # Startup script (Windows)
└── README.md             # This file
```

## 🤝 Contributing

We follow a feature branch workflow:

1. Create a feature branch from `dev`:
   ```bash
   git checkout dev
   git pull
   git checkout -b feat/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

3. Push and create a Pull Request to `dev`:
   ```bash
   git push -u origin feat/your-feature-name
   ```

4. After review and approval, squash and merge to `dev`

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🔒 Security

- Never commit `.env` files
- Keep your `SECRET_KEY` secure
- Use environment variables for sensitive data
- Follow security best practices for production deployment

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Team

- **Team Member 1 & 2:** Backend Development
- **Team Member 3 & 4:** Frontend Development
- **Team Member 5:** Database Architecture
- **Team Member 6:** Docker & DevOps

## 📞 Support

For issues and questions:
- Check the [API Documentation](#api-documentation)
- Review the [STARTUP_GUIDE.md](STARTUP_GUIDE.md)
- Open an issue on GitHub

---

**Built with ❤️ by the JobPortal Team**
