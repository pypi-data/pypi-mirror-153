from bitsoframework.utils.models import get_model_class, get_field, exists, diff_list


class Differ(object):

    def __init__(self, record):
        self.model_class = get_model_class(record)
        self.new_record = record
        self.old_record = self.model_class.objects.get(pk=record.pk) if exists(record) else None

    def compare(self, properties):

        result = {}

        for name in properties:
            field = get_field(self.model_class, name) or getattr(self.model_class, name)
            new_value = getattr(self.new_record, name)
            old_value = getattr(self.old_record or self.new_record, name)

            if new_value and new_value.__class__.name == "RelatedManager":

                old_value = list(getattr(self.old_record, name).all()) if self.old_record else []
                new_value = list(new_value.all())

                result[name] = {
                    "old_value": old_value,
                    "new_value": new_value,
                    **diff_list(old_value, new_value)
                }

            elif new_value != old_value:

                result[name] = {
                    "old_value": old_value,
                    "new_value": new_value
                }

        return result
