#!/bin/bash

# Install test dependencies
pip3.11 install -r test_requirements.txt

# Set test environment to avoid Kafka connections
export KAFKA_BOOTSTRAP_SERVERS="localhost:9092"
export MINIO_ENDPOINT="localhost:9000"

# Run tests with coverage
python3.11 -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term --tb=short

echo "Tests completed. Coverage report generated in htmlcov/"