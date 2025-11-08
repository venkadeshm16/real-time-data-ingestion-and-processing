#!/usr/bin/env python3

import pytest
import os
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_kafka_connections():
    """Mock all Kafka and external service connections during tests"""
    with patch('confluent_kafka.Producer'), \
         patch('confluent_kafka.Consumer'), \
         patch('minio.Minio'), \
         patch('prometheus_client.start_http_server'):
        yield

@pytest.fixture(autouse=True)
def set_test_env():
    """Set test environment variables"""
    os.environ['KAFKA_BOOTSTRAP_SERVERS'] = 'localhost:9092'
    os.environ['MINIO_ENDPOINT'] = 'localhost:9000'
    os.environ['MINIO_ACCESS_KEY'] = 'testkey'
    os.environ['MINIO_SECRET_KEY'] = 'testsecret'