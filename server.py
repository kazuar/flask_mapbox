
import json
import requests
from geojson import Point, Feature

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

ROUTE = [
    {"lat": 64.0027441, "long": -22.7066262, "name": "Keflavik Airport", "is_stop_location": True},
    {"lat": 64.0317168, "long": -22.1092311, "name": "Hafnarfjordur", "is_stop_location": True},
    {"lat": 63.99879, "long": -21.18802, "name": "Hveragerdi", "is_stop_location": True},
    {"lat": 63.4194089, "long": -19.0184548, "name": "Vik", "is_stop_location": True},
    {"lat": 63.5302354, "long": -18.8904333, "name": "Thakgil", "is_stop_location": True},
    {"lat": 64.2538507, "long": -15.2222918, "name": "Hofn", "is_stop_location": True},
    {"lat": 64.913435, "long": -14.01951, "is_stop_location": False},
    {"lat": 65.2622588, "long": -14.0179538, "name": "Seydisfjordur", "is_stop_location": True},
    {"lat": 65.2640083, "long": -14.4037548, "name": "Egilsstadir", "is_stop_location": True},
    {"lat": 66.0427545, "long": -17.3624953, "name": "Husavik", "is_stop_location": True},
    {"lat": 65.659786, "long": -20.723364, "is_stop_location": False},
    {"lat": 65.3958953, "long": -20.9580216, "name": "Hvammstangi", "is_stop_location": True},
    {"lat": 65.0722555, "long": -21.9704238, "is_stop_location": False},
    {"lat": 65.0189519, "long": -22.8767959, "is_stop_location": False},
    {"lat": 64.8929619, "long": -23.7260926, "name": "Olafsvik", "is_stop_location": True},
    {"lat": 64.785334, "long": -23.905765, "is_stop_location": False},
    {"lat": 64.174537, "long": -21.6480148, "name": "Mosfellsdalur", "is_stop_location": True},
    {"lat": 64.0792223, "long": -20.7535337, "name": "Minniborgir", "is_stop_location": True},
    {"lat": 64.14586, "long": -21.93955, "name": "Reykjavik", "is_stop_location": True},
]

ROUTE_URL = "https://api.mapbox.com/directions/v5/mapbox/driving/{0}.json?access_token={1}&overview=full&geometries=geojson"

def create_route_url():
    lat_longs = ";".join(["{0},{1}".format(point["long"], point["lat"]) for point in ROUTE])
    url = ROUTE_URL.format(lat_longs, MAPBOX_ACCESS_KEY)
    return url

def create_stop_location_detail(title, latitude, longitude, index):
    point = Point([longitude, latitude])
    properties = {
        "title": title,
        'icon': "campsite",
        'marker-color': '#3bb2d0',
        'marker-symbol': index
    }
    feature = Feature(geometry = point, properties = properties)
    return feature

def create_stop_locations_details():
    stop_locations = []
    for location in ROUTE:
        if not location["is_stop_location"]:
            continue
        stop_location = create_stop_location_detail(
            location['name'],
            location['lat'],
            location['long'],
            len(stop_locations) + 1
        )
        stop_locations.append(stop_location)
    return stop_locations

def get_route_data():
    route_url = create_route_url()
    result = requests.get(route_url)
    geometry = result.json()["routes"][0]["geometry"]
    print geometry.keys()
    route_data = Feature(geometry = geometry, properties = {})
    print route_data.keys()
    return route_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mapbox_js')
def mapbox_js():
    route_data = get_route_data()

    stop_locations = create_stop_locations_details()

    return render_template('mapbox_js.html', 
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        route_data=route_data["geometry"],
        stop_locations = stop_locations
    )

@app.route('/mapbox_gl')
def mapbox_gl():
    route_data = get_route_data()

    return render_template('mapbox_gl.html', 
        ACCESS_KEY=MAPBOX_ACCESS_KEY,
        route_data = route_data
    )
