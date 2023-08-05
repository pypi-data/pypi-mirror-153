from rest_framework import fields

from bitsoframework.media.serializers import AbstractFileMediaSerializer
from bitsoframework.media.settings import Image


class ImageSerializer(AbstractFileMediaSerializer):

    class Meta:
        model = Image
        exclude = ["parent_type", "parent_id", "file"]
