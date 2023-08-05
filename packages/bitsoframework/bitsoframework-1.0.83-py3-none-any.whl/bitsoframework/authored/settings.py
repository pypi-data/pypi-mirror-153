from django.conf import settings
from django.db.models import CASCADE

AUTH_USER_MODEL = settings.AUTH_USER_MODEL
ON_DELETE = getattr(settings, 'BITSO_AUTHORED_ON_DELETE', CASCADE)
