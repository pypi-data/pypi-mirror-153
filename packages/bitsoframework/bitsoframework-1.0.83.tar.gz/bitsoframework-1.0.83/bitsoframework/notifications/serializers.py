from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from bitsoframework.notifications.models import Device


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        exclude = ('user',)
