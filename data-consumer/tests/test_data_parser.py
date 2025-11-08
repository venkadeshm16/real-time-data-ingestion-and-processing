#!/usr/bin/env python3

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commonfunction.data_parser import DataParser

class TestDataParser:
    
    def test_parse_vitals(self):
        data = {
            'patient_id': 'P0001',
            'device_id': 'DEV001',
            'heart_rate': 120,
            'spo2': 95,
            'temperature': 37.5,
            'blood_pressure': '120/80',
            'status': 'CRITICAL',
            'timestamp': '2024-01-01T10:00:00'
        }
        result = DataParser.parse_vitals(data)
        assert result['patient_id'] == 'P0001'
        assert result['data_type'] == 'vitals'
        assert result['vitals']['heart_rate'] == 120
    
    def test_parse_hms(self):
        data = {
            'patient_id': 'P0001',
            'doctor_assigned': 'Dr. Smith',
            'ward': 'ICU-A',
            'bed_number': 'B001',
            'treatment': 'Surgery',
            'admission_date': '2024-01-01',
            'status': 'NORMAL',
            'priority': 'HIGH',
            'timestamp': '2024-01-01T10:00:00'
        }
        result = DataParser.parse_hms(data)
        assert result['data_type'] == 'hms'
        assert result['medical_info']['doctor_assigned'] == 'Dr. Smith'
    
    def test_parse_lab(self):
        data = {
            'patient_id': 'P0001',
            'test_name': 'Blood Sugar',
            'result': '150',
            'unit': 'mg/dL',
            'normal_range': '70-100',
            'status': 'CRITICAL',
            'priority': 'CRITICAL',
            'timestamp': '2024-01-01T10:00:00'
        }
        result = DataParser.parse_lab(data)
        assert result['data_type'] == 'lab'
        assert result['test_info']['test_name'] == 'Blood Sugar'
    
    def test_parse_pharmacy(self):
        data = {
            'patient_id': 'P0001',
            'medicine_name': 'Aspirin',
            'dosage': '100mg',
            'used_count': 5,
            'stock_count': 20,
            'ward': 'ICU-A',
            'status': 'NORMAL',
            'priority': 'NORMAL',
            'timestamp': '2024-01-01T10:00:00'
        }
        result = DataParser.parse_pharmacy(data)
        assert result['data_type'] == 'pharmacy'
        assert result['medication_info']['medicine_name'] == 'Aspirin'
    
    def test_parse_emergency(self):
        data = {
            'patient_id': 'P0001',
            'age': 45,
            'condition': 'Heart Attack',
            'criticality_score': 9,
            'emergency_doctor': 'Dr. Johnson',
            'target_ward': 'ICU-A',
            'status': 'CRITICAL',
            'priority': 'CRITICAL',
            'timestamp': '2024-01-01T10:00:00'
        }
        result = DataParser.parse_emergency(data)
        assert result['data_type'] == 'emergency'
        assert result['emergency_info']['condition'] == 'Heart Attack'