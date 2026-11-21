import requests 
import io
import zipfile 
import polars as pl

response = requests.get(url="https://gtfs.edmonton.ca/TMGTFSRealTimeWebService/GTFS/gtfs.zip")

with zipfile.ZipFile(io.BytesIO(response.content)) as z: 
    stop_times_data = pl.read_csv(z.open("stop_times.txt"))
    routes_data = pl.read_csv(z.open("routes.txt"))
    trips_data = pl.read_csv(z.open("trips.txt"))


