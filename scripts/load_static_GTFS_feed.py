import polars as pl
import os
from dotenv import load_dotenv
from sqlalchemy.types import Interval

#postgresql://USER:PASSWORD@HOST:PORT/DATABASE
load_dotenv()
URI = f"postgresql+psycopg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/{os.environ['POSTGRES_DB']}?connect_timeout=5"
GTFS = "path" # General Transit Feed Specification (originally called the Google Transit Feed Specification)
ROUTE_IDS = ["007", "054", "108", "113"]

def read(name):
    # some fields are padded with spaces (e.g. "  53.546309")
    return pl.read_csv(f"{GTFS}/{name}.txt", infer_schema=False).with_columns(pl.all().str.strip_chars())

with open("interested_routes.txt") as f:
    route_ids = [line.split(",")[0] for line in f if line.strip()]

routes = read("routes").filter(pl.col("route_id").is_in(ROUTE_IDS))
trips = read("trips").filter(pl.col("route_id").is_in(ROUTE_IDS))
stop_times = read("stop_times").filter(pl.col("trip_id").is_in(trips["trip_id"].implode()))
stops = read("stops").filter(pl.col("stop_id").is_in(stop_times["stop_id"].implode()))

tables = {
    "routes":     routes.select("route_id", "route_short_name", "route_long_name", pl.col("route_type").cast(pl.Int32)),
    "stops":      stops.select("stop_id", "stop_name", pl.col("stop_lat", "stop_lon").cast(pl.Float64)),
    "trips":      trips.select("trip_id", "route_id", "service_id", pl.col("direction_id").cast(pl.Int32), "shape_id"),
    "stop_times": stop_times.select("trip_id", "stop_id", pl.col("stop_sequence").cast(pl.Int32),
                                    "arrival_time", "departure_time"),
}

# "HH:MM:SS" strings (hours can be >= 24); typing them as Interval lets Postgres parse them
dtypes = {"stop_times": {"arrival_time": Interval(), "departure_time": Interval()}}

# insertion order matters because of the foreign keys
for name in ["routes", "stops", "trips", "stop_times"]:
    tables[name].write_database(name, URI, if_table_exists="append",
                                engine_options={"dtype": dtypes.get(name)})
    print(f"{name}: {tables[name].height} rows")