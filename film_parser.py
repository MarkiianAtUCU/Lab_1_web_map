import geocoder
from geopy.geocoders import Nominatim


def get_name(year, line):
    return line[:line.find("(" + year)].strip().strip('"')


def get_filming_place(line, year_pos):
    bracket_pos = line.find("}")
    if bracket_pos != -1:
        place = line[bracket_pos + 1:].strip()
    else:
        place = line[line.find(")") + 1:].strip()

    if place[-1] == ")":
        r_line = place[::-1]
        place = r_line[r_line.find("(") + 1:][::-1].strip()
    return place


def get_geo_position_geolocator(loc):
    geolocator = Nominatim()
    location = geolocator.geocode(loc)
    return (location.latitude, location.longitude)


def get_geo_position_google(loc):
    g = geocoder.google(loc, key="AIzaSyDgqFxZfFvhh8ponaUqskqn2bWwn9B7lM8")
    return g.latlng


def get_geo_position(loc):
    try:
        res = get_geo_position_geolocator(loc)
    except:
        res = get_geo_position_google(loc)
    if res == None:
        res = get_geo_position_google(loc)
    return res


def read_file(path, year):
    """
    (str) -> (list)
    Return list of lines from file (path to file)
    [name, loc]
    """
    res = []
    with open(path, "r") as file:
        for i in range(14):
            file.readline()
        for i in file:
            position = i.find("(")
            if i[position + 1:position + 5] == year:
                name = get_name(year, i)
                place = get_filming_place(i, position)
                res.append((name, place))

    return res