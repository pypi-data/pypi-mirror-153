from bitsoframework.vos import AbstractVO


class MetadataModel(AbstractVO):

    def __init__(self, attributes=None, **kwargs):
        super(MetadataModel, self).__init__(**kwargs)
        self.attributes = attributes or []


class MetadataAttribute(AbstractVO):
    pass
