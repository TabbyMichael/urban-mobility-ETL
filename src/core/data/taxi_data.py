import requests
import pandas as pd
import os
from typing import Dict, List, Optional

class TaxiDataExtractor:
    """Handle extraction of NYC taxi data from the Open Data Portal"""
    
    def __init__(self, base_url: str = "https://data.cityofnewyork.us/resource/"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_dataset_metadata(self, dataset_id: str) -> Dict:
        """Get metadata for a specific dataset"""
        try:
            url = f"{self.base_url}{dataset_id}.json"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def extract_taxi_trips(self, 
                          dataset_id: str = "t29m-gskq",
                          limit: int = 1000,
                          offset: int = 0) -> pd.DataFrame:
        """
        Extract taxi trip data from NYC Open Data Portal
        
        Args:
            dataset_id: The dataset identifier on NYC Open Data Portal
            limit: Number of records to fetch
            offset: Offset for pagination
            
        Returns:
            DataFrame with taxi trip data
        """
        try:
            # Construct the API URL
            url = f"{self.base_url}{dataset_id}.json"
            params = {
                "$limit": limit,
                "$offset": offset,
                "$order": "pickup_datetime DESC"
            }
            
            # Make the API request
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            # Convert to DataFrame
            data = response.json()
            df = pd.DataFrame(data)
            
            return df
        except Exception as e:
            print(f"Error extracting taxi data: {str(e)}")
            # Return empty DataFrame with expected columns
            return pd.DataFrame(columns=[
                'pickup_datetime', 'dropoff_datetime', 'pickup_location_id',
                'dropoff_location_id', 'trip_distance', 'fare_amount',
                'tip_amount', 'total_amount'
            ])
    
    def extract_historical_data(self, 
                               dataset_id: str = "t29m-gskq",
                               months: int = 12) -> pd.DataFrame:
        """
        Extract historical taxi data for a specified number of months
        
        Args:
            dataset_id: The dataset identifier on NYC Open Data Portal
            months: Number of months of historical data to fetch
            
        Returns:
            DataFrame with historical taxi trip data
        """
        all_data = []
        
        # Fetch data in batches
        batch_size = 1000
        for i in range(0, months * 30, batch_size):
            try:
                df = self.extract_taxi_trips(dataset_id, batch_size, i)
                if df.empty:
                    break
                all_data.append(df)
            except Exception as e:
                print(f"Error fetching batch {i}: {str(e)}")
                break
                
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame()

# Example usage
if __name__ == "__main__":
    extractor = TaxiDataExtractor()
    
    # Get sample data
    sample_data = extractor.extract_taxi_trips(limit=10)
    print("Sample taxi data:")
    print(sample_data.head())