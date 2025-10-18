import time
import random
from datetime import datetime
from commonfunction.producer_base import BaseProducer
from commonfunction.shared_config import PATIENT_IDS

last_critical_time = time.time()

def generate_icu_vitals():
    global last_critical_time
    
    current_time = time.time()
    is_critical = (current_time - last_critical_time) >= 60
    
    if is_critical:
        last_critical_time = current_time
        print("CRITICAL ALERT GENERATED")
    
    patient_id = random.choice(PATIENT_IDS)
    
    if is_critical:
        return {
            "patient_id": patient_id,
            "device_id": f"ICU_{patient_id[1:]}",
            "heart_rate": random.choice([35, 180]),
            "spo2": random.randint(85, 90),
            "temperature": round(random.choice([35.0, 40.5]), 1),
            "blood_pressure": random.choice(["80/50", "200/120"]),
            "status": "CRITICAL",
            "timestamp": datetime.now().isoformat()
        }
    
    return {
        "patient_id": patient_id,
        "device_id": f"ICU_{patient_id[1:]}",
        "heart_rate": random.randint(60, 100),
        "spo2": random.randint(95, 100),
        "temperature": round(36.5 + random.uniform(-0.3, 0.8), 1),
        "blood_pressure": f"{random.randint(110, 140)}/{random.randint(70, 90)}",
        "status": "NORMAL",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    producer = BaseProducer('icu_data_producer', 'icu_device_data')
    producer.run(generate_icu_vitals, sleep_interval=0.1)