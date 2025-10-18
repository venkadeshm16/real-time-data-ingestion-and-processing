#!/usr/bin/env python3

from confluent_kafka.admin import AdminClient, NewTopic

def create_topics():
    admin_client = AdminClient({'bootstrap.servers': 'kafka:9092'})
    
    topics = [
        NewTopic(
            topic='icu_device_data',
            num_partitions=3,
            replication_factor=1
        ),
        NewTopic(
            topic='icu_hims_data',
            num_partitions=3,
            replication_factor=1
        ),
        NewTopic(
            topic='icu_lab_results',
            num_partitions=2,
            replication_factor=1
        ),
        NewTopic(
            topic='icu_pharmacy_data',
            num_partitions=2,
            replication_factor=1
        ),
        NewTopic(
            topic='icu_emergency_data',
            num_partitions=2,
            replication_factor=1
        ),
        NewTopic(
            topic='icu_alerts',
            num_partitions=2,
            replication_factor=1
        )
    ]
    
    fs = admin_client.create_topics(topics)
    
    for topic, f in fs.items():
        try:
            f.result()
            print(f"Topic '{topic}' created successfully")
        except Exception as e:
            if "already exists" in str(e):
                print(f"Topic '{topic}' already exists")
            else:
                print(f"Failed to create topic '{topic}': {e}")

if __name__ == '__main__':
    create_topics()