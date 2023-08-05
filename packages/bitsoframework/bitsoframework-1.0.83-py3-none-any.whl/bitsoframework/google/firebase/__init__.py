import os

import firebase_admin
from django.conf import settings
from firebase_admin import credentials

cred_file = getattr(settings, 'BITSO_FIREBASE_CREDENTIALS',
                    os.path.join(settings.BASE_DIR, "keys/firebase.json"))
cred = credentials.Certificate(cred_file)
app = firebase_admin.initialize_app(cred)
