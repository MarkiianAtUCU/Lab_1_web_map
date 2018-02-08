import folium
import random
from geopy.geocoders import Nominatim
import countries
import film_parser


def add_marker(group, coords, name):
    """
    (FeatureGroup, [latitude, longitude], str) -> None

    Function adds folium marker to folium.FeatureGroup() or folium.Map()
    """
    color = ('#%06X' % random.randint(0, 256**3 - 1))
    folium.Marker(
        location=coords,
        popup=name,
        icon=folium.Icon(color=color, icon='film')
    ).add_to(group)


def add_countries(group, countries_list):
    """
    (FeatureGroup, [latitude, longitude], str) -> None

    Function adds folium marker to folium.FeatureGroup() or folium.Map()
    """    
    def style(x):
        return {'fillColor': ('#%06X' % random.randint(0, 256**3 - 1))}
    for element in countries_list:
        folium.GeoJson(
            "countries\\" + element + ".geo.json", style_function=style
        ).add_to(group)


year = input("Enter year of filming: ")
films = film_parser.read_file("locations.list", year)
print("[STATUS] Succesfully parsed file")
print("        ", len(films), "films was found")
film_number = input("Due to API limitation enter number of markers on map: ")


print("[STATUS] Searching for geolocation")

dct = {}
for i in range(int(film_number)):
    element = random.choice(films)
    loc = film_parser.get_geo_position(element[1])
    if str(loc) in dct.keys():
        dct[str(loc)] = dct[str(loc)] + [element[0]]
    else:
        dct[str(loc)] = [element[0]]
    status = "Done" if loc else "Error"
    print("[" + str(i + 1) + "/" + str(film_number) + "] - " + status)


def create_map(dct):
    # print(dct, len(dct))
    f_map = folium.Map()
    fg = folium.FeatureGroup(name="Film Markers")
    for loc, film in dct.items():
        if loc != "None":
            add_marker(fg, eval(loc), ("<br> ".join(list(set(film)))).replace("'","`"))
    fg.add_to(f_map)

    fg = folium.FeatureGroup(name="Eropean Union Countries")
    add_countries(fg, countries.EU_countries)
    fg.add_to(f_map)

    fg = folium.FeatureGroup(name="NATO Countries")
    add_countries(fg, countries.NATO_countries)
    fg.add_to(f_map)

    folium.LayerControl().add_to(f_map)
    f_map.save('Map_2.html')
    print("Done!")


create_map(dct)
