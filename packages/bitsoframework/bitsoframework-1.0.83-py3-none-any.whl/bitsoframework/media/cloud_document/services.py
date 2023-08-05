from bitsoframework.media.services import MediaService
from bitsoframework.media.settings import CloudDocument


class CloudDocumentService(MediaService):
    """
    Service used to manage the lifecycle of the Cloud document model.
    """

    model_class = CloudDocument
