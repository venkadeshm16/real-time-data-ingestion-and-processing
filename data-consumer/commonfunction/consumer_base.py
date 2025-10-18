#!/usr/bin/env python3

import json
import time
import threading
from confluent_kafka import Consumer
from commonfunction.metrics import start_metrics_server, record_message_consumed, record_error, set_active_consumer

class BaseConsumer:
    def __init__(self, group_id, topics):
        import os
        kafka_host = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')
        self.config = {
            'bootstrap.servers': kafka_host,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.config)
        self.topics = topics if isinstance(topics, list) else [topics]
        self.group_id = group_id
        
        # Start metrics server in background thread
        threading.Thread(target=start_metrics_server, daemon=True).start()
        set_active_consumer(group_id, True)
    
    def run(self, message_handler):
        self.consumer.subscribe(self.topics)
        
        try:
            while True:
                msg = self.consumer.poll(1.0)
                
                if msg is None:
                    continue
                if msg.error():
                    record_error(msg.topic(), self.group_id)
                    continue
                
                data = json.loads(msg.value().decode('utf-8'))
                message_handler(data)
                record_message_consumed(msg.topic(), self.group_id)
                
        except KeyboardInterrupt:
            pass
        finally:
            set_active_consumer(self.group_id, False)
            self.consumer.close()