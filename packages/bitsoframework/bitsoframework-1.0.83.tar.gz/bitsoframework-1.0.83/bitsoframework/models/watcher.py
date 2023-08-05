class ModelPropertyWatcher(object):
    """
    Component responsible for extracting changes off of model instances.
    """

    def __init__(self, include_diff=True, **kwargs):

        self.include_diff = include_diff
        self.properties = kwargs

    def __call__(self, diff):

        for name, handler in self.properties.items():

            old_value = None
            new_value = None

            if name in diff.added():

                new_value = getattr(diff.current, name)

            elif name in diff.removed():

                old_value = getattr(diff.previous, name)

            elif name in diff.changed():

                old_value = getattr(diff.previous, name)
                new_value = getattr(diff.current, name)

            if old_value != new_value:

                if self.include_diff:

                    handler(diff=diff, old_value=old_value, new_value=new_value)

                else:

                    handler(old_value=old_value, new_value=new_value)
