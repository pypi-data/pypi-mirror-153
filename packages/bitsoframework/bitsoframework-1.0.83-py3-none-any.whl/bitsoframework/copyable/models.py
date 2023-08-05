from django.db.models.base import Model

from bitsoframework.utils.models import set_attrs


class CopyableModel(Model):
    class Meta:
        abstract = True

    def copy(self, auto_save=True, **kwargs):
        pk = self.pk

        copy = self.__class__.objects.get(id=pk)
        copy.pk = None
        copy.id = None

        set_attrs(self, kwargs)

        if auto_save:
            copy.save(force_insert=True)

        return copy
