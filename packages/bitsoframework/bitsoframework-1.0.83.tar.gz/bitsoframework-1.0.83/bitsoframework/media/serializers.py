from bitsoframework.media.utils import Base64, download

from rest_framework import fields
from rest_framework.fields import CharField
from rest_framework.serializers import Serializer, ModelSerializer

from bitsoframework.media.settings import registry
from bitsoframework.media.utils import Base64, download
from bitsoframework.taggable.mixins import TaggableSerializer


class AbstractMediaSerializer(ModelSerializer):
    uid = fields.ReadOnlyField()

    urls = fields.DictField(read_only=True)

    type = fields.CharField(required=False)

    category = fields.ReadOnlyField()

    # created_by = UserNameSerializer(read_only=True)
    # modified_by = UserNameSerializer(read_only=True)
    created_by = fields.ReadOnlyField()
    modified_by = fields.ReadOnlyField()

    created = fields.ReadOnlyField()
    modified = fields.ReadOnlyField()


class AbstractFileMediaSerializer(AbstractMediaSerializer):
    """
    Serializer for bitso.media.models.Document or bitso.media.models.Image
    """

    extension = fields.ReadOnlyField()

    filesize = fields.ReadOnlyField()

    filename = fields.ReadOnlyField()

    thumbnails_filesize = fields.ReadOnlyField()

    base64 = fields.CharField(write_only=True)
    source_Url = fields.CharField(write_only=True)

    def to_internal_value(self, data):
        base64 = data.pop("base64", None)
        source_url = data.pop("base64", None)
        result = super(AbstractFileMediaSerializer, self).to_internal_value(data)
        if base64:
            file, extension = Base64.get_file(base64)
            result["file"] = file
        if source_url:
            file = download(source_url)
            result["file"] = file

        return result


class MediaMetadataSerializer(TaggableSerializer):
    title = CharField(max_length=255, required=False)
    description = CharField(required=False)


class MediaSerializer(Serializer):
    """
    Helper serializer that emulates support for polymorphic data serialization
    for multiple different types of media model classes.
    """

    def to_representation(self, item):
        serializer_class = registry.get_serializer(item.type)
        serializer = serializer_class()

        return serializer.to_representation(item)


class DictionaryMediaSerializer(Serializer):
    """
    Serializer that renders a list of documents as dictionary where each 
    document's name is a key in the rendered map.
    """

    many = True

    serializer_class = MediaSerializer

    def __init__(self, keys=None, other_key="other", **kwargs):

        super(DictionaryMediaSerializer, self).__init__(**kwargs)

        self.other_key = other_key
        self.keys = keys

    def to_representation(self, items):
        """
        Object instance -> Dict of primitive datatypes.
        """
        map = {}

        other = []

        if self.keys:

            map[self.other_key] = other

            for key in self.keys:
                map[key] = None

        serializer = self.serializer_class()

        for item in items:

            value = serializer.to_representation(item)

            if self.keys:

                if item.name in self.keys:

                    map[item.name] = value

                else:

                    other.append(value)
            else:

                map[item.name] = value

        return map
