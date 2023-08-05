import os

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import File
from django.db import models
from django.db.models import CASCADE
from django.db.models.fields.files import FieldFile
from django.utils.functional import cached_property
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel, ActivatorModel

from bitsoframework.authored.models import AuthoredModel
from bitsoframework.indexable.models import IndexedModel
from bitsoframework.media.utils import get_uid
from bitsoframework.utils import files
from bitsoframework.utils.files import get_random_name
from bitsoframework.utils.reflection import require

ON_DELETE = getattr(settings, 'BITSO_MEDIA_ON_DELETE', CASCADE)
MEDIA_CATEGORY_CHOICES = getattr(settings, "BITSO_MEDIA_CATEGORY_CHOICES", None)
MEDIA_PATH = getattr(settings, "BITSO_MEDIA_PATH", "uploads/documents")
MEDIA_PATH_RESOLVER_CLASS = require(getattr(settings, "BITSO_MEDIA_PATH_RESOLVER",
                                            "bitsoframework.media.path_resolvers.MediaPathResolver"))
MEDIA_PATH_RESOLVER = MEDIA_PATH_RESOLVER_CLASS(path=MEDIA_PATH)

DOCUMENT_MODEL_NAME = getattr(settings, "BITSO_MEDIA_DOCUMENT_MODEL_NAME", "media.Document")


class AbstractMedia(IndexedModel,
                    TitleDescriptionModel,
                    ActivatorModel,
                    TimeStampedModel,
                    AuthoredModel):
    """
    Abstract class common to document and image models.
    
    @since: 05/10/2016 19:50:00
    
    @author: bitsoframework
    """

    class Meta:
        abstract = True

    type = "undefined"
    """
    The type of media we are dealing with (overridden by every sub-class).
    """

    parent_id = models.CharField(db_index=True, max_length=200, null=True, blank=True)
    """
    The parent model's identifier.
    """

    parent_type = models.ForeignKey(ContentType, on_delete=ON_DELETE, null=True, blank=True, related_name="%(class)ss")
    """
    The type bound to this document
    """

    parent = GenericForeignKey('parent_type', 'parent_id')
    """
    The actual parent object storing this document.
    """

    category = models.IntegerField(db_index=True, null=True, blank=True, choices=MEDIA_CATEGORY_CHOICES)
    """
    The category used to group the image in the target model.
    """

    origin_url = models.URLField(null=True, blank=True, max_length=1000)
    """
    The URL from where this image was originally imported.
    """

    origin_id = models.CharField(null=True, blank=True, max_length=255, db_index=True)
    """
    An extra bit of information about the origin of this image.
    """

    author = models.CharField(null=True, blank=True, max_length=255, db_index=True)
    """
    The author name who created this document.
    """

    author_url = models.URLField(null=True, blank=True, max_length=255, db_index=True)
    """
    The website url of the person who created this document.
    """

    content_type = models.CharField(max_length=200, null=True, blank=True)
    """
    The type of content mapped by this file.
    """

    def __str__(self):
        return self.title

    @cached_property
    def uid(self):
        return get_uid(self)

    @cached_property
    def service(self):
        from .settings import registry

        service_class = registry.get_service(self.type)

        return service_class(self)

    @property
    def urls(self):
        return {
            "original": self.url
        }

    def calculate_content_type(self):
        from .settings import CONTENT_TYPE_CALCULATOR
        return CONTENT_TYPE_CALCULATOR(self)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.content_type:
            self.content_type = self.calculate_content_type()

        super(AbstractMedia, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                        update_fields=update_fields)


class AbstractFileMedia(AbstractMedia):
    filename = models.CharField(max_length=200, null=True, blank=True)
    """
    The original file name if needed to be used for anything
    """

    checksum = models.CharField(max_length=256, null=True, blank=True)
    """
    The original file's checksum
    """

    filesize = models.IntegerField(null=True, blank=True)
    """
    The number of bytes for the original file (size).
    """

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):

        super(AbstractFileMedia, self).__init__(*args, **kwargs)

        if self.pk:
            self.old_file = self.file if hasattr(self, "file") else None
        else:
            self.old_file = None

    @property
    def url(self):
        return self.file.url

    @property
    def extension(self):

        if self.filename:
            name, extension = os.path.splitext(self.filename)

            return extension[1:].lower()

        return None

    @cached_property
    def storage(self):
        return self._meta.get_field('file').storage

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.file != self.old_file and self.file and (update_fields is None or "file" in update_fields):
            self.on_update_file()

        return super(AbstractFileMedia, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                                   update_fields=update_fields)

    def on_update_file(self):

        self.filename = files.get_filename(self.get_file().name)
        self.filesize = self.get_file().size

        if not self.title:
            self.title = self.filename

        if self.old_file:
            # delete existing file so we can override it
            self.delete_file(self.old_file)

            #
            self.file.name = self.old_file.name
            self.checksum = None
            self.content_type = None

        self.file.name = get_random_name(self.filename)

        if not self.checksum:
            self.checksum = self.calculate_checksum()

        if not self.content_type:
            self.content_type = self.calculate_content_type()

    def get_file(self):

        if isinstance(self.file, FieldFile):
            return self.file.file

        return self.file

    def calculate_checksum(self):
        from .settings import CHECKSUM_CALCULATOR

        return CHECKSUM_CALCULATOR(self)

    def copy(self, **kwargs):

        new_file = File(self.file.storage.open(self.file.name))

        copy = super(AbstractFileMedia, self).copy(file=new_file, old_file=None, **kwargs)

        return copy

    def resolve_path(self, filename, resolver):
        """
        Method called finally resolve the location where this file should be stored.
        At first, the path is resolved by the framework over the bitso's MEDIA_PATH_RESOLVER settings
        but ultimately models have the ability to override this if necessary.

        For more info, see bitso.media.path_resolvers

        @return the resolved filepath for the given filename under this model. If nothing is returned
        then the logic is delegated up to the configured settings instead.
        """
        return None
