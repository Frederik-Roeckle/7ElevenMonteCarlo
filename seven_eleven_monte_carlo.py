import requests
import json
import dotenv
import os
from math import radians, cos, sin, asin, sqrt
import shapely
import geopandas as gpd
import tqdm
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

dotenv.load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# API
REVERSE_GEOLOCATION_API_BASE = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
PLACES_API_BASE = "https://places.googleapis.com/v1/places:searchText?fields=places.name,places.id,places.displayName,places.location&key="
ROUTE_API_BASE = "https://maps.googleapis.com/maps/api/directions/json?destination="
NEARBY_PLACES_API = "https://places.googleapis.com/v1/places:searchNearby?fields=places.displayName,places.formattedAddress,places.location,places.id,places.googleMapsLinks&key="


def get_reverse_geolocation_api_call(latlng):
    api_call = REVERSE_GEOLOCATION_API_BASE
    api_call += str(latlng[0]) + "," + str(latlng[1])
    api_call += "&result_type=street_address&key="
    api_call += GOOGLE_API_KEY
    return api_call

def get_places_api_call(text_search_query):
    api_call = PLACES_API_BASE
    api_call += GOOGLE_API_KEY
    api_call += "&textQuery="
    api_call += text_search_query
    return api_call

def get_route_api_call(destination, origin, transport_mode):
    api_call = ROUTE_API_BASE
    api_call += destination
    api_call += "&origin="
    api_call += origin
    api_call += "&mode="
    api_call += transport_mode
    api_call += "&key="
    api_call += GOOGLE_API_KEY
    return api_call

def get_nearby_places_api_call(latlon):
    """Results of this API are limited to 20 locations per response"""
    api_call = NEARBY_PLACES_API
    api_call += GOOGLE_API_KEY
    lat, lon = latlon
    payload = {
        "includedTypes": ["convenience_store"],
        "rankPreference": "DISTANCE",
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lon
                },
                "radius": 1000.0
            }
        }
    }
    return api_call, payload

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees) in x,xx [m]
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6378.137
    return round(c * r * 1000, 2)


# create a rectangle grid over Bangkok x1, x2, x3, x4 = UpperLeft, UpperRight, BottomLeft, BottomRight
x1 = (13.792176549543075, 100.46783783148831)
x2 = (13.793094841464807, 100.56780696491528)
x3 = (13.711144078982425, 100.4678598524839)
x4 = (13.709618838174725, 100.56747473097656)

# construct a polygon shape and convert it to a GeoDataFrame
polygon = shapely.geometry.Polygon([x1, x2, x4, x3, x1])
gdf = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[polygon])

# sample points from this shape
N_SAMPLE = 10000
sample_points = gdf.sample_points(N_SAMPLE)
sample_points = list(sample_points[0].geoms)
with open("Sample_Points_For_Finding_Stores.json", "w") as file:
    json.dump([(str(point.x),str(point.y)) for point in sample_points], file)


# transform coordinates into adresses with geolocation api
# for point in sample_points:
#     res = requests.get(get_reverse_geolocation_api_call((point.x, point.y)))
#     print(res.json()["results"][0]["formatted_address"])


conn = sqlite3.connect("SevenElevenLocations.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS locations (id TEXT, formattedAddress TEXT, latitude REAL, longitude REAL, displayNameText TEXT, googleMapsLinksPlaceURI TEXT)")

def get_nearby_places():
    # Use NearbyAPI to find convenience store close to sample point
    for point in tqdm.tqdm(sample_points):
        api_call, payload = get_nearby_places_api_call((point.x, point.y))
        res = requests.post(api_call, data=json.dumps(payload))
        if "places" in res.json():
            locations = []
            for location in res.json()["places"]:
                id = location["id"]
                formattedAddress = location["formattedAddress"]
                latitude = location["location"]["latitude"]
                longitude = location["location"]["longitude"]
                displayNameText = location["displayName"]["text"]
                googleMapsLinksPlaceURI = location["googleMapsLinks"]["placeUri"]
                location_data = (id, formattedAddress, latitude, longitude, displayNameText, googleMapsLinksPlaceURI)
                locations.append(location_data)
            db_res = cursor.executemany("INSERT INTO locations VALUES(?, ?, ?, ?, ?, ?)", locations)
            conn.commit()
get_nearby_places()


def calculate_distances():
    # Filter all unique 7-Eleven stores
    req = cursor.execute(r"SELECT DISTINCT * FROM locations WHERE displayNameText LIKE '%7-ELEVEN%'")
    stores = req.fetchall()

    # calculate min distance between each sample point and all 7-Eleven stores in the list
    N_SAMPLE = 200000
    sample_points = gdf.sample_points(N_SAMPLE)
    sample_points = list(sample_points[0].geoms)
    point_to_closest_store = {}
    for point in tqdm.tqdm(sample_points):
        shortest_dist = 10000
        for store in stores:
            if shortest_dist > haversine(point.x, point.y, store[2], store[3]):
                shortest_dist = haversine(point.x, point.y, store[2], store[3])
                point_to_closest_store[str(point.x) +","+str(point.y)] = (store[0], shortest_dist)
        
        # TODO: Use Route API to compute the walking distance

    with open("mapping_point_closest_store.json", "w") as file:
        json.dump(point_to_closest_store, file)

calculate_distances()

def visualize_mean_distance():
    with open("mapping_point_closest_store.json", "r") as file:
        point_to_closest_store = json.load(file)
    n = 1
    temporal_mean_average = []
    mean_average = list(point_to_closest_store.values())[0][1]
    for distance_mapping in list(point_to_closest_store.values()):
        mean_average = mean_average + ((1/n) * (distance_mapping[1] - mean_average))
        temporal_mean_average.append(mean_average)
        n += 1
    series_temporal_mean_average = pd.Series(temporal_mean_average)
    plt.figure(figsize=(15,8))
    series_temporal_mean_average.plot()
    plt.title("Incremental Mean of Distance to Closest 7-Eleven")
    plt.xlabel("Sample Index")
    plt.ylabel("Mean Distance in meter")
    plt.savefig("temporal_mean_average")

    print(f"Final Average is: {mean_average}m.")

visualize_mean_distance()