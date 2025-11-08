#!/bin/bash

# Install test dependencies
pip3.11 install -r test_requirements.txt

# Run tests with coverage
python3.11 -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term

echo "Tests completed. Coverage report generated in htmlcov/"