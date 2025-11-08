"""
Airflow DAG for Urban Mobility ETL Pipeline
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
import sys
import os

# Add the project directory to the path
sys.path.append('/home/kzer00/Documents/Urban Mobility & Transportation Analytics ETL')

from src.data.taxi_data import TaxiDataExtractor
from src.data.etl_pipeline import ETLPipeline
import pandas as pd

# Default arguments for the DAG
default_args = {
    'owner': 'urban_mobility_team',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['data-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'urban_mobility_etl',
    default_args=default_args,
    description='ETL pipeline for Urban Mobility & Transportation Analytics',
    schedule_interval=timedelta(hours=1),  # Run every hour
    catchup=False,
    tags=['urban_mobility', 'etl', 'transportation'],
)

def extract_taxi_data(**context):
    """Extract NYC taxi data"""
    extractor = TaxiDataExtractor()
    
    # Extract recent taxi trips
    df = extractor.extract_taxi_trips(limit=1000)
    
    # Save to XCom for downstream tasks
    context['task_instance'].xcom_push(key='taxi_data', value=df.to_json())
    
    print(f"Extracted {len(df)} taxi records")
    return len(df)

def extract_uber_data(**context):
    """Extract Uber travel times data"""
    # In a real implementation, this would connect to Uber API
    # For now, we'll create sample data
    sample_data = pd.DataFrame({
        'source_id': [1001, 1002, 1003],
        'dst_id': [2001, 2002, 2003],
        'mean_travel_time': [850, 1200, 950],
        'standard_deviation': [120, 180, 150],
        'geometric_mean': [820, 1150, 920]
    })
    
    # Save to XCom for downstream tasks
    context['task_instance'].xcom_push(key='uber_data', value=sample_data.to_json())
    
    print(f"Extracted {len(sample_data)} Uber records")
    return len(sample_data)

def extract_transit_data(**context):
    """Extract MTA transit status data"""
    # In a real implementation, this would connect to MTA API
    # For now, we'll create sample data
    sample_data = pd.DataFrame({
        'route_id': ['R1', 'R2', 'R3'],
        'trip_id': ['T1001', 'T1002', 'T1003'],
        'stop_id': ['S5001', 'S5002', 'S5003'],
        'arrival_time': ['2025-11-06T10:15:00Z', '2025-11-06T10:30:00Z', '2025-11-06T10:45:00Z'],
        'departure_time': ['2025-11-06T10:16:00Z', '2025-11-06T10:31:00Z', '2025-11-06T10:46:00Z']
    })
    
    # Save to XCom for downstream tasks
    context['task_instance'].xcom_push(key='transit_data', value=sample_data.to_json())
    
    print(f"Extracted {len(sample_data)} transit records")
    return len(sample_data)

def run_etl_pipeline(**context):
    """Run the complete ETL pipeline"""
    # Get data from XCom
    taxi_json = context['task_instance'].xcom_pull(task_ids='extract_taxi_data', key='taxi_data')
    uber_json = context['task_instance'].xcom_pull(task_ids='extract_uber_data', key='uber_data')
    transit_json = context['task_instance'].xcom_pull(task_ids='extract_transit_data', key='transit_data')
    
    # Convert JSON back to DataFrames
    taxi_data = pd.read_json(taxi_json)
    uber_data = pd.read_json(uber_json)
    transit_data = pd.read_json(transit_json)
    
    # Run ETL pipeline
    pipeline = ETLPipeline()
    results = pipeline.run_full_pipeline(taxi_data, uber_data, transit_data)
    
    print("ETL Pipeline Results:")
    for source, success in results.items():
        print(f"  {source}: {'Success' if success else 'Failed'}")
    
    return results

def generate_ml_features(**context):
    """Generate features for ML modeling"""
    # In a real implementation, this would:
    # 1. Query the database for processed data
    # 2. Aggregate data for ML features
    # 3. Store features in features_ml table
    
    print("Generating ML features...")
    # Simulate feature generation
    feature_count = 1000
    print(f"Generated {feature_count} ML features")
    return feature_count

# Define tasks
extract_taxi_task = PythonOperator(
    task_id='extract_taxi_data',
    python_callable=extract_taxi_data,
    dag=dag,
)

extract_uber_task = PythonOperator(
    task_id='extract_uber_data',
    python_callable=extract_uber_data,
    dag=dag,
)

extract_transit_task = PythonOperator(
    task_id='extract_transit_data',
    python_callable=extract_transit_data,
    dag=dag,
)

run_etl_task = PythonOperator(
    task_id='run_etl_pipeline',
    python_callable=run_etl_pipeline,
    dag=dag,
)

generate_features_task = PythonOperator(
    task_id='generate_ml_features',
    python_callable=generate_ml_features,
    dag=dag,
)

# Set task dependencies
extract_taxi_task >> run_etl_task
extract_uber_task >> run_etl_task
extract_transit_task >> run_etl_task
run_etl_task >> generate_features_task