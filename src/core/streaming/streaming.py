import json
import time
import threading
from flask_socketio import SocketIO, emit
from src.data.taxi_data import TaxiDataExtractor
from src.data.database import DatabaseManager
import pandas as pd

class RealTimeStreamer:
    def __init__(self, app=None):
        self.socketio = SocketIO(cors_allowed_origins="*") if app is None else SocketIO(app, cors_allowed_origins="*")
        self.taxi_extractor = TaxiDataExtractor()
        self.db_manager = DatabaseManager()
        self.streaming_active = False
        self.streaming_thread = None
        
        # Register SocketIO events
        self.register_events()
    
    def init_app(self, app):
        """Initialize SocketIO with Flask app"""
        self.socketio.init_app(app, cors_allowed_origins="*")
    
    def register_events(self):
        """Register SocketIO event handlers"""
        @self.socketio.on('connect')
        def handle_connect():
            print('Client connected')
            emit('status', {'msg': 'Connected to real-time stream'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            print('Client disconnected')
        
        @self.socketio.on('start_streaming')
        def handle_start_streaming(data):
            dataset_id = data.get('dataset_id', 't29m-gskq')
            interval = data.get('interval', 5)  # seconds
            self.start_streaming(dataset_id, interval)
            emit('streaming_status', {'status': 'started'})
        
        @self.socketio.on('stop_streaming')
        def handle_stop_streaming():
            self.stop_streaming()
            emit('streaming_status', {'status': 'stopped'})
    
    def start_streaming(self, dataset_id='t29m-gskq', interval=5):
        """Start real-time data streaming"""
        if not self.streaming_active:
            self.streaming_active = True
            self.streaming_thread = threading.Thread(
                target=self._stream_data, 
                args=(dataset_id, interval)
            )
            self.streaming_thread.start()
    
    def stop_streaming(self):
        """Stop real-time data streaming"""
        self.streaming_active = False
        if self.streaming_thread:
            self.streaming_thread.join()
    
    def _stream_data(self, dataset_id, interval):
        """Internal method to stream data"""
        while self.streaming_active:
            try:
                # Extract recent taxi data
                df = self.taxi_extractor.extract_taxi_trips(dataset_id, limit=10)
                
                if not df.empty:
                    # Convert to JSON-serializable format
                    data = df.to_dict('records')
                    
                    # Emit data to all connected clients
                    self.socketio.emit('taxi_data', {
                        'timestamp': time.time(),
                        'data': data,
                        'count': len(data)
                    })
                
                # Wait for the specified interval
                time.sleep(interval)
                
            except Exception as e:
                print(f"Error in streaming: {e}")
                self.socketio.emit('error', {'msg': f'Streaming error: {str(e)}'})
                time.sleep(interval)
    
    def stream_analytics(self):
        """Stream analytics data periodically"""
        def analytics_worker():
            while self.streaming_active:
                try:
                    # Get analytics data from database
                    query = """
                        SELECT 
                            COUNT(*) as total_trips,
                            AVG(fare_amount) as avg_fare,
                            AVG(trip_distance) as avg_distance
                        FROM trips 
                        WHERE pickup_datetime > NOW() - INTERVAL '1 hour'
                    """
                    df = self.db_manager.execute_query(query)
                    
                    if not df.empty:
                        analytics_data = df.to_dict('records')[0]
                        self.socketio.emit('analytics_data', {
                            'timestamp': time.time(),
                            'data': analytics_data
                        })
                    
                    # Wait 30 seconds before next analytics update
                    time.sleep(30)
                    
                except Exception as e:
                    print(f"Error in analytics streaming: {e}")
                    time.sleep(30)
        
        # Start analytics worker in separate thread
        analytics_thread = threading.Thread(target=analytics_worker)
        analytics_thread.start()

# Global instance
streamer = RealTimeStreamer()