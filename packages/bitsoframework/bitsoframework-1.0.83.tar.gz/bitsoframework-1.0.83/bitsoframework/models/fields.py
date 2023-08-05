from django import forms
from django.db.models import Field, CharField
from django.db.models.signals import pre_save
from django.utils.translation import gettext as _

from bitsoframework.utils.strings import random


class RandomIDField(CharField):
    default_error_messages = {
        'invalid': _("'%(value)s' is not a valid ID."),
    }
    description = 'Unique identifier'
    empty_strings_allowed = False

    def __init__(self, verbose_name=None, **kwargs):
        if not "max_length" in kwargs:
            kwargs["max_length"] = 7
        kwargs["primary_key"] = True
        kwargs["default"] = self.generate_id
        super().__init__(verbose_name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_length']
        del kwargs['primary_key']
        del kwargs['default']
        return name, path, args, kwargs

    def validate_id(self, value):
        return not self.model.objects.filter(pk=value).exists()

    def generate_id(self):
        return random(self.max_length, self.validate_id)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        if not value:
            value = self.generate_id()
        return value

    def validate(self, value, model_instance):
        pass

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value

    def formfield(self, **kwargs):
        return None

    def contribute_to_class(self, cls, name, **kwargs):
        assert not cls._meta.auto_field, "Model %s can't have more than one RandomIDField." % cls._meta.label
        super().contribute_to_class(cls, name, **kwargs)
        cls._meta.auto_field = self

        def on_before_save(sender, **kwargs):
            instance = kwargs.get("instance")
            if instance and not getattr(instance, name):
                new_id = self.generate_id()
                setattr(name, new_id)

        pre_save.connect(on_before_save, sender=cls)

    def to_python(self, value):
        return value
