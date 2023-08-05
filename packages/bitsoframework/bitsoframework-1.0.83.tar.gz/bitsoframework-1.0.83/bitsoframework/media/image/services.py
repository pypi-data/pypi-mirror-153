from bitsoframework.media.image.models import THUMBNAIL_ENABLED
from bitsoframework.media.services import MediaService
from bitsoframework.media.settings import Image


class ImageService(MediaService):
    """
    Service used to manage the lifecycle of the Image model.
    """

    model_class = Image

    def filter(self, **kwargs):
        queryset = super(ImageService, self).filter(**kwargs)

        if THUMBNAIL_ENABLED:
            queryset = queryset.select_related("thumbnails_source").prefetch_related("thumbnails_source__thumbnails")

        return queryset
