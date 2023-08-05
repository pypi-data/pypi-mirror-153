from django.conf import settings as django_settings
from django.db.models import fields, ForeignKey, CASCADE, SET_NULL
from django.utils.translation import gettext as _
from django_extensions.db.models import TitleDescriptionModel, TimeStampedModel, ActivatorModel
from jsonfield import JSONField

from bitsoframework.notifications import settings


class Device(TimeStampedModel, ActivatorModel):
    DEVICE_SERVICE_CHOICES = [(key, _(key)) for key in settings.NOTIFICATION_SERVICES.keys()]

    user = ForeignKey(django_settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="devices")
    service = fields.CharField(max_length=300, db_index=True, choices=DEVICE_SERVICE_CHOICES)
    manufacturer = fields.CharField(max_length=300, null=True, blank=True)
    model = fields.CharField(max_length=300, db_index=True, null=True, blank=True)
    platform = fields.CharField(max_length=300, db_index=True, null=True, blank=True)
    serial = fields.CharField(max_length=300, null=True, blank=True)
    token = fields.CharField(max_length=300, db_index=True, null=True, blank=True)
    uuid = fields.CharField(max_length=300, null=True, blank=True)
    version = fields.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = "bitso_device"

    def __str__(self):
        return "Device(id=%s, user=%s, service=%s, manufacturer=%s, model=%s, platform=%s, serial=%s, token=%s, uuid=%s, version=%s)" % \
               (str(self.id), str(self.user), str(self.service), str(self.manufacturer), str(self.model),
                str(self.platform), str(self.serial), str(self.token), str(self.uuid), str(self.version))


class DeviceNotification(TitleDescriptionModel, TimeStampedModel, ActivatorModel):
    recipient = ForeignKey(django_settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True,
                           related_name="device_notifications")
    sender = ForeignKey(django_settings.AUTH_USER_MODEL, on_delete=CASCADE, null=True,
                        related_name="sent_device_notifications")
    device = ForeignKey(Device, on_delete=SET_NULL, null=True, related_name="notifications")
    data = JSONField(null=True)

    class Meta:
        db_table = "bitso_device_notification"

    def __str__(self):
        return "DeviceNotification(id=%s, title=%s, description=%s, data=%s, recipient=%s, device=%s)" % \
               (str(self.id), str(self.title), str(self.description), str(self.data), str(self.recipient),
                str(self.device))
