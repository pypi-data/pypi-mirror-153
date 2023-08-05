from django.db import models

from django.conf import settings
from bitsoframework.media.models import AbstractMedia

ORIGIN_TYPES = getattr(settings, "BITSO_MEDIA_CLOUD_DOCUMENT_ORIGIN_TYPES", {
    "google.com": {
        "document": "google/document",
        "spreadsheets": "google/spreadsheet",
        "presentation": "google/presentation"
    }
})


class AbstractCloudDocument(AbstractMedia):
    """
    Model used to map an online document residing on a external server. Note that sometimes the document
    may translate to a service rather than a file.

    @since: 12/29/2020 1:30:00

    @author: bitsoframework
    """

    type = "cloud-document"
    """
    The unique type of document among the various registered document types.
    """

    origin_type = models.CharField(null=True, blank=True, max_length=255, db_index=True)
    """
    The type of origin for this document, (google doc, google spreadsheet, google presentation, dropbox, etc.).
    """

    class Meta:
        abstract = True

    @property
    def url(self):
        return self.origin_url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.origin_type:
            self.origin_type = self.extract_origin_type(self.url)

        return super(AbstractCloudDocument, self).save(force_insert=force_insert, force_update=force_update,
                                                       using=using,
                                                       update_fields=update_fields)

    def extract_origin_type(self, url):

        if not url:
            return None

        for url_fragment, fragments in ORIGIN_TYPES.items():
            if url_fragment in url:
                for fragment, origin_type in fragments.items():
                    if fragment in url:
                        return origin_type
