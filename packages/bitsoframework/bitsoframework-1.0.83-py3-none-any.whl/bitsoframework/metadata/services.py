from django.apps import apps

from bitsoframework.metadata.models import MetadataModel


class MetadataModelService(object):

    def __init__(self):
        self.models = {}

    def get_model(self, app_label, model_name):
        name = "%s.%s" % (app_label, model_name)
        if name not in self.models:
            self.models[name] = self.build_model(app_label, model_name)

        return self.models.get(name)

    def build_model(self, app_label, model_name):
        django_model = apps.get_model(app_label, model_name)
        model = MetadataModel(name=model_name)

        return model
