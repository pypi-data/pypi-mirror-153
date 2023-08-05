def require(name):
    if isinstance(name, str):
        index = name.rfind(".")
        module_name = name[0:index]
        member_name = name[index + 1:len(name)]
        module = __import__(module_name, globals(), locals(), [member_name])

        return getattr(module, member_name)

    return name


def exists(name):
    try:
        return require(name) is not None
    except:
        return False
