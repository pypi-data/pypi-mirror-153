import json

from bitsoframework.utils.reflection import require

from bitsoframework.notifications import settings
from bitsoframework.notifications.models import DeviceNotification


class NotificationService(object):
    enabled = settings.NOTIFICATION_ENABLED
    debug = settings.NOTIFICATION_DEBUG

    def __init__(self):
        self.engines = {}

    def get_engine(self, service):
        if service not in self.engines:
            class_name = settings.NOTIFICATION_SERVICES.get(service)
            factory = require(class_name)

            self.engines[service] = factory()

        return self.engines.get(service)

    def push(self, device, recipient, title, description=None, data=None, **kwargs):
        notification = DeviceNotification(device=device,
                                          recipient=recipient,
                                          sender=device.user,
                                          title=title,
                                          description=description,
                                          data=data or {})

        if self.debug:
            print("Pushing notification: " + str(notification))

        if self.enabled:

            engine = self.get_engine(device.service)

            engine.send(notification, **kwargs)

        elif self.debug:
            print("NotificationService is currently disabled.")
            print("To enable, make sure to set BITSO_NOTIFICATION_ENABLE='yes' on your .env file.")

        notification.save()

        return notification
