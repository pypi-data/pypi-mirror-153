from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field, FloatField


class CoordinatesField(Field):
    latitude = FloatField()
    longitude = FloatField()

    def to_internal_value(self, data):

        if data is not None:
            if not isinstance(data, dict):
                raise ValidationError("Expecting {latitude:..., longitude:...} but got %s" % (str(data),))

            latitude = data.get("latitude")
            longitude = data.get("longitude")

            latitude = self.latitude.to_internal_value(latitude)
            longitude = self.longitude.to_internal_value(longitude)

            from django.contrib.gis.geos.point import Point

            return Point(x=longitude,
                         y=latitude)

    def to_representation(self, instance):
        if instance:
            return {
                "longitude": instance.x,
                "latitude": instance.y
            }
