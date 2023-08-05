from django.conf import settings
from firebase_admin import messaging

from bitsoframework.notifications.models import DeviceNotification


class FirebasePushNotificationService(object):

    def send(self, notification: DeviceNotification, **kwargs):
        message = messaging.Message(
            token=notification.device.token, data=notification.data,
            notification=messaging.Notification(title=notification.title,
                                                body=notification.description)
        )

        return messaging.send(message, **kwargs)


class FirebaseWebPushNotificationService(object):

    def __init__(self, icon=None):
        self.icon = icon or getattr(settings, "BITSO_NOTIFICATION_FIREBASE_WEB_PUSH_ICON", None)

    def send(self, notification: DeviceNotification, **kwargs):
        message = messaging.Message(
            token=notification.device.token,
            webpush=messaging.WebpushConfig(
                notification=messaging.WebpushNotification(
                    title=notification.title,
                    body=notification.description,
                    icon=self.icon
                )
            )
        )

        return messaging.send(message, **kwargs)
