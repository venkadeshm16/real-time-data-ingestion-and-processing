#!/usr/bin/env python3

import pytest
from unittest.mock import patch, Mock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commonfunction.metrics import (
    record_message_consumed, record_process_duration, record_error,
    set_active_consumer, record_alert_generated, start_metrics_server
)

class TestMetrics:
    
    @patch('commonfunction.metrics.messages_consumed_total')
    def test_record_message_consumed(self, mock_counter):
        record_message_consumed('test_topic', 'test_consumer')
        mock_counter.labels.assert_called_once_with(topic='test_topic', consumer='test_consumer')
    
    @patch('commonfunction.metrics.message_process_duration')
    def test_record_process_duration(self, mock_histogram):
        record_process_duration('test_topic', 'test_consumer', 0.5)
        mock_histogram.labels.assert_called_once_with(topic='test_topic', consumer='test_consumer')
    
    @patch('commonfunction.metrics.consumer_errors_total')
    def test_record_error(self, mock_counter):
        record_error('test_topic', 'test_consumer')
        mock_counter.labels.assert_called_once_with(topic='test_topic', consumer='test_consumer')
    
    @patch('commonfunction.metrics.active_consumers')
    def test_set_active_consumer(self, mock_gauge):
        set_active_consumer('test_consumer', True)
        mock_gauge.labels.assert_called_once_with(consumer='test_consumer')
    
    @patch('commonfunction.metrics.alerts_generated_total')
    def test_record_alert_generated(self, mock_counter):
        record_alert_generated('vitals')
        mock_counter.labels.assert_called_once_with(data_type='vitals')
    
    @patch('commonfunction.metrics.start_http_server')
    def test_start_metrics_server(self, mock_server):
        start_metrics_server()
        mock_server.assert_called_once_with(8081)