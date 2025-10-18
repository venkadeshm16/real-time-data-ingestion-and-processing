#!/usr/bin/env python3

import random
from datetime import datetime
from commonfunction.producer_base import BaseProducer
from commonfunction.shared_config import ICU_WARDS

# Emergency patient IDs and doctors
emergency_patient_ids = [f"ER{i:04d}" for i in range(1, 501)]
emergency_doctors = [
    "Dr. Anderson", "Dr. Brown", "Dr. Clark", "Dr. Davis", 
    "Dr. Evans", "Dr. Foster", "Dr. Garcia", "Dr. Harris"
]

def generate_emergency_data():
    conditions = [
        "Cardiac Arrest", "Head Injury", "Severe Trauma", "Respiratory Distress",
        "Stroke", "Sepsis", "Multi-organ Failure", "Acute MI", "Pneumonia"
    ]
    
    patient_id = random.choice(emergency_patient_ids)
    condition = random.choice(conditions)
    criticality_score = random.randint(6, 10)
    
    return {
        "patient_id": patient_id,
        "age": random.randint(25, 85),
        "condition": condition,
        "criticality_score": criticality_score,
        "emergency_doctor": random.choice(emergency_doctors),
        "target_ward": random.choice(ICU_WARDS),
        "priority": "CRITICAL" if criticality_score >= 8 else "HIGH",
        "status": "Transfer to ICU",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    producer = BaseProducer('emergency_department_producer', 'icu_emergency_data')
    producer.run(generate_emergency_data, sleep_interval=1)