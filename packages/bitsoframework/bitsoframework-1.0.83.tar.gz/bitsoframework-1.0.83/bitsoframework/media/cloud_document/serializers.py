from bitsoframework.media.serializers import AbstractMediaSerializer
from bitsoframework.media.settings import CloudDocument


class CloudDocumentSerializer(AbstractMediaSerializer):
    class Meta:
        model = CloudDocument
        exclude = ["parent_type", "parent_id"]
