import folium
import random
import countries
import film_parser
import geoloc
import os
import re


def add_marker(group, coords, name):
    """
    (FeatureGroup, [latitude, longitude], str) -> None

    Function adds folium marker to folium.FeatureGroup() or folium.Map()
    """
    color_list = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
                  'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
                  'darkpurple', 'pink', 'lightblue', 'lightgreen',
                  'gray', 'black', 'lightgray']
    folium.Marker(
        location=coords,
        popup=name,
        icon=folium.Icon(color=random.choice(color_list), icon='film')
    ).add_to(group)


def add_countries(group, countries_list):
    """
    (FeatureGroup, [latitude, longitude], str) -> None

    Function adds geojson polygon to folium.FeatureGroup() or folium.Map()
    """
    def style(x):
        return {'fillColor': ('#%06X' % random.randint(0, 256**3 - 1))}
    for element in countries_list:
        folium.GeoJson(
            "countries\\" + element + ".geo.json", style_function=style
        ).add_to(group)


def get_geo():
    """
    (None) -> {coordinate (str): name of film (list)}

    Function return dictionary of films with coordinats as key and list
    of films filmed on this coordinates
    """
    dct = {}
    for i in range(int(film_number)):
        element = random.choice(films)
        loc = geoloc.get_geo_position_ArcGIS(element[1])
        if str(loc) in dct.keys():
            dct[str(loc)] = dct[str(loc)] + [element[0]]
        else:
            dct[str(loc)] = [element[0]]
        status = "Done" if loc else "Error"
        print("[" + str(i + 1) + "/" + str(film_number) + "] - " + status)
    return dct


def get_year(msg):
    """
    (str) -> str

    Function asks user to enter year with certain message.
    Function return string of year in case of correct input else asks again
    """
    year = input(msg)
    if re.match("[1-3][0-9]{3}", year) and len(year) == 4:
        return year
    else:
        print("Enter correct year!")
        return get_year(msg)


def get_film_number(msg, quantity):
    """
    (str) -> str

    Function asks user to enter number of films with certain message.
    Function return string of quantity in case of correct input else
    asks again
    """
    number = input(msg)
    if number.isdigit() and int(number) <= quantity:
        return number
    else:
        print("Enter correct number!")
        return get_film_number(msg, quantity)


def create_map(dct):
    """
    (dict) -> None

    Function creates map with markers and country borders
    """
    f_map = folium.Map()
    fg = folium.FeatureGroup(name="Film Markers")
    for loc, film in dct.items():
        if loc != "None":
            add_marker(fg, eval(loc), ("<br> ".join(
                list(set(film)))).replace("'", "`"))
    fg.add_to(f_map)

    # Write EU countries
    fg = folium.FeatureGroup(name="Eropean Union Countries")
    add_countries(fg, countries.EU_countries)
    fg.add_to(f_map)

    # Write NATO countries
    fg = folium.FeatureGroup(name="NATO Countries")
    add_countries(fg, countries.NATO_countries)
    fg.add_to(f_map)

    folium.LayerControl().add_to(f_map)
    f_map.save('Map_2.html')


year = get_year("Enter year of filming: ")

films = film_parser.read_file("locations.list", year)
quantity = len(films)
print("[STATUS] Succesfully parsed file")
print("        ", quantity, "films was found")

film_number = get_film_number(
    "Due to API limitation enter number of markers on map: ", quantity)

print("[STATUS] Searching for geolocation")
geo = get_geo()

print("[STATUS] Writing map")
create_map(geo)
print("[STATUS] Done!")

os.system("Map_2.html")
