from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.domain import Patient
from app.schemas.domain import PatientCreate, Patient as PatientSchema

router = APIRouter()

@router.post("/register-patient", response_model=PatientSchema)
def register_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/patient-history/{patient_id}", response_model=PatientSchema)
def get_patient_history(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.get("/patients", response_model=list[PatientSchema])
def get_all_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()
