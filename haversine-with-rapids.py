import time
import warnings

import cudf
import cuspatial
import geopandas as gpd
import pandas as pd

warnings.filterwarnings("ignore")

# Load the DataFrames
myLocation = gpd.read_file(r"static/data/main/startLocation.shp")
worldCities = pd.read_csv(r"static/data/main/worldCities.csv")

# Convert Pandas DataFrame to
worldCities = cudf.from_pandas(worldCities)
start = time.time()

# Create cuSpatial GeoSeries from cuDF Dataframe
cuGeoSeries = cuspatial.GeoSeries.from_points_xy(worldCities[['lat', 'lng']].interleave_columns())

# Assign start location to the current DataFrame rows
worldCities["myLocation_lat"] = myLocation["lat"][0]
worldCities["myLocation_lng"] = myLocation["lng"][0]

# Create cuSpatial GeoSeries from cuDF Dataframe
atlGeoSeries = cuspatial.GeoSeries.from_points_xy(worldCities[['myLocation_lat', 'myLocation_lng']].interleave_columns())

# Calculate Haversine Distance of cuDF dataframe to comparator point
worldCities['distance'] = cuspatial.haversine_distance(cuGeoSeries, atlGeoSeries)
end = time.time()
print("python computing distance time in ms={}".format((end - start) * 1000))

# Calculate travel time
worldCities["travel_time"] = worldCities["distance"] / 820

print(worldCities)

# Write current DataFrame to local as csv
worldCities.to_csv("worldCities_with_rapids.csv")