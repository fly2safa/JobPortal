# Quick Reference Card 🚀

## Windows (PowerShell)

### Default Ports
```powershell
# Backend (port 8000)
.\ourscript\start-backend.ps1

# Frontend (port 3000)
.\ourscript\start-frontend.ps1
```

### Custom Ports
```powershell
# Backend (port 8010)
.\ourscript\start-backend.ps1 -Port 8010

# Frontend (port 3001)
.\ourscript\start-frontend.ps1 -Port 3001
```

---

## macOS/Linux (Bash)

### First Time Setup
```bash
chmod +x ./ourscript/*.sh
```

### Default Ports
```bash
# Backend (port 8000)
./ourscript/start-backend.sh

# Frontend (port 3000)
./ourscript/start-frontend.sh
```

### Custom Ports
```bash
# Backend (port 8010)
./ourscript/start-backend.sh 8010

# Backend (port 8010, host 0.0.0.0)
./ourscript/start-backend.sh 8010 0.0.0.0

# Frontend (port 3001)
./ourscript/start-frontend.sh 3001
```

---

## URLs

| Service | Default URL | API Docs |
|---------|-------------|----------|
| Backend | http://127.0.0.1:8000 | http://127.0.0.1:8000/docs |
| Frontend | http://localhost:3000 | N/A |

---

## Stop Servers

Press `Ctrl+C` in the terminal

---

## Kill Port Process

### Windows
```powershell
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### macOS/Linux
```bash
# Kill process on port 8000
kill -9 $(lsof -ti:8000)
```

---

**💡 Tip:** Open two terminals - one for backend, one for frontend!

