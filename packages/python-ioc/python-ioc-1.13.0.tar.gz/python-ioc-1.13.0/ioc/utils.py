import keyword
import re

import six


def bytesequence(value, *args, **kwargs):
    return six.binary_type(value)\
        if six.PY2\
        else six.binary_type(value, *args, **kwargs)


def is_valid_identifier(name):
    """Return a boolean indicating if the given `name` is a
    valid path to a Python symbol.
    """
    is_valid = True
    for p in name.split('.'):
        is_valid &= not keyword.iskeyword(p)

        is_valid &= p.isidentifier() if six.PY3\
            else (re.match(r"^[^\d\W]\w*\Z", p) is not None)

    return is_valid
