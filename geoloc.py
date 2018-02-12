import geocoder
from geopy.geocoders import Nominatim
from geopy import ArcGIS


def get_geo_position_geolocator(loc):
    """
    (str) -> tuple

    Function geocode adress and returns it's latitude and
    longitude using geolocator module
    """
    geolocator = Nominatim()
    location = geolocator.geocode(loc)
    return (location.latitude, location.longitude)


def get_geo_position_ArcGIS(loc):
    """
    (str) -> tuple

    Function geocode adress and returns it's latitude and
    longitude using ArcGIS API
    """
    locator = ArcGIS(timeout=10)
    place = locator.geocode(loc)
    return (place.latitude, place.longitude)


def get_geo_position_google(loc, api_key):
    """
    (str, str) -> tuple

    Function geocode adress and returns it's latitude and
    longitude using Google API. Enter your API key is necessary
    """
    g = geocoder.google(loc, key=api_key)
    return g.latlng
