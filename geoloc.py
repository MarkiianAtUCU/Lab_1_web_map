import geocoder
from geopy.geocoders import Nominatim
from geopy import ArcGIS

def get_geo_position_geolocator(loc):
    geolocator = Nominatim()
    location = geolocator.geocode(loc)
    return (location.latitude, location.longitude)


def get_geo_position_ArcGIS(loc):
    locator = ArcGIS(timeout=10)
    place = locator.geocode(loc)
    return (place.latitude, place.longitude)


def get_geo_position_google(loc):
    g = geocoder.google(loc, key="AIzaSyDgqFxZfFvhh8ponaUqskqn2bWwn9B7lM8")
    return g.latlng


def get_geo_position(loc):
    # try:
    #     res = get_geo_position_geolocator(loc)
    # except:
    #     res = get_geo_position_google(loc)
    # if res == None:
    #     res = get_geo_position_google(loc)
    # return res
    return get_geo_position_ArcGIS(loc)