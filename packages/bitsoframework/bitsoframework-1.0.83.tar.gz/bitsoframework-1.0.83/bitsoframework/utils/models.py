from bitsoframework.utils import lists


def get_data(model, excluded=[]):
    data = {}

    for fld in model._meta.fields:
        if len(excluded) > 0 and excluded.__contains__(fld.name):
            continue

        data[fld.name] = getattr(model, fld.name)

    return data


def new_instance(model_class, **kwargs):
    data = {}

    for fld in model_class._meta.fields:
        if fld.name not in kwargs:
            continue

        data[fld.name] = kwargs.get(fld.name)

    model = model_class(**data)

    return model


def clone(model):
    new_kwargs = get_data(model, excluded=[model._meta.pk])

    return get_model_class(model)(**new_kwargs)


def get_model_class(model):
    return model.__class__


def get_field(clazz, name):
    for field in clazz._meta.fields:
        if field.name == name:
            return field

    return None


def set_attrs(object, __map=None, __allow_null=True, **kwargs):
    if not __map:
        __map = kwargs
    else:
        kwargs.update(__map)

    for key, value in __map.items():

        if not __allow_null and value is None:
            continue

        setattr(object, key, value)

    return object


def get_choice_label(choices, choice):
    for entry in choices:

        if entry[0] == choice:
            return entry[1]

    return ""


def get_choice_id(tuples, str_value):
    if str_value:
        s = str_value.lower()
        for t in tuples:
            if t[1].lower() == s:
                return t[0]
    return None


def exists(record):
    clazz = get_model_class(record)
    pk = get_field(clazz, 'id')

    if pk.auto_created:
        return record.pk is not None

    return clazz.objects.filter(pk=record.pk).exists()


def diff_list(old_value, new_value):
    old_value = lists.as_list(old_value)
    new_value = lists.as_list(new_value)

    added = []
    removed = []

    for item in new_value:
        if item not in old_value:
            added.append(item)

    for item in old_value:
        if item not in new_value:
            removed.append(new_value)

    return {
        "added": added,
        "removed": removed
    }
