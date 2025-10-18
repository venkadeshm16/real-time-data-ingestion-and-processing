#!/usr/bin/env python3

import json
from datetime import datetime

class DataParser:
    @staticmethod
    def parse_vitals(data):
        return {
            'patient_id': data['patient_id'],
            'device_id': data['device_id'],
            'vitals': {
                'heart_rate': data['heart_rate'],
                'spo2': data['spo2'],
                'temperature': data['temperature'],
                'blood_pressure': data['blood_pressure']
            },
            'status': data['status'],
            'timestamp': data['timestamp'],
            'data_type': 'vitals'
        }
    
    @staticmethod
    def parse_hms(data):
        return {
            'patient_id': data['patient_id'],
            'medical_info': {
                'doctor_assigned': data['doctor_assigned'],
                'ward': data['ward'],
                'bed_number': data['bed_number'],
                'treatment': data['treatment'],
                'admission_date': data['admission_date']
            },
            'status': data['status'],
            'priority': data['priority'],
            'timestamp': data['timestamp'],
            'data_type': 'hms'
        }
    
    @staticmethod
    def parse_lab(data):
        return {
            'patient_id': data['patient_id'],
            'test_info': {
                'test_name': data['test_name'],
                'result': data['result'],
                'unit': data['unit'],
                'normal_range': data['normal_range']
            },
            'status': data['status'],
            'priority': data['priority'],
            'timestamp': data['timestamp'],
            'data_type': 'lab'
        }
    
    @staticmethod
    def parse_pharmacy(data):
        return {
            'patient_id': data['patient_id'],
            'medication_info': {
                'medicine_name': data['medicine_name'],
                'dosage': data['dosage'],
                'used_count': data['used_count'],
                'stock_count': data['stock_count'],
                'ward': data['ward']
            },
            'status': data['status'],
            'priority': data['priority'],
            'timestamp': data['timestamp'],
            'data_type': 'pharmacy'
        }
    
    @staticmethod
    def parse_emergency(data):
        return {
            'patient_id': data['patient_id'],
            'emergency_info': {
                'age': data['age'],
                'condition': data['condition'],
                'criticality_score': data['criticality_score'],
                'emergency_doctor': data['emergency_doctor'],
                'target_ward': data['target_ward']
            },
            'status': data['status'],
            'priority': data['priority'],
            'timestamp': data['timestamp'],
            'data_type': 'emergency'
        }