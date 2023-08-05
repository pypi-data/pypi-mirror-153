from bitsoframework.media.image.serializers import ImageSerializer
from bitsoframework.media.serializers import AbstractFileMediaSerializer
from bitsoframework.media.settings import Document, PREVIEW_ENABLED


class DocumentSerializer(AbstractFileMediaSerializer):
    if PREVIEW_ENABLED:
        preview = ImageSerializer(read_only=True)

    class Meta:
        model = Document
        exclude = ["parent_type", "parent_id", "file"]
