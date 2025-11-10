#!/usr/bin/env python3

import json
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from confluent_kafka import Consumer, KafkaError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'icu_alert_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

active_alerts = []

class ICUAlertListener:
    def __init__(self):
        self.conf = {
            'bootstrap.servers': 'kafka:9092',
            'group.id': 'icu_alert_ui',
            'auto.offset.reset': 'latest'
        }
        self.consumer = Consumer(self.conf)
        self.consumer.subscribe(['icu_alerts'])
        self.running = False
    
    def start_listening(self):
        self.running = True
        while self.running:
            try:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f'Error: {msg.error()}')
                        break
                
                alert_data = json.loads(msg.value().decode('utf-8'))
                self.process_alert(alert_data)
                
            except Exception as e:
                print(f'Error processing message: {e}')
    
    def process_alert(self, alert_data):
        global active_alerts
        active_alerts.insert(0, alert_data)
        if len(active_alerts) > 100:
            active_alerts.pop()
        
        socketio.emit('new_alert', alert_data)
    
    def stop(self):
        self.running = False
        self.consumer.close()

alert_listener = ICUAlertListener()

@app.route('/')
def index():
    return render_template('icu_alerts.html')

@socketio.on('connect')
def handle_connect():
    emit('alert_history', active_alerts)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def start_alert_listener():
    alert_listener.start_listening()

if __name__ == '__main__':
    listener_thread = threading.Thread(target=start_alert_listener, daemon=True)
    listener_thread.start()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)