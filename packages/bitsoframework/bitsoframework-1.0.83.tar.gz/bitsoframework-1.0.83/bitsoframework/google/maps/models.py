from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models import Model


class AbstractAddress(Model):
    address = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=250, db_index=True, null=True, blank=True)
    state = models.CharField(max_length=250, db_index=True, null=True, blank=True)
    country = models.CharField(max_length=250, db_index=True, null=True, blank=True)
    postal_code = models.CharField(max_length=7, null=True, blank=True)

    full_address = models.CharField(max_length=1200, null=True, blank=True)

    coordinates = PointField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.full_address or self.get_address()

    def get_address(self):
        if self.address and self.city and self.state and self.country and self.postal_code:
            return "%s, %s, %s %s, %s" % (self.address, self.city, self.state, self.postal_code, self.country)

        return None
