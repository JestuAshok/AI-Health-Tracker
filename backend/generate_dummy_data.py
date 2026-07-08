import sys
import os
import random
from datetime import datetime, timedelta
from faker import Faker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.models.domain import Patient, SymptomLog, RiskAssessment, HealthReport

# Create tables
Base.metadata.create_all(bind=engine)

fake = Faker()

def generate_data():
    db = SessionLocal()
    
    print("Generating 10 patients for quick testing...")
    patients = []
    for i in range(10): # Doing 10 instead of 100 to be faster
        p = Patient(
            name=fake.name(),
            age=random.randint(20, 80),
            gender=random.choice(["Male", "Female"]),
            weight=random.uniform(50.0, 100.0),
            height=random.uniform(150.0, 190.0),
            blood_group=random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]),
            created_at=datetime.utcnow() - timedelta(days=60)
        )
        db.add(p)
        db.commit()
        db.refresh(p)
        patients.append(p)
        
    print("Generating symptom logs...")
    for p in patients:
        for day in range(60):
            date = datetime.utcnow() - timedelta(days=60-day)
            log = SymptomLog(
                patient_id=p.id,
                date=date,
                temperature=round(random.uniform(97.0, 103.0), 1),
                pain_level=random.randint(1, 10),
                fatigue_level=random.randint(1, 10),
                cough_severity=random.choice(["None", "Mild", "Moderate", "Severe"]),
                breathing_difficulty=random.choice(["None", "Mild", "Moderate", "Severe"]),
                headache_severity=random.choice(["None", "Mild", "Moderate", "Severe"]),
                sleep_quality=random.randint(1, 10),
                mood_score=random.randint(1, 10),
                stress_level=random.randint(1, 10),
                appetite=random.choice(["Poor", "Normal", "Good"]),
                energy_level=random.randint(1, 10),
                submission_method="Dashboard Form"
            )
            db.add(log)
        db.commit()
        
    print("Data generation complete!")
    db.close()

if __name__ == "__main__":
    generate_data()
