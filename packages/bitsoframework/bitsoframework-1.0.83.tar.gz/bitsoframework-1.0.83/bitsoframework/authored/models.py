from .settings import ON_DELETE, AUTH_USER_MODEL
from django.db import models
from django.db.models import Model


class AuthoredModel(Model):
    """
    Model that tracks users who have craeted or last updated a record.

    Note that by itself, this model only holds the two properties but it does not
    automatically set them. You must use AuthoredSerializer in conjunction with
    your REST API or manually specify them instead.

    This model replaced CreatorModel in favor of decoupled logic.
    """

    class Meta:
        abstract = True

    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=ON_DELETE,
                                   related_name="%(app_label)s_%(class)s_created", null=True,
                                   blank=True)
    """
    Reference to the user who created this record.
    """

    modified_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=ON_DELETE,
                                    related_name="%(app_label)s_%(class)s_modified",
                                    null=True, blank=True)
    """
    Reference to the user who last updated this record.
    """
