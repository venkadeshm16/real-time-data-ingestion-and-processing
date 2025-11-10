#!/usr/bin/env python3

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import with mocking at the Minio level
with patch('minio.Minio'):
    from commonfunction.minio_storage import MinIOStorage

class TestMinIOStorage:
    
    @patch('commonfunction.minio_storage.Minio')
    @patch('commonfunction.minio_storage.Process')
    def test_init(self, mock_process, mock_minio):
        mock_client = Mock()
        mock_minio.return_value = mock_client
        mock_client.bucket_exists.return_value = False
        
        storage = MinIOStorage(batch_size=5, batch_interval=30)
        
        assert storage.batch_size == 5
        assert storage.batch_interval == 30
        mock_client.make_bucket.assert_called_once_with('icu-critical-alerts')
    
    @patch('commonfunction.minio_storage.Minio')
    @patch('commonfunction.minio_storage.Process')
    def test_add_alert_to_batch(self, mock_process, mock_minio):
        mock_client = Mock()
        mock_minio.return_value = mock_client
        mock_client.bucket_exists.return_value = True
        
        storage = MinIOStorage(batch_size=2)
        alert_data = {'alert_id': 'ALERT_001', 'patient_id': 'P0001'}
        
        storage.add_alert_to_batch(alert_data)
        
        assert len(storage.alert_batch) == 1
        assert storage.alert_batch[0] == alert_data
    
    @patch('commonfunction.minio_storage.Minio')
    @patch('commonfunction.minio_storage.Process')
    def test_batch_size_trigger(self, mock_process, mock_minio):
        mock_client = Mock()
        mock_minio.return_value = mock_client
        mock_client.bucket_exists.return_value = True
        
        storage = MinIOStorage(batch_size=2)
        
        with patch.object(storage, '_queue_batch_for_storage') as mock_queue:
            storage.add_alert_to_batch({'alert_id': 'ALERT_001'})
            storage.add_alert_to_batch({'alert_id': 'ALERT_002'})
            
            mock_queue.assert_called_once()
    
    @patch('commonfunction.minio_storage.Minio')
    @patch('commonfunction.minio_storage.Process')
    def test_flush_batch(self, mock_process, mock_minio):
        mock_client = Mock()
        mock_minio.return_value = mock_client
        mock_client.bucket_exists.return_value = True
        
        storage = MinIOStorage()
        storage.alert_batch = [{'alert_id': 'ALERT_001'}]
        
        with patch.object(storage, '_queue_batch_for_storage') as mock_queue:
            storage.flush_batch()
            mock_queue.assert_called_once()
