#!/bin/bash

# Wait for Kafka to be ready
wait_for_kafka() {
    echo "Waiting for Kafka to be ready..."
    while ! nc -z kafka 9092; do
        sleep 1
    done
    echo "Kafka is ready!"
    sleep 5  # Additional delay for Kafka to fully initialize
}

case "$1" in
    "create-topics")
        wait_for_kafka
        cd data-producer && python create_topics.py
        ;;
    "producer-vitals")
        wait_for_kafka
        cd data-producer && python icu_vital.py
        ;;
    "producer-hms")
        wait_for_kafka
        cd data-producer && python hms.py
        ;;
    "producer-lab")
        wait_for_kafka
        cd data-producer && python lab.py
        ;;
    "producer-pharmacy")
        wait_for_kafka
        cd data-producer && python pharmacy.py
        ;;
    "producer-emergency")
        wait_for_kafka
        cd data-producer && python emergency.py
        ;;
    "consumer-vitals")
        wait_for_kafka
        cd data-consumer && python kafka_consumer.py
        ;;
    "consumer-hms")
        wait_for_kafka
        cd data-consumer && python hms_consumer.py
        ;;
    "consumer-lab")
        wait_for_kafka
        cd data-consumer && python lab_consumer.py
        ;;
    "consumer-pharmacy")
        wait_for_kafka
        cd data-consumer && python pharmacy_consumer.py
        ;;
    "consumer-emergency")
        wait_for_kafka
        cd data-consumer && python emergency_consumer.py
        ;;
    "consumer-alerts")
        wait_for_kafka
        cd data-consumer && python alert_consumer.py
        ;;
    *)
        echo "Usage: $0 {create-topics|producer-vitals|producer-hms|producer-lab|producer-pharmacy|producer-emergency|consumer-vitals|consumer-hms|consumer-lab|consumer-pharmacy|consumer-emergency|consumer-alerts}"
        exit 1
        ;;
esac