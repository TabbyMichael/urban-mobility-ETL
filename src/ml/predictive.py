import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.database import DatabaseManager

class PredictiveModels:
    """Predictive models for urban mobility analytics"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.trip_demand_model = None
        self.fraud_detection_model = None
        self.scaler = StandardScaler()
    
    def connect_to_database(self) -> bool:
        """Connect to the database"""
        return self.db_manager.connect()
    
    def close_database(self):
        """Close database connection"""
        self.db_manager.close()
    
    def prepare_trip_demand_features(self) -> pd.DataFrame:
        """Prepare features for trip demand forecasting"""
        query = """
            SELECT 
                EXTRACT(HOUR FROM timestamp) as hour,
                EXTRACT(DOW FROM timestamp) as day_of_week,
                EXTRACT(DOY FROM timestamp) as day_of_year,
                is_weekend,
                is_holiday,
                temperature,
                precipitation,
                location_id,
                trip_count
            FROM features_ml
            WHERE trip_count IS NOT NULL
        """
        return self.db_manager.execute_query(query)
    
    def train_trip_demand_model(self) -> Dict:
        """Train trip demand forecasting model"""
        try:
            # Get features
            df = self.prepare_trip_demand_features()
            
            if df.empty:
                return {"status": "failed", "message": "No data available for training"}
            
            # Prepare features and target
            feature_cols = ['hour', 'day_of_week', 'day_of_year', 'is_weekend', 
                          'is_holiday', 'temperature', 'precipitation', 'location_id']
            X = df[feature_cols]
            y = df['trip_count']
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train model
            self.trip_demand_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.trip_demand_model.fit(X_train_scaled, y_train)
            
            # Evaluate model
            y_pred = self.trip_demand_model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            
            return {
                "status": "success",
                "mse": mse,
                "mae": mae,
                "model_score": self.trip_demand_model.score(X_test_scaled, y_test)
            }
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def predict_trip_demand(self, features: pd.DataFrame) -> np.ndarray:
        """Predict trip demand for given features"""
        if self.trip_demand_model is None:
            raise ValueError("Model not trained yet. Call train_trip_demand_model() first.")
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make predictions
        predictions = self.trip_demand_model.predict(features_scaled)
        return predictions
    
    def prepare_fraud_detection_features(self) -> pd.DataFrame:
        """Prepare features for fare fraud detection"""
        query = """
            SELECT 
                trip_distance,
                fare_amount,
                tip_amount,
                total_amount,
                trip_duration_minutes,
                speed_mph,
                passenger_count,
                CASE 
                    WHEN trip_distance > 0 THEN fare_amount / trip_distance 
                    ELSE 0 
                END as fare_per_mile,
                CASE 
                    WHEN trip_duration_minutes > 0 THEN trip_distance / (trip_duration_minutes / 60)
                    ELSE 0
                END as calculated_speed
            FROM trips
            WHERE trip_distance IS NOT NULL 
                AND fare_amount IS NOT NULL
                AND trip_distance > 0
                AND fare_amount >= 0
        """
        return self.db_manager.execute_query(query)
    
    def train_fraud_detection_model(self) -> Dict:
        """Train fare fraud detection model"""
        try:
            # Get features
            df = self.prepare_fraud_detection_features()
            
            if df.empty:
                return {"status": "failed", "message": "No data available for training"}
            
            # Prepare features (no target needed for isolation forest)
            feature_cols = ['trip_distance', 'fare_amount', 'tip_amount', 'total_amount',
                          'trip_duration_minutes', 'speed_mph', 'passenger_count',
                          'fare_per_mile', 'calculated_speed']
            X = df[feature_cols]
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.fraud_detection_model = IsolationForest(contamination=0.1, random_state=42)
            self.fraud_detection_model.fit(X_scaled)
            
            # Predict anomalies
            anomalies = self.fraud_detection_model.predict(X_scaled)
            anomaly_count = sum(anomalies == -1)
            
            return {
                "status": "success",
                "anomaly_count": anomaly_count,
                "anomaly_percentage": anomaly_count / len(X) * 100
            }
        except Exception as e:
            return {"status": "failed", "message": str(e)}
    
    def detect_fraud(self, features: pd.DataFrame) -> np.ndarray:
        """Detect fraudulent trips"""
        if self.fraud_detection_model is None:
            raise ValueError("Model not trained yet. Call train_fraud_detection_model() first.")
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Detect anomalies
        predictions = self.fraud_detection_model.predict(features_scaled)
        return predictions

# Example usage
if __name__ == "__main__":
    ml_models = PredictiveModels()
    
    if ml_models.connect_to_database():
        print("Predictive Modeling Examples:")
        print("=" * 40)
        
        # Train trip demand model
        print("Training trip demand model...")
        result = ml_models.train_trip_demand_model()
        print(f"Training result: {result}")
        
        # Train fraud detection model
        print("\nTraining fraud detection model...")
        result = ml_models.train_fraud_detection_model()
        print(f"Training result: {result}")
        
        ml_models.close_database()
    else:
        print("Failed to connect to database")