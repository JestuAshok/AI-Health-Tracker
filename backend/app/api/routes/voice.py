import os
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.domain import VoiceSymptomRequest
from app.models.domain import SymptomLog
from groq import Groq

router = APIRouter()

@router.post("/voice-symptoms")
def submit_voice_symptoms(request: VoiceSymptomRequest, db: Session = Depends(get_db)):
    text = request.text
    
    from app.core.config import settings
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise HTTPException(status_code=500, detail="Groq API Key not configured. Please add it to your environment variables.")
        
    client = Groq(api_key=api_key)
    
    prompt = f"""
    Analyze the following patient voice transcript and extract health symptoms.
    Respond ONLY with a valid JSON object in the following format. 
    Make sure to provide a unique, empathetic, and encouraging 'description' of what was detected, as if speaking to the patient.
    
    {{
        "temperature": (float, estimate based on transcript if mentioned like fever=101.5, default 98.6),
        "fatigue_level": (int 1-10, default 1),
        "pain_level": (int 1-10, default 1),
        "description": "A customized encouraging description based on their specific transcript."
    }}
    
    Transcript: "{text}"
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful medical AI assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        
        result_str = response.choices[0].message.content
        data = json.loads(result_str)
        
        temperature = float(data.get("temperature", 98.6))
        fatigue = int(data.get("fatigue_level", 1))
        pain = int(data.get("pain_level", 1))
        description = data.get("description", "Your voice log has been saved and analyzed.")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing voice: {str(e)}")

    # Save generated health to SymptomLog
    new_log = SymptomLog(
        patient_id=1,  # Hardcoded for now
        temperature=temperature,
        pain_level=pain,
        fatigue_level=fatigue,
        cough_severity="None",
        breathing_difficulty="None",
        headache_severity="Severe" if pain > 5 else "None",
        sleep_quality=5,
        mood_score=5,
        stress_level=5,
        appetite="Normal",
        energy_level=max(1, 10 - fatigue),
        notes=f"Voice Log: {text}",
        submission_method="VOICE"
    )
    db.add(new_log)
    db.commit()
    
    return {
        "message": "Voice symptoms processed",
        "description": description,
        "extracted": {
            "temperature": temperature,
            "fatigue_level": fatigue,
            "pain_level": pain
        }
    }
