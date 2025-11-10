# Server Startup Scripts

This folder contains convenient scripts to start the backend and frontend servers for the JobPortal application.

## 📁 Available Scripts

### PowerShell Scripts (Windows)
- `start-backend.ps1` - Start FastAPI backend server
- `start-frontend.ps1` - Start Next.js frontend server

### Bash Scripts (macOS/Linux)
- `start-backend.sh` - Start FastAPI backend server
- `start-frontend.sh` - Start Next.js frontend server

---

## 🚀 Quick Start

### Windows (PowerShell)

#### Start Backend (Default Port 8000)
```powershell
.\ourscript\start-backend.ps1
```

#### Start Backend (Custom Port 8010)
```powershell
.\ourscript\start-backend.ps1 -Port 8010
```

#### Start Backend (Custom Host and Port)
```powershell
.\ourscript\start-backend.ps1 -Port 8010 -HostAddress "0.0.0.0"
```

#### Start Frontend (Default Port 3000)
```powershell
.\ourscript\start-frontend.ps1
```

#### Start Frontend (Custom Port 3001)
```powershell
.\ourscript\start-frontend.ps1 -Port 3001
```

### macOS/Linux (Bash)

#### Make Scripts Executable (First Time Only)
```bash
chmod +x ./ourscript/start-backend.sh
chmod +x ./ourscript/start-frontend.sh
```

#### Start Backend (Default Port 8000)
```bash
./ourscript/start-backend.sh
```

#### Start Backend (Custom Port 8010)
```bash
./ourscript/start-backend.sh 8010
```

#### Start Backend (Custom Host and Port)
```bash
./ourscript/start-backend.sh 8010 0.0.0.0
```

#### Start Frontend (Default Port 3000)
```bash
./ourscript/start-frontend.sh
```

#### Start Frontend (Custom Port 3001)
```bash
./ourscript/start-frontend.sh 3001
```

---

## 📋 Prerequisites

### Backend Server
- Python 3.8 or higher installed
- Virtual environment created: `python -m venv backend/venv`
- Dependencies installed: `pip install -r backend/requirements.txt`
- `.env` file configured in `backend/` directory with:
  - `MONGODB_URL`
  - `JWT_SECRET_KEY`
  - `SMTP_*` settings (optional)

### Frontend Server
- Node.js 18 or higher installed
- npm or yarn package manager
- Dependencies installed: `npm install` in `frontend/` directory
- `.env.local` file configured in `frontend/` directory with:
  - `NEXT_PUBLIC_API_URL=http://localhost:8000`

---

## 🔧 Default Ports

| Service  | Default Port | API/URL                          |
|----------|--------------|----------------------------------|
| Backend  | 8000         | http://127.0.0.1:8000           |
| Backend  | 8000         | http://127.0.0.1:8000/docs (API Docs) |
| Frontend | 3000         | http://localhost:3000           |

---

## 🎯 Custom Port Usage

### When to Use Custom Ports

Use custom ports when:
- Default ports are already in use by another application
- Running multiple instances for testing
- Deploying to environments with specific port requirements
- Port conflicts occur during development

### Important Notes for Custom Ports

1. **Backend Custom Port**: If you change the backend port from 8000, update the frontend `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8010
   ```

2. **Frontend Custom Port**: Next.js will automatically use the custom port. No additional configuration needed.

3. **Firewall**: Ensure your firewall allows traffic on custom ports.

---

## 🛑 Stopping Servers

To stop any running server:
- Press `Ctrl+C` in the terminal where the server is running

---

## 🐛 Troubleshooting

### "Port already in use" Error

**Windows (PowerShell):**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**macOS/Linux (Bash):**
```bash
# Find process using port 8000
lsof -ti:8000

# Kill process
kill -9 $(lsof -ti:8000)
```

### "Virtual environment not found" Error

Create the virtual environment:
```bash
cd backend
python -m venv venv  # Windows/Linux
python3 -m venv venv # macOS
```

### "node_modules not found" Error

Install frontend dependencies:
```bash
cd frontend
npm install
```

### PowerShell Execution Policy Error

If you get "cannot be loaded because running scripts is disabled":
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Bash Permission Denied Error

Make the script executable:
```bash
chmod +x ./ourscript/start-backend.sh
chmod +x ./ourscript/start-frontend.sh
```

---

## 📝 Development Workflow

### Typical Development Setup

1. **Terminal 1 - Backend:**
   ```bash
   ./ourscript/start-backend.sh
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   ./ourscript/start-frontend.sh
   ```

3. **Access Application:**
   - Frontend: http://localhost:3000
   - Backend API Docs: http://127.0.0.1:8000/docs
   - Backend Admin: http://127.0.0.1:8000/admin

### Running on Custom Ports

1. **Terminal 1 - Backend on 8010:**
   ```bash
   ./ourscript/start-backend.sh 8010
   ```

2. **Update Frontend .env.local:**
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8010
   ```

3. **Terminal 2 - Frontend on 3001:**
   ```bash
   ./ourscript/start-frontend.sh 3001
   ```

---

## 💡 Tips

- **Auto-reload**: Both servers support hot-reload during development
- **Logs**: Server logs appear in the terminal where the script was run
- **Multiple Instances**: Use custom ports to run multiple instances simultaneously
- **Background Running**: Add `&` at the end (Bash) or use `Start-Process` (PowerShell) to run in background

---

## 📞 Support

If you encounter issues:
1. Check the prerequisites are met
2. Verify `.env` and `.env.local` files are configured
3. Review the troubleshooting section
4. Check the main project README for additional setup instructions

---

**Last Updated:** November 2025
**Project:** JobPortal (TalentNest)

