-- Indexes for performance optimization
-- This script should be run after the main schema is created

CREATE INDEX IF NOT EXISTS idx_trips_pickup_datetime ON trips(pickup_datetime);
CREATE INDEX IF NOT EXISTS idx_trips_pickup_location ON trips(pickup_location_id);
CREATE INDEX IF NOT EXISTS idx_trips_dropoff_location ON trips(dropoff_location_id);
CREATE INDEX IF NOT EXISTS idx_trips_pickup_geom ON trips USING GIST(pickup_geom);
CREATE INDEX IF NOT EXISTS idx_trips_dropoff_geom ON trips USING GIST(dropoff_geom);