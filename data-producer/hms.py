import random
from datetime import datetime, timedelta
from commonfunction.producer_base import BaseProducer
from commonfunction.shared_config import PATIENT_IDS, ICU_DOCTORS, ICU_WARDS, CRITICAL_TREATMENTS

statuses = ["Critical", "Stable", "Under Observation", "Recovering"]

def generate_hms_data():
    patient_id = random.choice(PATIENT_IDS)
    status = random.choice(statuses)
    ward = random.choice(ICU_WARDS)
    
    admission_date = (datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d")
    
    return {
        "patient_id": patient_id,
        "doctor_assigned": random.choice(ICU_DOCTORS),
        "ward": ward,
        "status": status,
        "treatment": random.choice(CRITICAL_TREATMENTS),
        "bed_number": f"{ward}-{random.randint(1, 15):02d}",
        "admission_date": admission_date,
        "priority": "CRITICAL" if status == "Critical" else "HIGH",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    producer = BaseProducer('hospital_management_producer', 'icu_hims_data')
    producer.run(generate_hms_data, sleep_interval=2)