#!/usr/bin/env python3

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commonfunction.producer_base import BaseProducer

class TestBaseProducer:
    
    @patch('commonfunction.producer_base.Producer')
    @patch('commonfunction.producer_base.start_metrics_server')
    def test_init(self, mock_metrics, mock_producer):
        producer = BaseProducer('test_client', 'test_topic')
        assert producer.client_id == 'test_client'
        assert producer.topic_name == 'test_topic'
        assert producer.message_count == 0
        mock_producer.assert_called_once()
    
    @patch('commonfunction.producer_base.Producer')
    @patch('commonfunction.producer_base.start_metrics_server')
    def test_send_message(self, mock_metrics, mock_producer):
        mock_producer_instance = Mock()
        mock_producer.return_value = mock_producer_instance
        
        producer = BaseProducer('test_client', 'test_topic')
        test_data = {"patient_id": "P0001", "value": 100}
        
        producer.send_message(test_data)
        
        mock_producer_instance.produce.assert_called_once()
        assert producer.message_count == 1
    
    @patch('commonfunction.producer_base.Producer')
    @patch('commonfunction.producer_base.start_metrics_server')
    def test_delivery_report_success(self, mock_metrics, mock_producer):
        producer = BaseProducer('test_client', 'test_topic')
        msg = Mock()
        
        with patch('commonfunction.producer_base.record_message_sent') as mock_record:
            producer.delivery_report(None, msg)
            mock_record.assert_called_once()
    
    @patch('commonfunction.producer_base.Producer')
    @patch('commonfunction.producer_base.start_metrics_server')
    def test_delivery_report_error(self, mock_metrics, mock_producer):
        producer = BaseProducer('test_client', 'test_topic')
        
        with patch('commonfunction.producer_base.record_error') as mock_error:
            producer.delivery_report("Error occurred", None)
            mock_error.assert_called_once()
    
    @patch('commonfunction.producer_base.Producer')
    @patch('commonfunction.producer_base.start_metrics_server')
    def test_message_count_polling(self, mock_metrics, mock_producer):
        mock_producer_instance = Mock()
        mock_producer.return_value = mock_producer_instance
        
        producer = BaseProducer('test_client', 'test_topic')
        
        # Send 10 messages to trigger polling
        for i in range(10):
            producer.send_message({"patient_id": f"P{i:04d}"})
        
        mock_producer_instance.poll.assert_called_with(0)
        assert producer.message_count == 10