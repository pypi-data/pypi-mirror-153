from django.db import IntegrityError
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from rest_framework import serializers, fields
from rest_framework.exceptions import ValidationError

from bitsoframework.utils.models import set_attrs


class AnyField(fields.Field):

    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class ListIDSerializer(serializers.Serializer):
    ids = fields.ListField(child=AnyField(required=True))


class UpdateBulkListSerializer(serializers.ListSerializer):

    def update(self, instances, validated_data):

        writable_fields = []
        for index, attrs in enumerate(validated_data):
            instance = instances[index]
            set_attrs(instance, attrs)
            for key, value in attrs.items():
                setattr(instance, key, value)
                if key not in writable_fields:
                    writable_fields.append(key)
            # for field in self.child._writable_fields:
            # if field.field_name in attrs and field.field_name not in writable_fields:
            # writable_fields.append((field.field_name))

        if isinstance(instances[0], TimeStampedModel):
            writable_fields.append("modified")
            modified = timezone.now()
            for instance in instances:
                instance.modified = modified

        try:
            if getattr(self.child.Meta, "model_save", False):
                for instance in instances:
                    instance.save(update_fields=writable_fields)
            else:
                self.child.Meta.model.objects.bulk_update(instances, writable_fields)
        except IntegrityError as e:
            raise ValidationError(e)

        return instances
