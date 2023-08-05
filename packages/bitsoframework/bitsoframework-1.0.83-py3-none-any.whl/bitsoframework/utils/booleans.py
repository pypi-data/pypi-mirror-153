def to_boolean(value, default_value):
    if value is None:
        return default_value

    if isinstance(value, (str,)):
        return value == "true"

    return default_value
