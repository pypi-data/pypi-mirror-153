import hashlib
from django.core.files.base import File


def calculate_md5(media):
    return calculate(media, "md5")


def calculate_sha1(media):
    return calculate(media, "sha1")


def calculate_sha224(media):
    return calculate(media, "sha224")


def calculate_sha256(media):
    return calculate(media, "sha256")


def calculate_sha384(media):
    return calculate(media, "sha384")


def calculate_sha512(media):
    return calculate(media, "sha512")


def calculate(media, type):
    file = get_file(media)

    if file:
        hash = getattr(hashlib, type)()

        content = file.read()

        hash.update(content)

        digest = hash.hexdigest()

        return digest

    return None


def get_file(media):
    if isinstance(media, File):
        return media

    if isinstance(media, str):
        return open(media, "rb")

    if hasattr(media, "get_file"):
        return media.get_file()

    if hasattr(media, "file"):
        return media.file

    return None
