import base64
import binascii
import imghdr
import mimetypes
import uuid

from PIL import Image as PILImage
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile, File
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from bitsoframework.middleware import get_request
from bitsoframework.utils import files

EMPTY_VALUES = (None, '', [], (), {})
DEFAULT_CONTENT_TYPE = "application/octet-stream"
ALLOWED_IMAGE_TYPES = (
    "jpe",
    "jpeg",
    "jpg",
    "png",
    "gif"
)


def download(url):
    file_path = files.download(url)

    return File(file=open(file_path, 'rb'), name=file_path)


def get_uid(media):
    return "%s:%s" % (media.type, urlsafe_base64_encode(force_bytes(media.id)))


def get_files(request=None):
    request = request or get_request()

    files = []

    for key in request.FILES.keys():

        for file in request.FILES.getlist(key):
            files.append(file)

    return files


def is_image(file):
    try:
        image = PILImage.open(file)
        image.verify()
        # image.close()
        return True
    except:
        return False


class Base64:
    """
    Utility used to parse a base64 into a temporary file
    """

    @classmethod
    def get_file(cls, base64_data):
        """
        convert the given base64 data to a file and file extension

        :param base64_data:
        :return:
        """

        # Check if this is a base64 string
        if base64_data in EMPTY_VALUES:
            return None, None

        if isinstance(base64_data, str):
            # Strip base64 header.
            if ';base64,' in base64_data:
                header, base64_data = base64_data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error):
                raise ValidationError(_("Please upload a valid image."))

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.

            # Get the file name extension:
            file_extension = Base64.get_file_extension(file_name, decoded_file, header.replace("data:", ""))

            if file_extension not in ALLOWED_IMAGE_TYPES:
                raise ValidationError(_("The type of the image couldn't been determined."))

            complete_file_name = file_name + "." + file_extension

            data = ContentFile(decoded_file, name=complete_file_name)

            return data, file_extension

        raise ValidationError(_('This is not an base64 string'))

    @classmethod
    def get_file_extension(cls, filename, decoded_file, content_type):

        extension = imghdr.what(filename, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        if extension is None and content_type:
            extension = mimetypes.guess_extension(content_type)
            if extension:
                extension = extension.replace(".", "")

        return extension
