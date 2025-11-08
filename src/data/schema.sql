-- Database schema for Urban Mobility Analytics
-- PostgreSQL with PostGIS extension required

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Taxi trips table
CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    vendor_id TEXT,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INTEGER,
    trip_distance NUMERIC,
    pickup_location_id INTEGER,
    dropoff_location_id INTEGER,
    pickup_geom GEOMETRY(POINT, 4326),
    dropoff_geom GEOMETRY(POINT, 4326),
    rate_code_id INTEGER,
    store_and_fwd_flag TEXT,
    payment_type TEXT,
    fare_amount NUMERIC,
    extra NUMERIC,
    mta_tax NUMERIC,
    tip_amount NUMERIC,
    tolls_amount NUMERIC,
    improvement_surcharge NUMERIC,
    total_amount NUMERIC,
    congestion_surcharge NUMERIC,
    airport_fee NUMERIC,
    trip_duration_minutes NUMERIC,
    speed_mph NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_trips_pickup_datetime ON trips(pickup_datetime);
CREATE INDEX IF NOT EXISTS idx_trips_pickup_location ON trips(pickup_location_id);
CREATE INDEX IF NOT EXISTS idx_trips_dropoff_location ON trips(dropoff_location_id);
CREATE INDEX IF NOT EXISTS idx_trips_pickup_geom ON trips USING GIST(pickup_geom);
CREATE INDEX IF NOT EXISTS idx_trips_dropoff_geom ON trips USING GIST(dropoff_geom);

-- Taxi zones reference table
CREATE TABLE IF NOT EXISTS zones (
    location_id INTEGER PRIMARY KEY,
    borough TEXT,
    zone TEXT,
    service_zone TEXT,
    geom GEOMETRY(MULTIPOLYGON, 4326)
);

-- Weather data table
CREATE TABLE IF NOT EXISTS weather (
    id SERIAL PRIMARY KEY,
    date DATE,
    temperature NUMERIC,
    precipitation NUMERIC,
    humidity NUMERIC,
    wind_speed NUMERIC,
    is_holiday BOOLEAN,
    is_weekend BOOLEAN
);

-- Uber travel times table
CREATE TABLE IF NOT EXISTS uber_travel_times (
    id SERIAL PRIMARY KEY,
    source_id INTEGER,
    dst_id INTEGER,
    mean_travel_time NUMERIC,
    standard_deviation NUMERIC,
    geometric_mean NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MTA status table
CREATE TABLE IF NOT EXISTS mta_status (
    id SERIAL PRIMARY KEY,
    route_id TEXT,
    trip_id TEXT,
    stop_id TEXT,
    arrival_time TIMESTAMP,
    departure_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ML features table
CREATE TABLE IF NOT EXISTS features_ml (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    location_id INTEGER,
    trip_count INTEGER,
    is_holiday BOOLEAN,
    is_weekend BOOLEAN,
    temperature NUMERIC,
    precipitation NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Insert default admin user (password: admin123)
-- In production, this should be removed and proper user management implemented
INSERT INTO users (username, password_hash, role) VALUES 
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PZvO.S', 'admin')
ON CONFLICT (username) DO NOTHING;