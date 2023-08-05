from bitsoframework.utils import files


def calculate(media):
    if hasattr(media, 'filename'):
        return files.get_content_type(media.filename)

    if media.origin_url:
        return files.get_remote_content_type(media.origin_url)

    return None


def get_file(media):
    if isinstance(media, str):
        return open(media, "rb")

    if hasattr(media, "get_file"):
        return media.get_file()

    if hasattr(media, "file"):
        return media.file

    return None
