import math
import random as pr

EMPTY = ""
"""
The empty String <code>""</code>.
"""

INDEX_NOT_FOUND = -1
"""
Represents a failed index search.
"""


def to_string(value, encoding="utf-8"):
    if isinstance(value, bytes):
        return value.decode(encoding)

    if isinstance(value, str):
        return value

    if value is None:
        return value

    return str(value)


def is_empty(string):
    """
    Checks if a String is empty ("") or null.

    @param string: the String to check, may be null

    @return: true if the String is empty or null, false otherwise
    """

    return string is None or len(string) == 0


def tokenize_by_camel_case(string, token):
    """
    Tokenize the given String by camel case replacing upper case characters by
    the given token.
    """

    if not string:
        return string

    result = [string[0:1]]

    index = 1
    length = len(string)

    while index < length:

        character = string[index].upper()

        if character != " " and character == string[index]:

            result.append(token);
            result.append(string[index].lower())

        else:

            result.append(string[index])

        index += 1

    return "".join(result)


def uncapitalize(string):
    """
    UN-Capitalize the first character of the given String
    """

    return string[0].lower() + string[1:]


def contains_ignore_case(string, searchStr):
    """
    <p>
    Checks if String contains a search String irrespective of case, handling
    <code>null</code>. Case-insensitivity is defined as by
    {@link String#equalsIgnoreCase(String)}.

    <p>
    A <code>null</code> String will return <code>false</code>.
    </p>

    @param string
               the String to check, may be null
    @param searchStr
               the String to find, may be null
    @return true if the String contains the search String irrespective of
             case or false if not or <code>null</code> string input
    """

    if (string is None) or (searchStr is None):
        return False

    return string.lower().__contains__(searchStr.lower())


def substring_between(string, before, after):
    """
    <p>
    Gets the String that is nested in between two  Only the first
    match is returned.
    </p>

    <p>
    A <code>null</code> input String returns <code>null</code>. A
    <code>null</code> before/after returns <code>null</code> (no match). An
    empty ("") before and after returns an empty string.
    </p>

    @param string
               the String containing the substring, may be null
    @param before
               the String before the substring, may be null
    @param after
               the String after the substring, may be null
    @return the substring, <code>null</code> if no match
    """

    if (string is None) or (before is None) or (after is None):
        return None

    start = string.find(before);

    if start != INDEX_NOT_FOUND:

        end = string.find(after, start + len(before))

        if end != INDEX_NOT_FOUND:
            return string[start + len(before):end]

    return None


def substring_after(string, delimiter):
    """
    <p>
    Gets the substring after the first occurrence of a delimiter. The
    delimiter is not returned.
    </p>

    <p>
    A <code>null</code> string input will return <code>null</code>. An empty
    ("") string input will return the empty string. A <code>null</code>
    delimiter will return the empty string if the input string is not
    <code>null</code>.
    </p>

    <p>
    If nothing is found, the empty string is returned.
    </p>

    @param string
               the String to get a substring from, may be null
    @param delimiter
               the String to search for, may be null
    @return the substring after the first occurrence of the delimiter, null
            if null String input
    """

    if is_empty(string):
        return string

    if delimiter is None:
        return EMPTY

    pos = string.find(delimiter)

    if pos == INDEX_NOT_FOUND:
        return EMPTY

    return string[pos + delimiter.length()]


def substring_before(string, delimiter):
    """
      <p>
      Gets the substring before the first occurrence of a delimiter. The delimiter
      is not returned.
      </p>

      <p>
      A <code>null</code> string input will return <code>null</code>. An empty
      (Strings.EMPTY) string input will return the empty string. A <code>null</code>
      delimiter will return the empty string if the input string is not
      <code>null</code>.
      </p>

      <p>
      If nothing is found, the empty string is returned.
      </p>

      @param string
                 the String to get a substring from, may be null
      @param delimiter
                 the String to search for, may be null
      @return the substring before the first occurrence of the delimiter,
              null if null String input
    :param str:
    :param delimiter:
    :return:
    """

    if is_empty(string):
        string

    if delimiter is None:
        return EMPTY

    pos = string.find(delimiter)

    if pos == INDEX_NOT_FOUND:
        return EMPTY

    return string[0:pos]


def substring_before_last(string, delimiter):
    """
    Gets the substring before the last occurrence of a separator. The
    separator is not returned.
    </p>

    <p>
    A <code>null</code> string input will return <code>null</code>. An empty
    ("") string input will return the empty string. An empty or
    <code>null</code> separator will return the input string.
    </p>

    <p>
    If nothing is found, the string input is returned.
    </p>

    @param string
               the String to get a substring from, may be null
    @param delimiter
               the String to search for, may be null
    @return the substring after the first occurrence of the delimiter, null
            if null String input
    """

    if is_empty(string):
        return string

    if delimiter is None:
        return EMPTY

    pos = string.rfind(delimiter)

    if pos == INDEX_NOT_FOUND:
        return EMPTY

    return string[0:pos]


def split_by_length(value, length, add_suffix=False, suffix_template=" (%i/%i)"):
    """
    Split the given string into an array of substrings at a maximum length.

    :param value:
    :param length:
    :param suffix:
    :return: split array of strings
    """

    max_length = len(value)

    chunks = range(0, int(math.ceil(max_length / length)))
    chunk_size = len(chunks)
    result = []

    for chunk in chunks:
        start = chunk * length
        end = min(max_length, (chunk + 1) * length)
        substring = value[start:end]

        if add_suffix and chunk_size > 1:
            suffix = suffix_template % (chunk + 1, chunk_size)
            substring += suffix

        result.append(substring)

    return result


def random(length=7, validator=None, combination='abcdefghijklmnpqrstuvwxyz0123456789'):
    while True:

        random_id = ''.join(pr.choice(combination) for _ in range(length))

        if not validator or validator(random_id):
            return random_id


class StringBuffer(object):

    def __init__(self, source=None):

        if isinstance(source, (str,)):
            self.source = [source]
        else:
            self.source = source or []

    @property
    def length(self):

        length = 0

        for item in self.source:
            length += len(item)

        return length

    def append(self, value):

        if value:
            self.source.append(value)

    def __str__(self):

        return "".join(self.source)
