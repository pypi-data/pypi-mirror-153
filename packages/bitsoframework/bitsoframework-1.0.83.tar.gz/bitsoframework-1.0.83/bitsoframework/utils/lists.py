def as_list(value):
    if not isinstance(value, list):
        return list(value)

    return value


def add_all(array, other):
    """
    Append all items of the second array into the first one.

    :param array:
    :param other:
    :return:
    """

    for item in other:
        array.append(item)

    return array


def remove_all(array, other):
    """
    Remove all items of the second array into the first one.

    :param array:
    :param other:
    :return:
    """
    for item in other:
        array.remove(item)

    return array


def contains(array, *args):
    """
    Check rather the given array contains at least one of the given items
    :param array:
    :param args:
    :return: true if at least one item exists, false otherwise
    """

    for arg in args:

        if array.__contains__(arg):
            return True

    return False


def unique(array):
    """
    Remove any duplicate items from the given array
    :param array:
    :param args:
    :return: true if at least one item exists, false otherwise
    """

    indexed = set()
    return [x for x in array if x not in indexed and (indexed.add(x) or True)]


def copy(entries):
    result = list()

    for entry in entries:
        result.append(entry)

    return result


def to_list(entries):
    if isinstance(entries, list):
        return entries

    values = list()

    if isinstance(entries, tuple):

        for entry in entries:
            values.append(entry)
    else:
        values.append(entries)

    return values


def flatten(*args):
    result = []

    for items in args:
        for item in items:
            result.append(item)

    return result
