#!/usr/bin/env python3

import pytest
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commonfunction.metrics import (
    record_message_sent, record_send_duration, record_error, 
    set_active_producer, start_metrics_server
)

class TestMetrics:
    
    @patch('commonfunction.metrics.messages_sent_total')
    def test_record_message_sent(self, mock_counter):
        record_message_sent('test_topic', 'test_producer')
        mock_counter.labels.assert_called_once_with(topic='test_topic', producer='test_producer')
    
    @patch('commonfunction.metrics.producer_errors_total')
    def test_record_error(self, mock_counter):
        record_error('test_topic', 'test_producer')
        mock_counter.labels.assert_called_once_with(topic='test_topic', producer='test_producer')
    
    @patch('commonfunction.metrics.active_producers')
    def test_set_active_producer(self, mock_gauge):
        set_active_producer('test_producer', True)
        mock_gauge.labels.assert_called_once_with(producer='test_producer')
    
    @patch('commonfunction.metrics.start_http_server')
    def test_start_metrics_server(self, mock_server):
        start_metrics_server()
        mock_server.assert_called_once_with(8081)