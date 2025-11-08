#!/usr/bin/env python3

import pytest
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from icu_vital import generate_icu_vitals
from hms import generate_hms_data
from lab import generate_lab_data
from pharmacy import generate_pharmacy_data
from emergency import generate_emergency_data

class TestDataGenerators:
    
    def test_icu_vitals_structure(self):
        data = generate_icu_vitals()
        required_fields = ["patient_id", "device_id", "heart_rate", "spo2", "temperature", "blood_pressure", "status", "timestamp"]
        assert all(field in data for field in required_fields)
        assert data["status"] in ["NORMAL", "CRITICAL"]
        assert isinstance(data["heart_rate"], int)
        assert isinstance(data["spo2"], int)
        assert isinstance(data["temperature"], float)
    
    def test_hms_data_structure(self):
        data = generate_hms_data()
        required_fields = ["patient_id", "doctor_assigned", "ward", "status", "treatment", "bed_number", "admission_date", "priority", "timestamp"]
        assert all(field in data for field in required_fields)
        assert data["priority"] in ["CRITICAL", "HIGH"]
        assert data["ward"].startswith("ICU-")
    
    def test_lab_data_structure(self):
        data = generate_lab_data()
        required_fields = ["patient_id", "test_name", "result", "unit", "normal_range", "status", "priority", "timestamp"]
        assert all(field in data for field in required_fields)
        assert data["priority"] in ["CRITICAL", "NORMAL"]
    
    def test_pharmacy_data_structure(self):
        data = generate_pharmacy_data()
        required_fields = ["patient_id", "ward", "medicine_name", "dosage", "used_count", "stock_count", "priority", "status", "timestamp"]
        assert all(field in data for field in required_fields)
        assert isinstance(data["stock_count"], int)
        assert data["priority"] in ["CRITICAL", "NORMAL"]
    
    def test_emergency_data_structure(self):
        data = generate_emergency_data()
        required_fields = ["patient_id", "age", "condition", "criticality_score", "emergency_doctor", "target_ward", "priority", "status", "timestamp"]
        assert all(field in data for field in required_fields)
        assert data["priority"] in ["CRITICAL", "HIGH"]
        assert 6 <= data["criticality_score"] <= 10
    
    def test_timestamp_format(self):
        generators = [generate_icu_vitals, generate_hms_data, generate_lab_data, generate_pharmacy_data, generate_emergency_data]
        for gen in generators:
            data = gen()
            datetime.fromisoformat(data["timestamp"])  # Should not raise exception
    
    def test_icu_vitals_critical_values(self):
        # Test critical value ranges
        for _ in range(10):
            data = generate_icu_vitals()
            if data["status"] == "CRITICAL":
                assert data["heart_rate"] in [35, 180] or data["spo2"] <= 90
    
    def test_pharmacy_critical_stock(self):
        # Test critical stock detection
        for _ in range(20):
            data = generate_pharmacy_data()
            if data["priority"] == "CRITICAL":
                assert data["stock_count"] < 30
    
    def test_emergency_criticality_priority(self):
        # Test criticality score to priority mapping
        for _ in range(10):
            data = generate_emergency_data()
            if data["criticality_score"] >= 8:
                assert data["priority"] == "CRITICAL"
            else:
                assert data["priority"] == "HIGH"