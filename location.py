import requests
from geopy.geocoders import Nominatim


def get_location(city_name):
    url = "https://ru.wikipedia.org/w/api.php?action=query&prop=coordinates&format=json&titles={}"
    data = requests.get(url.format(city_name)).json()
    resp = data["query"]['pages']
    key = next(iter(resp))
    lat, lon = resp[key]['coordinates'][0]['lat'], resp[key]['coordinates'][0]['lon']

    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.reverse(f"{lat},{lon}")

    return location.raw['address']['state']

