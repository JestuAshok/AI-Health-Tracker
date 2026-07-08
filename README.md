# AI Health Tracker

AI Health Tracker is a FastAPI-based healthcare monitoring app for tracking patient symptoms, vitals, appointments, and recovery progress. It includes patient-facing pages for daily symptom logging and a doctor dashboard for reviewing risk levels, symptom trends, and patient reports.

The project uses a simple HTML/CSS/JavaScript frontend, a FastAPI backend, SQLite with SQLAlchemy, and optional Groq AI integration for extracting structured health metrics from voice or text symptom logs.

## Features

- Patient registration and profile management
- Daily symptom and vital logging
- Voice/text symptom parsing with optional Groq AI support
- Doctor dashboard with patient summaries and risk indicators
- Symptom history, recovery score, and health report views
- Appointment scheduling workflow
- Static frontend served directly from the FastAPI app
- Optional ngrok tunnel support for local public testing

## Tech Stack

- **Backend:** FastAPI, Uvicorn, SQLAlchemy, Pydantic
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **AI Integration:** Groq API
- **Tunneling:** pyngrok

## Project Structure

```text
ai-health-tracker/
|-- backend/
|   |-- app/
|   |   |-- api/routes/      # FastAPI route modules
|   |   |-- core/            # Configuration, database, ngrok setup
|   |   |-- models/          # SQLAlchemy models
|   |   |-- schemas/         # Pydantic schemas
|   |   `-- main.py          # Application entry point
|   |-- generate_dummy_data.py
|   |-- requirements.txt
|   `-- run.bat
|-- frontend/                # Static HTML, CSS, and JavaScript pages
|-- docker-compose.yml
`-- README.md
```

## Getting Started

### 1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install dependencies

```powershell
pip install -r backend/requirements.txt
```

### 3. Configure environment variables

Create a local `.env` file and add the values you need:

```env
GROQ_API_KEY=
NGROK_AUTH_TOKEN=
NGROK_URL=
DATABASE_URL=sqlite:///./sql_app.db
```

Keep real API keys out of Git.

### 4. Seed sample data

```powershell
cd backend
python generate_dummy_data.py
```

### 5. Run the application

```powershell
run.bat
```

Open the app at:

```text
http://127.0.0.1:8000
```

## Main Pages

- `index.html` - sign-in page
- `patient-dashboard.html` - patient overview
- `symptom-log.html` - daily symptom form
- `voice-logger.html` - voice/text symptom entry
- `doctor-dashboard.html` - clinician overview
- `health-reports.html` - patient reports
- `appointments.html` - appointment scheduling

## API Routes

The backend exposes grouped REST endpoints under `/api` for:

- Patients
- Symptoms
- Analytics
- Voice symptom parsing
- Appointments

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Security Notes

- Do not commit `.env`, database files, API keys, or generated cache files.
- Store `GROQ_API_KEY` and ngrok credentials only in local environment variables.
- Rotate any API key that has ever been committed or shared.

## Author

JestuAshok
