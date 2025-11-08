#!/usr/bin/env python3

import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commonfunction.alert_producer import AlertProducer

class TestAlertProducer:
    
    @patch('commonfunction.alert_producer.Producer')
    @patch('commonfunction.alert_producer.record_alert_generated')
    def test_send_alert(self, mock_record, mock_producer):
        mock_producer_instance = Mock()
        mock_producer.return_value = mock_producer_instance
        
        producer = AlertProducer()
        parsed_data = {
            'patient_id': 'P0001',
            'data_type': 'vitals',
            'status': 'CRITICAL'
        }
        
        producer.send_alert(parsed_data)
        
        mock_producer_instance.produce.assert_called_once()
        mock_record.assert_called_once_with('vitals')
    
    @patch('commonfunction.alert_producer.Producer')
    def test_alert_structure(self, mock_producer):
        mock_producer_instance = Mock()
        mock_producer.return_value = mock_producer_instance
        
        producer = AlertProducer()
        parsed_data = {
            'patient_id': 'P0001',
            'data_type': 'vitals',
            'status': 'CRITICAL'
        }
        
        with patch('json.dumps') as mock_json:
            producer.send_alert(parsed_data)
            
            # Check alert structure
            call_args = mock_json.call_args[0][0]
            assert 'alert_id' in call_args
            assert call_args['patient_id'] == 'P0001'
            assert call_args['data_type'] == 'vitals'
    
    @patch('commonfunction.alert_producer.Producer')
    def test_close(self, mock_producer):
        mock_producer_instance = Mock()
        mock_producer.return_value = mock_producer_instance
        
        producer = AlertProducer()
        producer.close()
        
        mock_producer_instance.flush.assert_called_once()