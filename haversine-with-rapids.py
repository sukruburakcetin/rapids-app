import math
import time
import warnings

import cudf
import cuspatial
import pandas as pd

warnings.filterwarnings("ignore")

# Load worldCities Data
worldCities = pd.read_csv(r"static/data/in-main/worldCities.csv")

# Extract main location(suleymaniye kulliyesi) lat and lng => from
lon1 = 28.965305
lat1 = 41.015177

# Create column names, assign preloading values
worldCities["merged_travel_time"] = ""
worldCities["merged_distance"] = ""
worldCities["icon"] = "heart"

# Assign start location to the current DataFrame rows
worldCities["SULEYMANIYE_KULLIYESI_LAT"] = lat1
worldCities["SULEYMANIYE_KULLIYESI_LON"] = lon1

# Convert Pandas DataFrame to cuda dataFrame
worldCities = cudf.from_pandas(worldCities)

# Create cuSpatial GeoSeries for WorldCities Data from cuDF Dataframe
cuGeoSeries = cuspatial.GeoSeries.from_points_xy(worldCities[['lat', 'lng']].interleave_columns())

# Create cuSpatial GeoSeries for Input Data(Süleymaniye Külliyesi) from cuDF Dataframe
atlGeoSeries = cuspatial.GeoSeries.from_points_xy(
    worldCities[['SULEYMANIYE_KULLIYESI_LAT', 'SULEYMANIYE_KULLIYESI_LON']].interleave_columns())

# Start timer
start = time.time()

# Calculate Haversine Distance of cuDF dataframe to comparator point
worldCities['distance'] = cuspatial.haversine_distance(cuGeoSeries, atlGeoSeries)

# Stop timer
end = time.time()
print("python computing distance time in ms={}".format((end - start) * 1000))

# Calculate travel time
worldCities["travel_time"] = worldCities["distance"] / 820

# Split travel time into hours and minutes
worldCities['hours'] = worldCities['travel_time'].apply(lambda x: int(math.floor(x)))
worldCities['minutes'] = round((worldCities['travel_time'] - worldCities['hours']) * 60)

# Convert column names with meaningful tags in order to improve readability in Turkish
worldCities['merged_travel_time'] = worldCities["hours"].astype(str) + " saat" + worldCities['minutes'].astype(str) + " dakika"
worldCities['merged_distance'] = worldCities["distance"].astype(str) + " km"

# Rename column names to translate some of the columns into Turkish
worldCities.rename(columns={"city": "SEHIR", "country": "ULKE", "capital": "BASKENT", "population": "NUFUS", "merged_travel_time": "SEYAHAT_SURESI", "merged_distance": "MESAFE"}, inplace=True)

# Write current DataFrame to local as csv
worldCities.to_csv("./static/data/out-haversine-with-rapids/with_rapids_tr_worldCities.csv")
