from bitsoframework.media.filterset import get_filterset_base
from bitsoframework.utils.reflection import require
from django.contrib import admin as django_admin


class MediaRegistry(object):
    defaults = {
        "document": {
            "serializer": "bitsoframework.media.document.serializers.DocumentSerializer",
            "service": "bitsoframework.media.document.services.DocumentService",
            "admin": "bitsoframework.media.document.admin.DocumentAdmin"
        },
        "cloud-document": {
            "serializer": "bitsoframework.media.cloud_document.serializers.CloudDocumentSerializer",
            "service": "bitsoframework.media.cloud_document.services.CloudDocumentService",
            "admin": "bitsoframework.media.cloud_document.admin.CloudDocumentAdmin"
        },
        "image": {
            "serializer": "bitsoframework.media.image.serializers.ImageSerializer",
            "service": "bitsoframework.media.image.services.ImageService",
            "admin": "bitsoframework.media.image.admin.ImageAdmin"
        }
    }

    def __init__(self, storage=[]):
        self.storage = {}

        for entry in storage:
            self.add(**entry)

    @property
    def media_types(self):
        return self.storage.keys()

    def add(self, model, serializer=None, service=None, admin=None, filterset=None, **kwargs):
        model = require(model)

        default = self.defaults.get(model.type, {})

        serializer = serializer or default.get("serializer")
        service = service or default.get("service")
        admin = admin or default.get("admin")
        filterset = filterset or default.get("filterset")

        # if model and admin:
        #    django_admin.site.register(model, admin)

        self.storage[model.type] = {
            "model": model,
            "serializer": serializer,
            "service": service,
            "admin": admin,
            "filterset": filterset,
            **kwargs
        }

    def get_model(self, media_type):
        return self.storage.get(media_type, {}).get("model")

    def get_admin(self, media_type):
        entry = self.storage.get(media_type, {})
        admin = entry.get("admin")

        if isinstance(admin, str):
            admin = require(admin)
            entry["admin"] = admin

        return admin

    def get_serializer(self, media_type):
        entry = self.storage.get(media_type, {})
        serializer = entry.get("serializer")

        if isinstance(serializer, str):
            serializer = require(serializer)
            entry["serializer"] = serializer

        return serializer

    def get_filterset(self, media_type):
        entry = self.storage.get(media_type, {})
        filterset = entry.get("filterset")

        if isinstance(filterset, str):
            filterset = require(filterset)
            entry["filterset"] = filterset

        elif not filterset:
            filterset = get_filterset_base(self.get_model(media_type))
            entry["filterset"] = filterset

        return filterset

    def get_service(self, media_type):
        entry = self.storage.get(media_type, {})
        service = entry.get("service")

        if isinstance(service, str):
            service = require(service)
            entry["service"] = service

        return service

    def register_admin(self, site):
        for media_type in self.storage.keys():
            model = self.get_model(media_type)
            admin = self.get_admin(media_type)
            if admin:
                site.register(model, admin)
