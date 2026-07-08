from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.domain import Appointment
from app.schemas.domain import AppointmentCreate, Appointment as AppointmentSchema

router = APIRouter()

@router.get("/appointments/{patient_id}", response_model=List[AppointmentSchema])
def get_appointments(patient_id: int, db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.patient_id == patient_id).order_by(Appointment.date_time.asc()).all()
    return appointments

@router.post("/appointments/{patient_id}", response_model=AppointmentSchema)
def schedule_appointment(patient_id: int, appointment: AppointmentCreate, db: Session = Depends(get_db)):
    new_appointment = Appointment(
        patient_id=patient_id,
        **appointment.dict()
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment
