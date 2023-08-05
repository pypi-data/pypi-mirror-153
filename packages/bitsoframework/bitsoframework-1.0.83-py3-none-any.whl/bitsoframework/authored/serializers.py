from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import Serializer

from bitsoframework.middleware import get_user


class UserNameSerializer(Serializer):
    """
    Serializer used to expose minimum information about the user (first name,
    last name and id).
    """

    id = IntegerField()

    first_name = CharField()

    last_name = CharField()


class AuthoredSerializer(Serializer):
    def validate(self, value):
        value = super(AuthoredSerializer, self).validate(value)

        if not self.instance:
            value["created_by"] = get_user()

        value["modified_by"] = get_user()

        return value
