#!/usr/bin/env python3

import threading
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Producer metrics
messages_sent_total = Counter('kafka_messages_sent_total', 'Total messages sent to Kafka', ['topic', 'producer'])
message_send_duration = Histogram('kafka_message_send_duration_seconds', 'Time spent sending messages', ['topic', 'producer'])
producer_errors_total = Counter('kafka_producer_errors_total', 'Total producer errors', ['topic', 'producer'])
active_producers = Gauge('kafka_active_producers', 'Number of active producers', ['producer'])

def start_metrics_server():
    """Start Prometheus metrics server on port 8081"""
    start_http_server(8081)
    print("Metrics server started on port 8081")

def record_message_sent(topic, producer_name):
    """Record a message sent"""
    messages_sent_total.labels(topic=topic, producer=producer_name).inc()

def record_send_duration(topic, producer_name, duration):
    """Record message send duration"""
    message_send_duration.labels(topic=topic, producer=producer_name).observe(duration)

def record_error(topic, producer_name):
    """Record producer error"""
    producer_errors_total.labels(topic=topic, producer=producer_name).inc()

def set_active_producer(producer_name, active=True):
    """Set producer as active/inactive"""
    active_producers.labels(producer=producer_name).set(1 if active else 0)