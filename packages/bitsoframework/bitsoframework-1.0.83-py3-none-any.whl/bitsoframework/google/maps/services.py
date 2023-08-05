import tempfile

import googlemaps
from django.conf import settings
from django.utils.functional import cached_property


class GoogleMapService(object):

    def __init__(self, client_id=None, api_key=None):

        super(GoogleMapService, self).__init__()

        self._client = None
        self.client_id = client_id or getattr(settings, "GOOGLE_MAPS_CLIENT_ID", None)
        self.client_api_key = api_key or getattr(settings, "GOOGLE_MAPS_API_KEY", None)

    @cached_property
    def client(self):
        return googlemaps.Client(self.client_api_key,
                                 client_id=self.client_id)

    def update_coordinates(self, record):

        coordinates = self.get_coordinates(record)

        if record.coordinates != coordinates:
            record.coordinates = coordinates
            return True

        return False

    def get_address_query(self, record):

        if record:
            return record.get_address()

        return None

    def get_place_photo(self, *args, **kwargs):

        local_filename = tempfile.mktemp()

        f = open(local_filename, 'wb')

        for chunk in self.client.places_photo(*args, **kwargs):
            if chunk:
                f.write(chunk)
        f.close()

        return local_filename

    def get_directions(self, origin, destination):

        directions = self.client.directions(mode="driving", origin={
            "latitude": origin.y,
            "longitude": origin.x
        }, destination={
            "latitude": destination.y,
            "longitude": destination.x
        })

        return directions

    def get_coordinates(self, address):

        query = self.get_address_query(address)

        if query:
            geocode = self.client.geocode(query)
            if geocode and len(geocode) > 0:
                location = geocode[0]["geometry"]["location"]
                from django.contrib.gis.geos.point import Point
                return Point(x=location.get("lng"),
                             y=location.get("lat"))

        return None
