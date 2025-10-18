#!/usr/bin/env python3

import json
from commonfunction.consumer_base import BaseConsumer
from commonfunction.data_parser import DataParser
from commonfunction.alert_producer import AlertProducer

alert_producer = AlertProducer()

def handle_lab_message(data):
    parsed_data = DataParser.parse_lab(data)
    print(json.dumps(parsed_data, indent=2))
    
    if parsed_data['priority'] == 'CRITICAL':
        alert_producer.send_alert(parsed_data)

if __name__ == '__main__':
    consumer = BaseConsumer('lab_consumer_group', 'icu_lab_results')
    consumer.run(handle_lab_message)