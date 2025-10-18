import random
from datetime import datetime
from commonfunction.producer_base import BaseProducer
from commonfunction.shared_config import PATIENT_IDS

def generate_lab_data():
    tests = ["Blood Glucose", "Hemoglobin", "WBC Count", "Platelet Count", "Lactate", "Troponin", "BUN", "Creatinine"]
    test = random.choice(tests)
    
    if test == "Blood Glucose":
        result = random.randint(70, 180)
        unit = "mg/dL"
        normal_range = "70-110 mg/dL"
    elif test == "Hemoglobin":
        result = round(random.uniform(11.0, 16.0), 1)
        unit = "g/dL"
        normal_range = "12-16 g/dL"
    elif test == "WBC Count":
        result = random.randint(4000, 11000)
        unit = "cells/uL"
        normal_range = "4000-11000 cells/uL"
    elif test == "Platelet Count":
        result = random.randint(150000, 450000)
        unit = "/µL"
        normal_range = "150000-450000 /µL"
    elif test == "Lactate":
        result = round(random.uniform(0.5, 4.0), 1)
        unit = "mmol/L"
        normal_range = "0.5-2.2 mmol/L"
    elif test == "Troponin":
        result = round(random.uniform(0.01, 2.0), 2)
        unit = "ng/mL"
        normal_range = "<0.04 ng/mL"
    elif test == "BUN":
        result = random.randint(7, 50)
        unit = "mg/dL"
        normal_range = "7-20 mg/dL"
    elif test == "Creatinine":
        result = round(random.uniform(0.6, 3.0), 1)
        unit = "mg/dL"
        normal_range = "0.6-1.2 mg/dL"
    
    is_critical = random.random() < 0.2
    
    return {
        "patient_id": random.choice(PATIENT_IDS),
        "test_name": test,
        "result": result,
        "unit": unit,
        "normal_range": normal_range,
        "status": random.choice(["Completed", "Verified", "Critical"]) if is_critical else "Completed",
        "priority": "CRITICAL" if is_critical else "NORMAL",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    producer = BaseProducer('lab_information_producer', 'icu_lab_results')
    producer.run(generate_lab_data, sleep_interval=2)