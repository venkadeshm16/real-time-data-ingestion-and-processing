import random
from datetime import datetime
from commonfunction.producer_base import BaseProducer
from commonfunction.shared_config import PATIENT_IDS, ICU_WARDS

def generate_pharmacy_data():
    medicines = [
        "Dopamine", "Midazolam", "Fentanyl", "Noradrenaline", "Propofol",
        "Morphine", "Atropine", "Epinephrine", "Heparin", "Insulin"
    ]
    
    medicine = random.choice(medicines)
    patient_id = random.choice(PATIENT_IDS)
    ward = random.choice(ICU_WARDS)
    used = random.randint(1, 3)
    stock = random.randint(20, 200)
    
    is_critical = stock < 30
    
    return {
        "patient_id": patient_id,
        "ward": ward,
        "medicine_name": medicine,
        "dosage": f"{random.randint(5, 50)}mg",
        "used_count": used,
        "stock_count": stock,
        "priority": "CRITICAL" if is_critical else "NORMAL",
        "status": "Low Stock" if is_critical else "Available",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    producer = BaseProducer('icu_pharmacy_usage_producer', 'icu_pharmacy_data')
    producer.run(generate_pharmacy_data, sleep_interval=1)