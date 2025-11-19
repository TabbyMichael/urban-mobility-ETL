import requests
import pandas as pd
import os
from typing import Dict, List, Optional
from datetime import datetime
import json

class MTAGTFSExtractor:
    """Handle extraction of MTA GTFS data"""
    
    def __init__(self):
        self.api_key = os.getenv('MTA_API_KEY')
        self.base_url = "https://api.mta.info"
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'x-api-key': self.api_key})
    
    def get_subway_lines(self) -> List[Dict]:
        """Get list of subway lines"""
        try:
            # Check if API key is available
            if not self.api_key:
                # Return sample data for development
                sample_lines = [
                    {"line_id": "1", "name": "1 Broadway-7 Avenue", "color": "#EE352E"},
                    {"line_id": "2", "name": "2 7 Avenue", "color": "#EE352E"},
                    {"line_id": "3", "name": "3 7 Avenue", "color": "#EE352E"},
                    {"line_id": "4", "name": "4 Lexington Avenue", "color": "#00933C"},
                    {"line_id": "5", "name": "5 Lexington Avenue", "color": "#00933C"},
                    {"line_id": "6", "name": "6 Lexington Avenue", "color": "#00933C"},
                    {"line_id": "7", "name": "7 Flushing", "color": "#B933AD"},
                    {"line_id": "A", "name": "A 8 Avenue", "color": "#2850AD"},
                    {"line_id": "C", "name": "C 8 Avenue", "color": "#2850AD"},
                    {"line_id": "E", "name": "E 8 Avenue", "color": "#2850AD"},
                ]
                return sample_lines
            
            # In a real implementation, you would call the actual MTA API
            # For now, we'll return sample data as the actual API requires specific endpoints
            sample_lines = [
                {"line_id": "1", "name": "1 Broadway-7 Avenue", "color": "#EE352E"},
                {"line_id": "2", "name": "2 7 Avenue", "color": "#EE352E"},
                {"line_id": "3", "name": "3 7 Avenue", "color": "#EE352E"},
                {"line_id": "4", "name": "4 Lexington Avenue", "color": "#00933C"},
                {"line_id": "5", "name": "5 Lexington Avenue", "color": "#00933C"},
                {"line_id": "6", "name": "6 Lexington Avenue", "color": "#00933C"},
                {"line_id": "7", "name": "7 Flushing", "color": "#B933AD"},
                {"line_id": "A", "name": "A 8 Avenue", "color": "#2850AD"},
                {"line_id": "C", "name": "C 8 Avenue", "color": "#2850AD"},
                {"line_id": "E", "name": "E 8 Avenue", "color": "#2850AD"},
            ]
            return sample_lines
        except Exception as e:
            print(f"Error fetching subway lines: {str(e)}")
            return []
    
    def get_realtime_feed(self, feed_id: int = 1) -> pd.DataFrame:
        """
        Get real-time transit feed data
        
        Args:
            feed_id: Feed ID (1 for Subway, 2 for Bus, etc.)
            
        Returns:
            DataFrame with real-time transit data
        """
        try:
            # Check if API key is available
            if not self.api_key:
                # Return sample data for development
                sample_data = {
                    "trip_id": ["T1001", "T1002", "T1003", "T1004", "T1005"],
                    "route_id": ["1", "2", "3", "4", "5"],
                    "stop_id": ["S5001", "S5002", "S5003", "S5004", "S5005"],
                    "arrival_time": [
                        "2025-11-06T10:15:00Z", 
                        "2025-11-06T10:30:00Z", 
                        "2025-11-06T10:45:00Z",
                        "2025-11-06T11:00:00Z",
                        "2025-11-06T11:15:00Z"
                    ],
                    "departure_time": [
                        "2025-11-06T10:16:00Z", 
                        "2025-11-06T10:31:00Z", 
                        "2025-11-06T10:46:00Z",
                        "2025-11-06T11:01:00Z",
                        "2025-11-06T11:16:00Z"
                    ],
                    "status": ["ON_TIME", "DELAYED", "ON_TIME", "ON_TIME", "DELAYED"]
                }
                return pd.DataFrame(sample_data)
            
            # In a real implementation, you would call the actual MTA GTFS-realtime API
            # Example endpoint: https://api.mta.info/gtfs-realtime/feed/{feed_id}
            # For now, we'll return sample data as the actual API requires protobuf decoding
            sample_data = {
                "trip_id": ["T1001", "T1002", "T1003", "T1004", "T1005"],
                "route_id": ["1", "2", "3", "4", "5"],
                "stop_id": ["S5001", "S5002", "S5003", "S5004", "S5005"],
                "arrival_time": [
                    "2025-11-06T10:15:00Z", 
                    "2025-11-06T10:30:00Z", 
                    "2025-11-06T10:45:00Z",
                    "2025-11-06T11:00:00Z",
                    "2025-11-06T11:15:00Z"
                ],
                "departure_time": [
                    "2025-11-06T10:16:00Z", 
                    "2025-11-06T10:31:00Z", 
                    "2025-11-06T10:46:00Z",
                    "2025-11-06T11:01:00Z",
                    "2025-11-06T11:16:00Z"
                ],
                "status": ["ON_TIME", "DELAYED", "ON_TIME", "ON_TIME", "DELAYED"]
            }
            
            return pd.DataFrame(sample_data)
        except Exception as e:
            print(f"Error fetching real-time feed: {str(e)}")
            # Return empty DataFrame with expected columns
            df = pd.DataFrame()
            df.columns = [
                'trip_id', 'route_id', 'stop_id', 'arrival_time', 
                'departure_time', 'status'
            ]
            return df
    
    def get_service_alerts(self) -> pd.DataFrame:
        """
        Get service alerts and disruptions
        
        Returns:
            DataFrame with service alert data
        """
        try:
            # Check if API key is available
            if not self.api_key:
                # Return sample data for development
                sample_alerts = {
                    "alert_id": ["A001", "A002", "A003"],
                    "route_id": ["1", "4", "L"],
                    "stop_id": ["S1001", "S4001", "SL001"],
                    "reason": [
                        "Signal problems", 
                        "Track maintenance", 
                        "Station accessibility issue"
                    ],
                    "effect": ["DELAY", "PLANNED_WORK", "ACCESSIBILITY_ISSUE"],
                    "created_at": [
                        "2025-11-06T08:00:00Z",
                        "2025-11-06T09:30:00Z",
                        "2025-11-06T10:15:00Z"
                    ]
                }
                return pd.DataFrame(sample_alerts)
            
            # In a real implementation, you would call the actual MTA service alerts API
            # For now, we'll return sample data as the actual API requires specific endpoints
            sample_alerts = {
                "alert_id": ["A001", "A002", "A003"],
                "route_id": ["1", "4", "L"],
                "stop_id": ["S1001", "S4001", "SL001"],
                "reason": [
                    "Signal problems", 
                    "Track maintenance", 
                    "Station accessibility issue"
                ],
                "effect": ["DELAY", "PLANNED_WORK", "ACCESSIBILITY_ISSUE"],
                "created_at": [
                    "2025-11-06T08:00:00Z",
                    "2025-11-06T09:30:00Z",
                    "2025-11-06T10:15:00Z"
                ]
            }
            
            return pd.DataFrame(sample_alerts)
        except Exception as e:
            print(f"Error fetching service alerts: {str(e)}")
            # Return empty DataFrame with expected columns
            df = pd.DataFrame()
            df.columns = [
                'alert_id', 'route_id', 'stop_id', 'reason', 'effect', 'created_at'
            ]
            return df

# Example usage
if __name__ == "__main__":
    extractor = MTAGTFSExtractor()
    
    # Get sample data
    realtime_data = extractor.get_realtime_feed()
    print("Sample MTA real-time data:")
    print(realtime_data.head())