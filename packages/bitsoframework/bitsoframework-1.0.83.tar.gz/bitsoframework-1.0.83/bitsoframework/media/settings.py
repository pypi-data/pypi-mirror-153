from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from bitsoframework.media.registry import MediaRegistry
from bitsoframework.utils.reflection import require

registry = MediaRegistry(getattr(settings, "BITSO_MEDIA_REGISTRY", []))

Document = registry.get_model("document")
Image = registry.get_model("image")
CloudDocument = registry.get_model("cloud-document")

PREVIEW_ENABLED = getattr(settings, "BITSO_DOCUMENT_PREVIEW_ENABLED", True)

PREVIEW_WIDTH = getattr(settings, "BITSO_DOCUMENT_PREVIEW_WIDTH", 768)
PREVIEW_HEIGHT = getattr(settings, "BITSO_DOCUMENT_PREVIEW_HEIGHT", 1024)

AVOID_DUPLICATES = getattr(settings, "BITSO_MEDIA_AVOID_DUPLICATES", True)

CHECKSUM_CALCULATOR = require(
    getattr(settings, "BITSO_MEDIA_CHECKSUM_CALCULATOR", "bitsoframework.media.checksum.calculate_sha256"))

CONTENT_TYPE_CALCULATOR = require(
    getattr(settings, "BITSO_MEDIA_CONTENT_TYPE_CALCULATOR", "bitsoframework.media.content_type.calculate"))

if Image:
    @receiver(pre_delete, sender=Image)
    def on_delete_image(sender, instance, **kwargs):
        instance.delete_file(instance.file)

if Document:
    @receiver(pre_delete, sender=Document)
    def on_delete_document(sender, instance, **kwargs):
        instance.delete_file(instance.file)
