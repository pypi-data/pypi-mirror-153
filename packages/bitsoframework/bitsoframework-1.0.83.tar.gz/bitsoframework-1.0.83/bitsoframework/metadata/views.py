from rest_framework.decorators import action
from rest_framework.response import Response

from bitsoframework.metadata.serializers import MetadataModelSerializer
from bitsoframework.metadata.services import MetadataModelService
from bitsoframework.mixins import AbstractViewSet


class MetadataModelViewSet(AbstractViewSet):
    serializer_class = MetadataModelSerializer

    def __init__(self, **kwargs):
        super(MetadataModelViewSet, self).__init__(**kwargs)
        self.service = MetadataModelService()

    def get(self):
        pass

    @action(detail=False, url_path="(?P<app_label>[-\w]+)/(?P<model_name>[-\w]+)")
    def get_by_name(self, request, app_label, model_name):
        instance = self.service.get_model(app_label, model_name)

        serializer = self.get_serializer(instance=instance)

        return Response(serializer.data)
