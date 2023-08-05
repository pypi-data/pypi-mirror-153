from django.conf import settings

NOTIFICATION_SERVICES = getattr(settings, "BITSO_NOTIFICATION_SERVICES", {
    "firebase-push": "bitsoframework.notifications.services.firebase.FirebasePushNotificationService",
    "firebase-web-push": "bitsoframework.notifications.services.firebase.FirebaseWebPushNotificationService"
})

NOTIFICATION_ENABLED = getattr(settings, "BITSO_NOTIFICATION_ENABLED", False)
NOTIFICATION_DEBUG = getattr(settings, "BITSO_NOTIFICATION_DEBUG", False)
