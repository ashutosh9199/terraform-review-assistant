@echo off
echo Starting Terraform Review Assistant...

:: Start the Python Backend in a new window
start "FastAPI Backend" cmd /c "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

:: Start the React Frontend in a new window
start "Vite Frontend" cmd /c "cd frontend && npm run dev -- --host"

echo Servers are starting up!
echo Frontend will be available at: http://localhost:5173
echo Backend API will be available at: http://localhost:8000/docs
pause
