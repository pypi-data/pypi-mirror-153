import os

import googlemaps

from utils import timex
from utils.cache import cache

CACHE_NAME, CACHE_TIMEOUT = 'GoogleMaps', timex.SECONDS_IN.YEAR


def get_api_key():
    return os.environ['GOOGLE_API_KEY']


class GoogleMaps:
    def __init__(self):
        gmaps_api_key = get_api_key()
        self.api = googlemaps.Client(key=gmaps_api_key)

    def __get_geocode__(self, address):
        @cache(CACHE_NAME, CACHE_TIMEOUT)
        def get_geocode_inner(address):
            return self.api.geocode(address)
        return get_geocode_inner(address)

    def __get_reverse_geocode__(self, latlng):
        @cache(CACHE_NAME, CACHE_TIMEOUT)
        def get_reverse_geocode_inner(latlng):
            return self.api.reverse_geocode(latlng)
        return get_reverse_geocode_inner(latlng)

    def get_latlng(self, address):
        geocode = self.__get_geocode__(address)
        location = geocode[0]['geometry']['location']
        return [location['lat'], location['lng']]

    def get_address(self, latlng):
        rev_geocode = self.__get_reverse_geocode__(latlng)
        return rev_geocode[0]['formatted_address']
