from django_extensions.db.models import ActivatorModel
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from bitsoframework.notifications.models import Device
from bitsoframework.notifications.serializers import DeviceSerializer


class DeviceViewMixin(object):
    shared_devices = False

    @action(methods=["GET"], detail=False, url_path="devices")
    def list_devices(self, request):
        """
        Attach a new photo to the underlying record.
        """

        queryset = request.user.devices.active()

        serializer = DeviceSerializer(instance=queryset, many=True)

        return Response(serializer.data)

    @action(methods=["POST"], detail=False, url_path="devices/unregister")
    def unregister_device(self, request):
        """
        Unregister a device for the currently logged within the given token so it no longer
        receives push notifications.
        """

        token = request.data.get("token")

        instance = request.user.devices.filter(token=token).first()

        if instance:
            instance.status = ActivatorModel.INACTIVE_STATUS
            instance.save()

        return Response()

    @action(methods=["POST"], detail=False, url_path="devices/register")
    def register_device(self, request):
        """
        Register a device for the currently logged user either by creating or updating an existing one
        with the same token.
        """

        token = request.data.get("token")

        if not self.shared_devices:

            devices = Device.objects.filter(token=token,
                                            status=ActivatorModel.ACTIVE_STATUS).exclude(user=request.user)

            if devices.exists():
                devices.update(status=ActivatorModel.INACTIVE_STATUS)

        instance = request.user.devices.filter(token=token).first()

        if instance:

            serializer = DeviceSerializer(data=request.data, instance=instance, partial=True)
            serializer.is_valid(raise_exception=True)

            serializer.save(status=ActivatorModel.ACTIVE_STATUS)

            return Response(serializer.data, status=HTTP_200_OK)
        else:

            serializer = DeviceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save(user=request.user)

            return Response(serializer.data, status=HTTP_201_CREATED)
