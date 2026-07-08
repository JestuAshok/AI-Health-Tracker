from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class SymptomLogBase(BaseModel):
    temperature: float
    pain_level: int
    fatigue_level: int
    cough_severity: str
    breathing_difficulty: str
    headache_severity: str
    sleep_quality: int
    mood_score: int
    stress_level: int
    appetite: str
    energy_level: int
    notes: Optional[str] = None
    submission_method: str

class SymptomLogCreate(SymptomLogBase):
    pass

class SymptomLog(SymptomLogBase):
    id: int
    patient_id: int
    date: datetime
    
    class Config:
        from_attributes = True

class PatientBase(BaseModel):
    name: str
    age: int
    gender: str
    weight: float
    height: float
    blood_group: str
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None
    medications: Optional[str] = None
    emergency_contact: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    created_at: datetime
    symptoms: List[SymptomLog] = []
    
    class Config:
        from_attributes = True

class RiskAssessmentBase(BaseModel):
    risk_level: str
    explanation: str
    generated_by_ai: str

class RiskAssessment(RiskAssessmentBase):
    id: int
    patient_id: int
    date: datetime
    
    class Config:
        from_attributes = True

class HealthReportBase(BaseModel):
    report_type: str
    summary_text: str
    recovery_score: int

class HealthReport(HealthReportBase):
    id: int
    patient_id: int
    date: datetime
    
    class Config:
        from_attributes = True

class SymptomLogResponse(SymptomLog):
    progress_message: str

class VoiceSymptomRequest(BaseModel):
    text: str

class AppointmentBase(BaseModel):
    doctor_id: int
    date_time: datetime
    purpose: str
    status: str
    google_calendar_event_id: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    patient_id: int

    class Config:
        from_attributes = True
