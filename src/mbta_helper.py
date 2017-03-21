import urllib.request   # urlencode function
import json
from pprint import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json?"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """

    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    query = {'address': place_name}
    encoded_query = urllib.parse.urlencode(query)
    new_url = GMAPS_BASE_URL + encoded_query

    response = get_json(new_url)['results'][0]['geometry']['location']

    latitude = response['lat']
    longitude = response['lng']
    return latitude, longitude


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.
    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """

    query = {'api_key': MBTA_DEMO_API_KEY, 'lat': latitude, 'lon': longitude}
    encoded_query = urllib.parse.urlencode(query)

    url = MBTA_BASE_URL + '?' + encoded_query
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)

    # find minimum
    min_distance = float(response_data['stop'][0]['distance'])
    station = response_data['stop'][0]['stop_name']
    for i in range(len(response_data['stop'])):
        distance = float(response_data['stop'][i]['distance'])
        if distance < min_distance:
            min_distance = distance
            station = response_data['stop'][i]['stop_name']
    return station, round(min_distance,4)


def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and the
    distance from the given place to that stop.
    """
    lat, lng = get_lat_long(place_name)
    return get_nearest_station(lat, lng)
