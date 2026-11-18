import polars as pl
import os
from dotenv import load_dotenv 

#postgresql://USER:PASSWORD@HOST:PORT/DATABASE
load_dotenv()
URI = f"postgresql+psycopg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/{os.environ['POSTGRES_DB']}?connect_timeout=5"
GTFS = "path" # General Transit Feed Specification (originally called the Google Transit Feed Specification)
ROUTE_IDS = ["007", "054", "108", "113"]

def read(name):
    return pl.read_csv(f"{GTFS}/{name}.txt", infer_schema=False)

with open("interested_routes.txt") as f:
    route_ids = [line.split(",")[0] for line in f if line.strip()]

routes = read("routes").filter(pl.col("route_id").is_in(ROUTE_IDS))
trips = read("trips").filter(pl.col("route_id").is_in(ROUTE_IDS))
stop_times = read("stop_times").filter(pl.col("trip_id").is_in(trips["trip_id"].implode()))
stops = read("stops").filter(pl.col("stop_id").is_in(stop_times["stop_id"].implode()))

tables = {
    "routes":     routes.select("route_id", "route_short_name", "route_long_name", "route_type"),
    "stops":      stops.select("stop_id", "stop_name", "stop_lat", pl.col("stop_lon").alias("stop_long")),
    "trips":      trips.select("trip_id", "route_id", "service_id", "direction_id", "shape_id"),
    "stop_times": stop_times.select("trip_id", "stop_id", "stop_sequence", "arrival_time", "departure_time"),
}

# insertion order matters because of the foreign keys
for name in ["routes", "stops", "trips", "stop_times"]:
    tables[name].write_database(name, URI, if_table_exists="append")
    print(f"{name}: {tables[name].height} rows")