CREATE TABLE routes (
    route_id TEXT PRIMARY KEY, 
    route_short_name TEXT, 
    route_long_name TEXT,
    route_type INT 
);

CREATE TABLE stops ( 
    stop_id TEXT PRIMARY KEY, 
    stop_name TEXT NOT NULL, 
    stop_lat DOUBLE PRECISION, 
    stop_lon DOUBLE PRECISION
); 

CREATE TABLE trips (
    trip_id TEXT PRIMARY KEY, 
    route_id TEXT NOT NULL REFERENCES routes(route_id),
    service_id TEXT NOT NULL,
    direction_id INT, 
    shape_id TEXT
);

CREATE TABLE stop_times (
    trip_id TEXT NOT NULL REFERENCES trips(trip_id),
    stop_id TEXT NOT NULL REFERENCES stops(stop_id), 
    stop_sequence INT NOT NULL, 
    arrival_time INTERVAL, 
    departure_time INTERVAL, 
    PRIMARY KEY (trip_id, stop_sequence)
);

CREATE INDEX ON stop_times (stop_id); 

