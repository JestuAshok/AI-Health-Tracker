from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    weight = Column(Float)
    height = Column(Float)
    blood_group = Column(String)
    allergies = Column(Text, nullable=True)
    chronic_conditions = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    emergency_contact = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    symptoms = relationship("SymptomLog", back_populates="patient")

class SymptomLog(Base):
    __tablename__ = "symptom_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    pain_level = Column(Integer)
    fatigue_level = Column(Integer)
    cough_severity = Column(String)
    breathing_difficulty = Column(String)
    headache_severity = Column(String)
    sleep_quality = Column(Integer)
    mood_score = Column(Integer)
    stress_level = Column(Integer)
    appetite = Column(String)
    energy_level = Column(Integer)
    notes = Column(Text, nullable=True)
    submission_method = Column(String)
    
    patient = relationship("Patient", back_populates="symptoms")

class VoiceLog(Base):
    __tablename__ = "voice_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(DateTime, default=datetime.utcnow)
    audio_path = Column(String)
    transcript = Column(Text)
    extracted_symptoms = Column(JSON)

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(DateTime, default=datetime.utcnow)
    risk_level = Column(String) # LOW/MEDIUM/HIGH/CRITICAL
    explanation = Column(Text)
    generated_by_ai = Column(String)

class HealthReport(Base):
    __tablename__ = "health_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(DateTime, default=datetime.utcnow)
    report_type = Column(String) # DAILY/WEEKLY/MONTHLY
    summary_text = Column(Text)
    recovery_score = Column(Integer)

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer)
    date_time = Column(DateTime)
    purpose = Column(String)
    status = Column(String)
    google_calendar_event_id = Column(String, nullable=True)

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    type = Column(String) # REMINDER/ALERT
    message = Column(Text)
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)
