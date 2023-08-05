from django.conf import settings
from django.db import models
from django.db.models import SET_NULL
from django.db.models.fields.files import FieldFile

from bitsoframework.media.models import MEDIA_PATH_RESOLVER, AbstractFileMedia

IMAGE_MODEL_NAME = getattr(settings, "BITSO_MEDIA_DOCUMENT_MODEL_NAME", "media.Image")


class AbstractDocument(AbstractFileMedia):
    """
    Model used to map an image uploaded/attached to another model in the system.

    @since: 06/17/2016 20:30:00

    @author: bitsoframework
    """

    type = "document"
    """
    The unique type of document among the various registered document types.
    """

    file = models.FileField('The document itself', upload_to=MEDIA_PATH_RESOLVER, max_length=500)
    """
    The image itself
    """

    preview = models.OneToOneField(IMAGE_MODEL_NAME, on_delete=SET_NULL, null=True, blank=True,
                                   related_name="preview_source")
    """
    If preview tools are installed, this stores the reference of the image used to preview the document's content. 
    """

    class Meta:
        abstract = True

    def delete_file(self, _file):

        if isinstance(_file, FieldFile):

            self.storage.delete(_file.name)

        elif isinstance(_file, str):

            self.storage.delete(_file)
