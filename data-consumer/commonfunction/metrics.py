#!/usr/bin/env python3

import threading
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Consumer metrics
messages_consumed_total = Counter('kafka_messages_consumed_total', 'Total messages consumed from Kafka', ['topic', 'consumer'])
message_process_duration = Histogram('kafka_message_process_duration_seconds', 'Time spent processing messages', ['topic', 'consumer'])
consumer_errors_total = Counter('kafka_consumer_errors_total', 'Total consumer errors', ['topic', 'consumer'])
active_consumers = Gauge('kafka_active_consumers', 'Number of active consumers', ['consumer'])
alerts_generated_total = Counter('icu_alerts_generated_total', 'Total critical alerts generated', ['data_type'])

def start_metrics_server():
    """Start Prometheus metrics server on port 8081"""
    start_http_server(8081)
    print("Metrics server started on port 8081")

def record_message_consumed(topic, consumer_name):
    """Record a message consumed"""
    messages_consumed_total.labels(topic=topic, consumer=consumer_name).inc()

def record_process_duration(topic, consumer_name, duration):
    """Record message processing duration"""
    message_process_duration.labels(topic=topic, consumer=consumer_name).observe(duration)

def record_error(topic, consumer_name):
    """Record consumer error"""
    consumer_errors_total.labels(topic=topic, consumer=consumer_name).inc()

def set_active_consumer(consumer_name, active=True):
    """Set consumer as active/inactive"""
    active_consumers.labels(consumer=consumer_name).set(1 if active else 0)

def record_alert_generated(data_type):
    """Record critical alert generated"""
    alerts_generated_total.labels(data_type=data_type).inc()