import requests 
import io
import zipfile 
import polars as pl

response = requests.get(url="https://gtfs.edmonton.ca/TMGTFSRealTimeWebService/GTFS/gtfs.zip")

with zipfile.ZipFile(io.BytesIO(response.content)) as z: 
    print(z.namelist())
    z.extractall("path/")