import json
from random import randint
import urllib.request
class random_city:
    cities = None
    def __init__(self) -> None:
        urllib.request.HTTPHandler(debuglevel=1)
        cities_file = urllib.request.urlopen('https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json').read()
        self.cities = json.loads(cities_file)
        pass
    def get_city(self):
        idx =  randint(0, len(self.cities))
        city = self.cities[idx]
        return {
            "name":city['name'],
            "country":city['country'],
            "lat":city['lat'],
            "lng":city['lng']
        }