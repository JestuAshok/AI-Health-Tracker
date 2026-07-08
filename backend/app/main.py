from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import Base, engine
from app.models import domain # Import models to register metadata
from app.api.routes import patients, symptoms, analytics, voice, appointments

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Symptom Progression Tracker",
    description="Agentic AI-powered healthcare monitoring system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router, prefix="/api", tags=["Patients"])
app.include_router(symptoms.router, prefix="/api", tags=["Symptoms"])
app.include_router(analytics.router, prefix="/api", tags=["Analytics"])
app.include_router(voice.router, prefix="/api", tags=["Voice"])
app.include_router(appointments.router, prefix="/api", tags=["Appointments"])

import os
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend"))
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.on_event("startup")
def startup_event():
    from app.core.ngrok import start_ngrok_tunnel
    start_ngrok_tunnel(port=8000)
