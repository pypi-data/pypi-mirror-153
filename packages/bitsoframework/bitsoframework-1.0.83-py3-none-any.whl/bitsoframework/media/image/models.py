from django.conf import settings
from django.db import models
from django.db.models import SET_NULL
from django.db.models.fields.files import ImageFieldFile
from django.utils.functional import cached_property
from easy_thumbnails.files import ThumbnailFile

from bitsoframework.media.models import MEDIA_PATH_RESOLVER, AbstractFileMedia
from bitsoframework.utils.reflection import exists

THUMBNAIL_ENABLED = getattr(settings, "BITSO_IMAGE_THUMBNAIL_ENABLED", exists("easy_thumbnails.models.Source"))
THUMBNAIL_SOURCE_MODEL = getattr(settings, "BITSO_IMAGE_THUMBNAIL_SOURCE", "easy_thumbnails.Source")


class AbstractImage(AbstractFileMedia):
    """
    Model used to map an image uploaded/attached to another model in the system.

    @since: 06/17/2014 20:30:00

    @author: bitsoframework
    """

    type = "image"
    """
    The unique type of document among the various registered document types.
    """

    file = models.ImageField('The image itself', upload_to=MEDIA_PATH_RESOLVER, width_field="width",
                             height_field="height", max_length=500)
    """
    The image itself
    """

    if THUMBNAIL_ENABLED:
        thumbnails_source = models.OneToOneField(THUMBNAIL_SOURCE_MODEL, null=True, blank=True, on_delete=SET_NULL,
                                                 related_name="image")
        """
        The easy_thumbnail source for this file so we can encapsulate all of its thumbnails into a single db reference.
        """

    thumbnails_filesize = models.IntegerField(null=True, blank=True)
    """
    The number of bytes for all the generated thumbnails.
    """

    width = models.FloatField(null=True, blank=True)
    """
    The width (in pixels) for the image
    """

    height = models.FloatField(null=True, blank=True)
    """
    The height (in pixels) for the image
    """

    class Meta:
        abstract = True

    @cached_property
    def thumbnail_aliases(self):

        data = getattr(settings, "THUMBNAIL_ALIASES", {})

        aliases = []

        for value in data.values():

            for name in value.keys():
                aliases.append(name)

        return aliases

    @cached_property
    def thumbnails(self):
        from easy_thumbnails.files import get_thumbnailer
        from easy_thumbnails.alias import aliases

        data = {}
        thumbnails = list(self.thumbnails_source.thumbnails.all()) if self.thumbnails_source else []
        thumbnailer = get_thumbnailer(self.file)

        if len(thumbnails) != len(aliases.all()):
            self.generate_thumbnails()
            thumbnails = list(self.thumbnails_source.thumbnails.all())

        for thumbnail in thumbnails:
            for alias in aliases.all():

                options = aliases.get(alias, target=thumbnailer.alias_target)
                thumbnail_options = thumbnailer.get_options(options)
                thumbnail_options["HIGH_RESOLUTION"] = False

                names = [
                    thumbnailer.get_thumbnail_name(thumbnail_options, transparent=False)
                ]
                transparent_name = thumbnailer.get_thumbnail_name(thumbnail_options, transparent=True)
                if transparent_name not in names:
                    names.append(transparent_name)

                for name in names:
                    if thumbnail.name == name:
                        data[alias] = ThumbnailFile(
                            name=name, storage=thumbnailer.thumbnail_storage,
                            thumbnail_options=thumbnail_options)
                        break

        return data

    def thumbnail_by_alias(self, alias):
        return self.thumbnails.get(alias)

    @property
    def urls(self):

        urls = {
            "original": self.url
        }

        if THUMBNAIL_ENABLED:
            for alias, thumbnail in self.thumbnails.items():
                urls[alias] = thumbnail.url

        return urls

    def on_update_file(self):

        if THUMBNAIL_ENABLED:
            self.thumbnails_source = None

        super(AbstractImage, self).on_update_file()

    def delete_file(self, _file):

        self.thumbnails_filesize = None

        if isinstance(_file, ImageFieldFile) and _file.name:

            self.storage.delete(_file.name)

        elif isinstance(_file, str):

            self.storage.delete(_file)

        try:
            from easy_thumbnails.files import get_thumbnailer

            thumbnailer = get_thumbnailer(_file)
            thumbnailer.delete_thumbnails()

        except ImportError:
            pass

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        creating = not self.id

        super(AbstractImage, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                        update_fields=update_fields)

        if creating and THUMBNAIL_ENABLED:
            self.generate_thumbnails()

    def generate_thumbnails(self):

        from easy_thumbnails.templatetags import thumbnail
        from easy_thumbnails.models import Source
        aliases = getattr(settings, "THUMBNAIL_ALIASES", {})

        for value in aliases.values():

            for name in value.keys():
                thumbnail.thumbnail_url(self.file, name)

        if not self.thumbnails_source:
            self.thumbnails_source = Source.objects.get_file(self.storage, self.file.name)
            self.save(update_fields=['thumbnails_source'])

    def copy(self, **kwargs):

        if THUMBNAIL_ENABLED:
            kwargs["thumbnails_source"] = None

        copy = super(AbstractImage, self).copy(**kwargs)

        return copy

    def resolve_path(self, filename, resolver):

        if hasattr(self, "preview_source") and self.preview_source:
            return resolver(self.preview_source, "preview/" + filename, allow_override=False)

        return super(AbstractImage, self).resolve_path(filename, resolver)
