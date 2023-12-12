import math
import time
import warnings

import pandas as pd

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

    return round(distance)


# Load the worldCities data to the DataFrame
worldCities = pd.read_csv(r"static/data/in-main/worldCities.csv")

worldCities["merged_travel_time"] = ""
worldCities["merged_distance"] = ""
worldCities["icon"] = "heart"

# Extract main location(suleymaniye kulliyesi) lat and lng => from
lon1 = 28.965305
lat1 = 41.015177

# Assign start location to the current DataFrame rows
worldCities["SULEYMANIYE_KULLIYESI_LAT"] = lat1
worldCities["SULEYMANIYE_KULLIYESI_LON"] = lon1

# Start timer
start = time.time()

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

# Split travel time into hours and minutes
worldCities['hours'] = worldCities['travel_time'].apply(lambda x: int(math.floor(x)))
worldCities['minutes'] = round((worldCities['travel_time'] - worldCities['hours']) * 60)
worldCities['minutes'] = worldCities['minutes'].astype(int)

# Convert column names with meaningful tags in order to improve readability in Turkish (saat = hour ; dakika = minute)
worldCities['merged_travel_time'] = worldCities["hours"].astype(str) + " saat " + worldCities['minutes'].astype(
    str) + " dakika"
worldCities['merged_distance'] = worldCities["distance"].astype(str) + " km"

# Rename column names to translate some of the columns into Turkish
worldCities.rename(columns={"city": "SEHIR", "country": "ULKE", "capital": "BASKENT", "population": "NUFUS",
                            "merged_travel_time": "SEYAHAT_SURESI", "merged_distance": "MESAFE"}, inplace=True)

# Write current DataFrame to local as csv
worldCities.to_csv("./static/data/out-haversine-without-rapids/without_rapids_tr_worldCities.csv")
