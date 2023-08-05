from django.db import models
from django.db.models.base import Model

from bitsoframework.media.image.services import ImageService


class MyProduct(Model):
    name = models.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)

        self.images = ImageService(parent=self, category=0)
        self.defects = ImageService(parent=self, category=1)
