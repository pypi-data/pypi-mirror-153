def get_full_name(user=None, first_name=None, last_name=None):
    if user:
        first_name = user.first_name
        last_name = user.last_name

    if first_name and last_name:
        return first_name + " " + last_name

    if last_name:
        return last_name

    return first_name


def get_first_and_last_name(full_name):
    if not full_name:
        return "", ""

    names = full_name.split(" ")

    length = len(names)

    first_name = names[0]
    last_name = " ".join(names[1:length]) if length > 1 else ""

    return first_name, last_name
