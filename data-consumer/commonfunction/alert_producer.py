#!/usr/bin/env python3

import json
from datetime import datetime
from confluent_kafka import Producer
from commonfunction.metrics import record_alert_generated

class AlertProducer:
    def __init__(self):
        self.conf = {
            'bootstrap.servers': 'kafka:9092',
            'client.id': 'alert_producer',
            'batch.size': 16384,
            'linger.ms': 10,
            'compression.type': 'snappy',
            'acks': 1
        }
        self.producer = Producer(self.conf)
    
    def send_alert(self, parsed_data):
        alert = {
            'alert_id': f"ALERT_{parsed_data['patient_id']}_{int(datetime.now().timestamp())}",
            'patient_id': parsed_data['patient_id'],
            'data_type': parsed_data['data_type'],
            'status': parsed_data.get('status'),
            'priority': parsed_data.get('priority', 'CRITICAL'),
            'alert_timestamp': datetime.now().isoformat(),
            'original_data': parsed_data
        }
        
        self.producer.produce(
            topic='icu_alerts',
            key=parsed_data['patient_id'],
            value=json.dumps(alert)
        )
        self.producer.poll(0)
        record_alert_generated(parsed_data['data_type'])
        print(f"ALERT SENT: {alert['alert_id']}")
    
    def close(self):
        self.producer.flush()