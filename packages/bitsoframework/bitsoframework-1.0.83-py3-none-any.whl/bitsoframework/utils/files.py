import tempfile
import os
from datetime import datetime
from uuid import uuid4

import mimetypes

"""
File utilities and tricks

@author: bitsoframework

@since: 07/25/2014
"""


def save(path, content):
    f = open(path, "w")
    f.write(content)
    f.close()


def list(directory, include_files=True, include_directories=False, recursive=False):
    """
    Build up a list with files and directories under the given directory or
    according to the given filter parameterized in this method call.

    @return: list of files
    """
    files = list()

    for filename in os.listdir(directory):

        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):

            if include_files:
                files.append(file_path)

        elif os.path.isdir(file_path):

            if include_directories:
                files.append(file_path)

            if recursive:

                for f in list(filename, include_files, include_directories, recursive):
                    files.add(f)

    return files


def delete_file(file_path):
    return os.remove(file_path)


def read_base64(file_path):
    return read(file_path).encode("base64")


def read(file_path):
    f = open(file_path, 'rb')
    s = f.read()
    f.close()
    return s


def get_remote_content_type(url):
    from urllib.request import urlopen
    try:
        res = urlopen(url)
        http_message = res.info()
        return http_message.get_content_type()
    except:
        if url and url.startswith("http"):
            return "text/html"

        return None


def get_content_type(filename):
    return mimetypes.MimeTypes().guess_type(filename)[0]


def download(url, output=None, debug=False):
    """
    Download and save a file specified by url to output file. If not provided,
    creates a temp file instead.
    """
    from urllib.request import urlopen

    u = urlopen(url)

    if not output:
        output = tempfile.mktemp()

    with open(output, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if debug and meta_length:
            file_size = int(meta_length[0])
            print("Downloading: {0} Bytes: {1}".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            if debug:
                status = "{0:16}".format(file_size_dl)
                if file_size:
                    status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
                status += chr(13)

                print(status),
                print()

    return output


def get_extension(file_path):
    """
    Utility used to extract the extension of a given file path.

    :param file_path:
    :return:
    """
    name, extension = os.path.splitext(file_path)

    return extension[1:].lower()


def get_filename(filename):
    """
    Utility used to extract the extension of a given file path.

    :param filename:
    :return:
    """
    name, extension = os.path.splitext(filename)

    return name


def get_random_name(name):
    """
    Generate a random name for the given file name preserving the original file's
    name extension

    @param name the file name

    @return a random file name
    """

    ext = os.path.splitext(name)[1]

    return uuid4().__str__() + ext


def get_last_modified(filename):
    """
    Retrieve a datetime instance of when the given file was last modified
    :param filename:
    """
    stat = os.stat(filename)
    return datetime.fromtimestamp(stat.st_mtime)


def set_last_modified(filename, modified):
    """
    Set a datetime attribute within the given filename
    :param filename:
    """
    stat = os.stat(filename)
    os.utime(filename, times=(stat.st_atime, modified.timestamp()))
