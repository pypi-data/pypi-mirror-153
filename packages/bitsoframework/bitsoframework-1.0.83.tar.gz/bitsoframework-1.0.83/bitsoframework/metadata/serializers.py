from rest_framework.fields import CharField
from rest_framework.serializers import Serializer


class MetadataAttributeSerializer(Serializer):
    name = CharField()
    type = CharField()


class MetadataModelSerializer(Serializer):
    name = CharField()
    attributes = MetadataAttributeSerializer(many=True)
