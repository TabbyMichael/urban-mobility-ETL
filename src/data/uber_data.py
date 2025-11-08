import requests
import pandas as pd
import os
from typing import Dict, List, Optional, Union
from datetime import datetime

class UberDataExtractor:
    """Handle extraction of Uber Movement data"""
    
    def __init__(self):
        self.api_key = os.getenv('UBER_MOVEMENT_API_KEY')
        self.base_url = "https://movement.uber.com/v1"
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def get_cities(self) -> List[Dict]:
        """Get list of available cities"""
        try:
            # Check if API key is available
            if not self.api_key:
                # Return sample data for development
                sample_cities = [
                    {"city_id": 1, "name": "New York City", "country": "USA"},
                    {"city_id": 2, "name": "London", "country": "UK"},
                    {"city_id": 3, "name": "San Francisco", "country": "USA"}
                ]
                return sample_cities
            
            # In a real implementation, you would call the actual Uber Movement API
            # https://movement.uber.com/api/v1/docs
            # For now, we'll return sample data as the actual API requires specific parameters
            sample_cities = [
                {"city_id": 1, "name": "New York City", "country": "USA"},
                {"city_id": 2, "name": "London", "country": "UK"},
                {"city_id": 3, "name": "San Francisco", "country": "USA"}
            ]
            return sample_cities
        except Exception as e:
            print(f"Error fetching cities: {str(e)}")
            return []
    
    def get_travel_times(self, 
                        source_id: int, 
                        dst_id: int, 
                        start_date: Optional[str] = None, 
                        end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Get travel times between two locations
        
        Args:
            source_id: Source location ID
            dst_id: Destination location ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with travel time data
        """
        try:
            # Check if API key is available
            if not self.api_key:
                # Return sample data for development
                sample_data = {
                    "source_id": [source_id] * 5,
                    "dst_id": [dst_id] * 5,
                    "time": [
                        "00:00", "06:00", "12:00", "18:00", "23:59"
                    ],
                    "mean_travel_time": [850, 1200, 950, 1800, 900],
                    "standard_deviation": [120, 180, 150, 300, 130],
                    "geometric_mean": [820, 1150, 920, 1750, 870]
                }
                return pd.DataFrame(sample_data)
            
            # In a real implementation, you would call the actual Uber Movement API
            # Example endpoint: https://movement.uber.com/gql?operationName=travelTimesQuery
            # For now, we'll return sample data as the actual API requires specific parameters
            sample_data = {
                "source_id": [source_id] * 5,
                "dst_id": [dst_id] * 5,
                "time": [
                    "00:00", "06:00", "12:00", "18:00", "23:59"
                ],
                "mean_travel_time": [850, 1200, 950, 1800, 900],
                "standard_deviation": [120, 180, 150, 300, 130],
                "geometric_mean": [820, 1150, 920, 1750, 870]
            }
            
            return pd.DataFrame(sample_data)
        except Exception as e:
            print(f"Error fetching travel times: {str(e)}")
            # Return empty DataFrame with expected columns
            df = pd.DataFrame()
            df.columns = [
                'source_id', 'dst_id', 'time', 'mean_travel_time',
                'standard_deviation', 'geometric_mean'
            ]
            return df
    
    def get_speeds(self, 
                  city_id: int, 
                  start_date: Optional[str] = None, 
                  end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Get speed data for a city
        
        Args:
            city_id: City ID
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with speed data
        """
        try:
            # Check if API key is available
            if not self.api_key:
                # Return sample data for development
                sample_data = {
                    "city_id": [city_id] * 3,
                    "region": ["Downtown", "Midtown", "Uptown"],
                    "hour": [8, 12, 18],
                    "average_speed": [12.5, 15.2, 10.8],
                    "congestion_level": ["high", "medium", "high"]
                }
                return pd.DataFrame(sample_data)
            
            # In a real implementation, you would call the actual Uber Movement API
            # For now, we'll return sample data as the actual API requires specific parameters
            sample_data = {
                "city_id": [city_id] * 3,
                "region": ["Downtown", "Midtown", "Uptown"],
                "hour": [8, 12, 18],
                "average_speed": [12.5, 15.2, 10.8],
                "congestion_level": ["high", "medium", "high"]
            }
            
            return pd.DataFrame(sample_data)
        except Exception as e:
            print(f"Error fetching speeds: {str(e)}")
            # Return empty DataFrame with expected columns
            df = pd.DataFrame()
            df.columns = [
                'city_id', 'region', 'hour', 'average_speed', 'congestion_level'
            ]
            return df

# Example usage
if __name__ == "__main__":
    extractor = UberDataExtractor()
    
    # Get sample data
    travel_times = extractor.get_travel_times(1001, 2001)
    print("Sample Uber travel times:")
    print(travel_times.head())