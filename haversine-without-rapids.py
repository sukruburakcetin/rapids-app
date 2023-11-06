import geopandas as gpd
import pandas as pd
import math
import time
import warnings

warnings.filterwarnings("ignore")


# Define the Haversine formula
# Function to calculate the distance between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    earth_radius = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance


# Load the DataFrames
myLocation = gpd.read_file(r"static/data/main/startLocation.shp")
worldCities = pd.read_csv(r"static/data/main/worldCities.csv")

# Start timer
start = time.time()

# Extract main location lat and lng => from
lon1 = myLocation['lng'][0]
lat1 = myLocation['lat'][0]

# Alternative for loop method (0)
# for j in range(len(worldCities)):
#     lat2 = worldCities["lng"][j]
#     lon2 = worldCities["lat"][j]
#     worldCities.loc[worldCities.index[j], ["distance"]] = haversine(lat1, lon1, lat2, lon2)

# Alternative list comprehension method (1)
# worldCities["distance"] = [haversine(lat1, lon1, worldCities["lat"][j], worldCities["lng"][j]) for j in range(len(worldCities))]

# Alternative lambda method (2)
worldCities["distance"] = worldCities.apply(lambda row: haversine(lat1, lon1, row["lat"], row["lng"]), axis=1)

# Stop timer
end = time.time()

print("python computing distance time in ms={}".format((end - start) * 1000))

# Calculate travel time
worldCities["travel_time"] = worldCities["distance"] / 820

print(worldCities)

# Write current DataFrame to local as csv
worldCities.to_csv("worldCities_without_rapids.csv")
