@echo off
echo Starting AI Symptom Progression Tracker API...
cd %~dp0
call ..\venv\Scripts\activate
uvicorn app.main:app --reload
