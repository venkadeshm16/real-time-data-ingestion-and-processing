#!/usr/bin/env python3

import json
import time
import threading
from datetime import datetime
from confluent_kafka import Producer
from commonfunction.metrics import start_metrics_server, record_message_sent, record_error, set_active_producer

class BaseProducer:
    def __init__(self, client_id, topic_name):
        import os
        kafka_host = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        self.conf = {
            'bootstrap.servers': kafka_host,
            'client.id': client_id,
            'batch.size': 16384,
            'linger.ms': 10,
            'compression.type': 'snappy',
            'acks': 1
        }
        self.producer = Producer(self.conf)
        self.topic_name = topic_name
        self.client_id = client_id
        self.message_count = 0
        
        # Start metrics server in background thread
        threading.Thread(target=start_metrics_server, daemon=True).start()
        set_active_producer(client_id, True)
    
    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Delivery failed: {err}")
            record_error(self.topic_name, self.client_id)
        else:
            record_message_sent(self.topic_name, self.client_id)
    
    def send_message(self, data, key=None):
        self.producer.produce(
            topic=self.topic_name,
            key=key or data.get("patient_id"),
            value=json.dumps(data),
            callback=self.delivery_report
        )
        
        self.message_count += 1
        if self.message_count % 10 == 0:
            self.producer.poll(0)
            print(f"Sent {self.message_count} {self.topic_name} records")
    
    def run(self, data_generator, sleep_interval=1):
        try:
            while True:
                data = data_generator()
                self.send_message(data)
                time.sleep(sleep_interval)
        except KeyboardInterrupt:
            print(f"\nShutting down {self.topic_name} producer...")
        finally:
            set_active_producer(self.client_id, False)
            self.producer.flush()
            print(f"{self.topic_name} producer closed. Total messages: {self.message_count}")