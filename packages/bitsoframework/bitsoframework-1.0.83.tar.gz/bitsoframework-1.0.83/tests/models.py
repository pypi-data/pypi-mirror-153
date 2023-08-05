from bitsoframework.media.document.models import AbstractDocument
from bitsoframework.media.image.models import AbstractImage
from bitsoframework.media.cloud_document.models import AbstractCloudDocument


class Image(AbstractImage):
    pass


class Document(AbstractDocument):
    pass


class CloudDocument(AbstractCloudDocument):
    pass
