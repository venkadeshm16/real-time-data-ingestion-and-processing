#!/usr/bin/env python3

import json
from commonfunction.consumer_base import BaseConsumer
from commonfunction.minio_storage import MinIOStorage

# Initialize MinIO storage with batch processing
# Batch size: 10 alerts, Batch interval: 60 seconds
minio_storage = MinIOStorage(batch_size=10, batch_interval=60)

def handle_alert_message(data):
    print(json.dumps(data, indent=2))
    
    # Add alert to batch for later storage
    minio_storage.add_alert_to_batch(data)

if __name__ == '__main__':
    consumer = BaseConsumer('alert_consumer_group', 'icu_alerts')
    consumer.run(handle_alert_message)