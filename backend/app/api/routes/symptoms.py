from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.domain import SymptomLog
from app.schemas.domain import SymptomLogCreate, SymptomLog as SymptomLogSchema, SymptomLogResponse

router = APIRouter()

@router.post("/submit-symptoms/{patient_id}")
def submit_symptoms(patient_id: int, symptom: SymptomLogCreate, db: Session = Depends(get_db)):
    # Find the most recent symptom log for comparison
    previous_log = db.query(SymptomLog).filter(SymptomLog.patient_id == patient_id).order_by(SymptomLog.date.desc()).first()
    
    if not previous_log:
        return {"progress_message": "This is your first log, so we can't compare it to yesterday."}

    messages = []
    
    # Temperature comparison
    if symptom.temperature < previous_log.temperature:
        messages.append(f"Temperature dropped from {previous_log.temperature}°F to {symptom.temperature}°F (Improving).")
    elif symptom.temperature > previous_log.temperature:
        messages.append(f"Temperature increased from {previous_log.temperature}°F to {symptom.temperature}°F (Worsening).")
    else:
        messages.append(f"Temperature is stable at {symptom.temperature}°F.")
        
    # Fatigue comparison
    if symptom.fatigue_level < previous_log.fatigue_level:
        messages.append(f"Fatigue is improving (down to {symptom.fatigue_level} from {previous_log.fatigue_level}).")
    elif symptom.fatigue_level > previous_log.fatigue_level:
        messages.append(f"Fatigue is worsening (up to {symptom.fatigue_level} from {previous_log.fatigue_level}).")
    else:
        messages.append(f"Fatigue level is stable at {symptom.fatigue_level}.")
        
    # Pain comparison
    if symptom.pain_level < previous_log.pain_level:
        messages.append(f"Pain is improving (down to {symptom.pain_level} from {previous_log.pain_level}).")
    elif symptom.pain_level > previous_log.pain_level:
        messages.append(f"Pain is worsening (up to {symptom.pain_level} from {previous_log.pain_level}).")
    else:
        messages.append(f"Pain level is stable at {symptom.pain_level}.")

    # Count improvements vs worsenings
    improvements = sum(1 for m in messages if "Improving" in m or "improving" in m)
    worsenings = sum(1 for m in messages if "Worsening" in m or "worsening" in m)
    
    if improvements > worsenings:
        overall = "Overall, your health is better compared to yesterday! Keep it up.\n\n"
    elif worsenings > improvements:
        overall = "Overall, your health seems a bit worse compared to yesterday. Please take care.\n\n"
    else:
        overall = "Overall, your health is about the same as yesterday.\n\n"

    progress_message = overall + "Details:\n- " + "\n- ".join(messages)

    # Return only the progress message without saving to DB
    return {"progress_message": progress_message}
