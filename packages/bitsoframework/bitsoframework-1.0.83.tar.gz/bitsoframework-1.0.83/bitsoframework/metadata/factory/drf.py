from bitsoframework.metadata.factory.base import AbstractModelFactory


class MetadataModelSerializerFactory(AbstractModelFactory):

    serializers = None

    def get_model(self, app_label, model_name):
        pass
