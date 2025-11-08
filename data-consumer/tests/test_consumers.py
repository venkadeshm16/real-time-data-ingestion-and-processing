#!/usr/bin/env python3

import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import kafka_consumer
import hms_consumer
import lab_consumer
import pharmacy_consumer
import emergency_consumer
import alert_consumer

class TestConsumerHandlers:
    
    @patch('kafka_consumer.DataParser')
    @patch('kafka_consumer.alert_producer')
    def test_handle_vitals_message_critical(self, mock_producer, mock_parser):
        mock_parser.parse_vitals.return_value = {
            'patient_id': 'P0001',
            'status': 'CRITICAL',
            'data_type': 'vitals'
        }
        
        data = {'patient_id': 'P0001', 'heart_rate': 180}
        kafka_consumer.handle_vitals_message(data)
        
        mock_parser.parse_vitals.assert_called_once_with(data)
        mock_producer.send_alert.assert_called_once()
    
    @patch('hms_consumer.DataParser')
    @patch('hms_consumer.alert_producer')
    def test_handle_hms_message_critical(self, mock_producer, mock_parser):
        mock_parser.parse_hms.return_value = {
            'patient_id': 'P0001',
            'priority': 'CRITICAL',
            'data_type': 'hms'
        }
        
        data = {'patient_id': 'P0001', 'priority': 'CRITICAL'}
        hms_consumer.handle_hms_message(data)
        
        mock_producer.send_alert.assert_called_once()
    
    @patch('lab_consumer.DataParser')
    @patch('lab_consumer.alert_producer')
    def test_handle_lab_message_normal(self, mock_producer, mock_parser):
        mock_parser.parse_lab.return_value = {
            'patient_id': 'P0001',
            'priority': 'NORMAL',
            'data_type': 'lab'
        }
        
        data = {'patient_id': 'P0001', 'priority': 'NORMAL'}
        lab_consumer.handle_lab_message(data)
        
        mock_producer.send_alert.assert_not_called()
    
    @patch('pharmacy_consumer.DataParser')
    @patch('pharmacy_consumer.alert_producer')
    def test_handle_pharmacy_message_critical(self, mock_producer, mock_parser):
        mock_parser.parse_pharmacy.return_value = {
            'patient_id': 'P0001',
            'priority': 'CRITICAL',
            'data_type': 'pharmacy'
        }
        
        data = {'patient_id': 'P0001', 'stock_count': 5}
        pharmacy_consumer.handle_pharmacy_message(data)
        
        mock_producer.send_alert.assert_called_once()
    
    @patch('emergency_consumer.DataParser')
    @patch('emergency_consumer.alert_producer')
    def test_handle_emergency_message_critical(self, mock_producer, mock_parser):
        mock_parser.parse_emergency.return_value = {
            'patient_id': 'P0001',
            'priority': 'CRITICAL',
            'data_type': 'emergency'
        }
        
        data = {'patient_id': 'P0001', 'criticality_score': 9}
        emergency_consumer.handle_emergency_message(data)
        
        mock_producer.send_alert.assert_called_once()
    
    @patch('alert_consumer.minio_storage')
    def test_handle_alert_message(self, mock_storage):
        data = {'alert_id': 'ALERT_001', 'patient_id': 'P0001'}
        alert_consumer.handle_alert_message(data)
        
        mock_storage.add_alert_to_batch.assert_called_once_with(data)