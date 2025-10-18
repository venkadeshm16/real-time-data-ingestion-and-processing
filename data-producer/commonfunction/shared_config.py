# Shared configuration for ICU data producers

# 1000 patients shared between HMS and ICU vital systems
PATIENT_IDS = [f"P{i:04d}" for i in range(1, 1001)]

# ICU doctors with specializations
ICU_DOCTORS = [
    "Dr. Kumar", "Dr. Meena", "Dr. Ravi", "Dr. Priya", 
    "Dr. Singh", "Dr. Sharma", "Dr. Patel", "Dr. Gupta",
    "Dr. Reddy", "Dr. Nair", "Dr. Joshi", "Dr. Verma"
]

# Only ICU wards
ICU_WARDS = ["ICU-1", "ICU-2", "ICU-3", "ICU-4", "ICU-5"]

# Critical treatments for ICU patients
CRITICAL_TREATMENTS = [
    "Mechanical Ventilation", "ECMO", "Dialysis", "Cardiac Monitoring",
    "Vasopressor Support", "Intubation", "Defibrillation", "Blood Transfusion",
    "Emergency Surgery", "CPR", "Chest Tube", "Central Line"
]