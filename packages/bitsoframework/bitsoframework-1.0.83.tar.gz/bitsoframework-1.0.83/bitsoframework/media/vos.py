from bitsoframework.utils.models import set_attrs, get_choice_label
from bitsoframework.vos import AbstractVO


class Media(AbstractVO):
    """
    Value Object that represents a set of uploaded documents and images to a
    parent record.
    """

    categories = None
    """
    Required grouping categories.
    """

    def load(self, entries):
        """
        Load from a single collection of images and documents into this vo.
        """

        map = {}

        for entry in entries:

            name = get_choice_label(self.categories, entry.category)

            values = map.get(name, None)

            if not values:
                map[name] = values = list()

            values.append(entry)

        # index them
        for key, value in map.items():
            map[key] = sorted(value, key=lambda entry: entry.index, reverse=True)

        set_attrs(self, map)

        return self
