import requests
import json
import dotenv
import os
from math import radians, cos, sin, asin, sqrt
import shapely
import geopandas as gpd

dotenv.load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# API
REVERSE_GEOLOCATION_API_BASE = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
PLACES_API_BASE = "https://places.googleapis.com/v1/places:searchText?fields=places.name,places.id,places.displayName,places.location&key="
ROUTE_API_BASE = "https://maps.googleapis.com/maps/api/directions/json?destination="

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
N_SAMPLE = 2
sample_points = gdf.sample_points(N_SAMPLE)
sample_points = list(sample_points[0].geoms)


# transform coordinates into adresses with geolocation api
for point in sample_points:
    res = requests.get(get_reverse_geolocation_api_call((point.x, point.y)))
    print(res.json()["results"][0]["formatted_address"])

# Use NearbyAPI



# use places api text search to get all nearby 7Eleven around each place
# 
# MC sample coordinates over Bangkok (perhaps reverse geocode again into adresses)
# 
# Find shortest manhattan distance between sampled points and all 7/eleven locations
#
# (Use Route API to compute the walking distance as formula for coordinates-2-meter is complex 

# Note 
