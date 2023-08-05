from .serializers import TagListSerializerField, TaggitSerializer


class TaggableSerializer(TaggitSerializer):
    tags = TagListSerializerField(required=False)
