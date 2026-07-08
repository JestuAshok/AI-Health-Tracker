from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.domain import SymptomLog

router = APIRouter()

@router.get("/health-analytics/{patient_id}")
def get_health_analytics(patient_id: int, db: Session = Depends(get_db)):
    symptoms = db.query(SymptomLog).filter(SymptomLog.patient_id == patient_id).order_by(SymptomLog.date.asc()).all()
    # Mocking for now
    return {"patient_id": patient_id, "total_logs": len(symptoms)}

@router.get("/recovery-score/{patient_id}")
def get_recovery_score(patient_id: int, db: Session = Depends(get_db)):
    return {"patient_id": patient_id, "recovery_score": 85}

@router.get("/risk-assessment/{patient_id}")
def get_risk_assessment(patient_id: int, db: Session = Depends(get_db)):
    return {"patient_id": patient_id, "risk_level": "LOW", "explanation": "Symptoms are stable."}

@router.get("/health-summary/{patient_id}")
def get_health_summary(patient_id: int, db: Session = Depends(get_db)):
    return {"patient_id": patient_id, "summary": "Patient is doing well based on recent logs."}

@router.post("/send-alert/{patient_id}")
def send_alert(patient_id: int, db: Session = Depends(get_db)):
    return {"message": f"Alert sent for patient {patient_id}"}
