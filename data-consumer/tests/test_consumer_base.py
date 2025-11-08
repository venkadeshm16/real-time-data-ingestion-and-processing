#!/usr/bin/env python3

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from commonfunction.consumer_base import BaseConsumer

class TestBaseConsumer:
    
    @patch('commonfunction.consumer_base.Consumer')
    @patch('commonfunction.consumer_base.start_metrics_server')
    @patch('commonfunction.consumer_base.set_active_consumer')
    def test_init(self, mock_set_active, mock_metrics, mock_consumer):
        consumer = BaseConsumer('test_group', 'test_topic')
        
        assert consumer.group_id == 'test_group'
        assert consumer.topics == ['test_topic']
        mock_consumer.assert_called_once()
        mock_set_active.assert_called_with('test_group', True)
    
    @patch('commonfunction.consumer_base.Consumer')
    @patch('commonfunction.consumer_base.start_metrics_server')
    @patch('commonfunction.consumer_base.set_active_consumer')
    def test_init_multiple_topics(self, mock_set_active, mock_metrics, mock_consumer):
        consumer = BaseConsumer('test_group', ['topic1', 'topic2'])
        
        assert consumer.topics == ['topic1', 'topic2']
    
    @patch('commonfunction.consumer_base.Consumer')
    @patch('commonfunction.consumer_base.start_metrics_server')
    @patch('commonfunction.consumer_base.set_active_consumer')
    @patch('commonfunction.consumer_base.record_message_consumed')
    def test_message_handling(self, mock_record, mock_set_active, mock_metrics, mock_consumer):
        mock_consumer_instance = Mock()
        mock_consumer.return_value = mock_consumer_instance
        
        # Mock message
        mock_msg = Mock()
        mock_msg.error.return_value = None
        mock_msg.value.return_value.decode.return_value = '{"patient_id": "P0001"}'
        mock_msg.topic.return_value = 'test_topic'
        
        # Mock poll to return message once then None
        mock_consumer_instance.poll.side_effect = [mock_msg, None, KeyboardInterrupt()]
        
        consumer = BaseConsumer('test_group', 'test_topic')
        handler = Mock()
        
        consumer.run(handler)
        
        handler.assert_called_once_with({"patient_id": "P0001"})
        mock_record.assert_called_once_with('test_topic', 'test_group')