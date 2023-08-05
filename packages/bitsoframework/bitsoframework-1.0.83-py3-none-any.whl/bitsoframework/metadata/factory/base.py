from bitsoframework.metadata.models import MetadataModel


class AbstractModelFactory(object):

    def get_model(self, app_label, model_name):
        model = MetadataModel(app_label=app_label,
                              model_name=model_name)

        model.attributes = self.__build_attributes(model)

        return model

    def __build_attributes(self, model):
        return []
