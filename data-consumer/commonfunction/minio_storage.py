#!/usr/bin/env python3

import json
import os
import threading
import time
from datetime import datetime
from multiprocessing import Process, Queue
from minio import Minio
from minio.error import S3Error
from io import BytesIO

class MinIOStorage:
    def __init__(self, batch_size=10, batch_interval=60):
        self.client = Minio(
            os.getenv('MINIO_ENDPOINT', 'minio:9000'),
            access_key=os.getenv('MINIO_ACCESS_KEY', 'admin'),
            secret_key=os.getenv('MINIO_SECRET_KEY', 'changeme123'),
            secure=False
        )
        self.bucket_name = 'icu-critical-alerts'
        self.batch_size = batch_size
        self.batch_interval = batch_interval
        self.alert_batch = []
        self.batch_lock = threading.Lock()
        self.batch_queue = Queue(maxsize=100)  # Buffer for batches
        self._ensure_bucket_exists()
        self._start_batch_timer()
        self._start_storage_worker()
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Created bucket: {self.bucket_name}")
        except S3Error as e:
            print(f"Error creating bucket: {e}")
    
    def add_alert_to_batch(self, alert_data):
        """Add alert to batch for later storage"""
        with self.batch_lock:
            self.alert_batch.append(alert_data)
            print(f"Added alert to batch. Batch size: {len(self.alert_batch)}")
            
            # Store batch if it reaches batch_size
            if len(self.alert_batch) >= self.batch_size:
                self._queue_batch_for_storage()
    
    def _start_batch_timer(self):
        """Start timer to store batch periodically"""
        def timer_worker():
            while True:
                time.sleep(self.batch_interval)
                with self.batch_lock:
                    if self.alert_batch:
                        self._queue_batch_for_storage()
        
        timer_thread = threading.Thread(target=timer_worker, daemon=True)
        timer_thread.start()
    
    def _queue_batch_for_storage(self):
        """Queue batch for background storage"""
        if not self.alert_batch:
            return
        
        # Copy batch data and clear immediately
        batch_copy = self.alert_batch.copy()
        self.alert_batch.clear()
        
        try:
            # Add to queue (non-blocking)
            self.batch_queue.put_nowait(batch_copy)
            print(f"Queued batch with {len(batch_copy)} alerts for storage")
        except:
            print(f"Queue full, dropping batch with {len(batch_copy)} alerts")
    
    def _start_storage_worker(self):
        """Start background worker process for MinIO storage"""
        worker = Process(target=self._storage_worker, daemon=True)
        worker.start()
        print("Started MinIO storage worker process")
    
    def _storage_worker(self):
        """Background worker to process batch queue"""
        # Create MinIO client in worker process
        client = Minio(
            os.getenv('MINIO_ENDPOINT', 'minio:9000'),
            access_key=os.getenv('MINIO_ACCESS_KEY', 'admin'),
            secret_key=os.getenv('MINIO_SECRET_KEY', 'changeme123'),
            secure=False
        )
        
        while True:
            try:
                # Get batch from queue (blocking)
                batch_data = self.batch_queue.get()
                
                # Create batch object name with timestamp
                timestamp = datetime.now().strftime('%Y/%m/%d/%H/%M')
                batch_id = int(datetime.now().timestamp())
                object_name = f"critical-alerts-batch/{timestamp}/batch_{batch_id}.json"
                
                # Create batch object
                batch_obj = {
                    'batch_id': batch_id,
                    'timestamp': datetime.now().isoformat(),
                    'alert_count': len(batch_data),
                    'alerts': batch_data
                }
                
                # Convert to JSON string
                batch_json = json.dumps(batch_obj, indent=2)
                
                # Store batch in MinIO
                client.put_object(
                    bucket_name=self.bucket_name,
                    object_name=object_name,
                    data=BytesIO(batch_json.encode('utf-8')),
                    length=len(batch_json.encode('utf-8')),
                    content_type='application/json'
                )
                
                print(f"Stored alert batch: {object_name} ({len(batch_data)} alerts)")
                
            except Exception as e:
                print(f"Error in storage worker: {e}")
    
    def flush_batch(self):
        """Force store current batch"""
        with self.batch_lock:
            if self.alert_batch:
                self._queue_batch_for_storage()