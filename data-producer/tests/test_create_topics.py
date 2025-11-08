#!/usr/bin/env python3

import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from create_topics import create_topics

class TestCreateTopics:
    
    @patch('create_topics.AdminClient')
    def test_create_topics_success(self, mock_admin):
        mock_client = Mock()
        mock_admin.return_value = mock_client
        
        # Mock successful topic creation
        mock_future = Mock()
        mock_future.result.return_value = None
        mock_client.create_topics.return_value = {
            'icu_device_data': mock_future,
            'icu_hims_data': mock_future
        }
        
        create_topics()
        
        mock_admin.assert_called_once_with({'bootstrap.servers': 'kafka:9092'})
        mock_client.create_topics.assert_called_once()
    
    @patch('create_topics.AdminClient')
    def test_create_topics_already_exists(self, mock_admin):
        mock_client = Mock()
        mock_admin.return_value = mock_client
        
        # Mock topic already exists error
        mock_future = Mock()
        mock_future.result.side_effect = Exception("Topic already exists")
        mock_client.create_topics.return_value = {
            'icu_device_data': mock_future
        }
        
        create_topics()  # Should not raise exception
        
        mock_client.create_topics.assert_called_once()