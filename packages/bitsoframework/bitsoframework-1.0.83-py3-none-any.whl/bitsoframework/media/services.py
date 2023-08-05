from django.contrib.contenttypes.models import ContentType

from bitsoframework.media import utils
from bitsoframework.utils.models import set_attrs, new_instance


class MediaService(object):
    """
    Service used to manage the lifecycle of the media models.
    """

    category = 0
    """
    The category in which the image is saved against
    """

    model_class = None
    """
    The underlying model class being managed by this service.
    """

    parent_class = None
    """
    The parent related class we are contributing to.
    """

    parent = None
    """
    The parent model related to the maintained images
    """

    def __init__(self, category=0, parent=None, parent_class=None, **kwargs):

        super(MediaService, self).__init__(**kwargs)

        self.category = category
        self.parent = parent
        self.parent_class = parent_class

        if not self.parent_class and self.parent:
            self.parent_class = self.parent.__class__

    def __iter__(self):
        return self.filter().__iter__()

    def get_parent_type(self):

        if not hasattr(self, "_parent_type"):
            self._parent_type = ContentType.objects.get_for_model(self.parent_class)

        return self._parent_type

    def delete(self, **kwargs):

        self.filter(**kwargs).delete()

    def all(self):
        return self.filter()

    def filter(self, **kwargs):

        if self.category:
            kwargs["category"] = self.category

        if self.parent_class:
            kwargs["parent_type"] = self.get_parent_type()

        if self.parent and self.parent.id:
            kwargs["parent_id"] = self.parent.id

        return self.model_class.objects.filter(**kwargs).indexed()  # .select_related("created_by", "modified_by")F

    def download_and_create(self, origin_url, origin_id=None, category=None, **kwargs):

        file = utils.download(origin_url)

        return self.create(file=file, origin_url=origin_url, origin_id=origin_id, category=category, **kwargs)

    def create(self, category=None, auto_save=True, **kwargs):

        model = new_instance(self.model_class,
                             category=category or self.category,
                             **kwargs)

        if self.parent_class:
            model.parent_type = self.get_parent_type()

        if self.parent and self.parent.id:
            model.parent_id = self.parent.id

        if auto_save:
            model.save()

        return model

    def update(self, model, auto_save=True, **kwargs):

        if kwargs.get("tags"):
            model.tags.set(*kwargs.pop("tags"), clear=True)

        set_attrs(model, kwargs)

        if auto_save:
            model.save()

        return model
