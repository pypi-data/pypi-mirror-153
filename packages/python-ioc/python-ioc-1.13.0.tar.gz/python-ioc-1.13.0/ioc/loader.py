"""Declares functions to import dependencies."""
import importlib


BUILTINS = __builtins__


def import_module(qualname, fail_silent=False):
    """Import a Python module using its qualified name `qualname`."""
    try:
        return importlib.import_module(qualname)
    except ImportError:
        if not fail_silent:
            raise

        return None


def import_builtin(qualname, fail_silent=False):
    """Import a builtin type."""
    try:
        return BUILTINS[qualname]
    except KeyError:
        if not fail_silent:
            raise ImportError(qualname)

        return None


def call(qualname, *args, **kwargs):
    """Like :func:`~ioc.loader.import_symbol`, but invokes the symbol
    with the given positional and keyword arguments.
    """
    return import_symbol(qualname)(*args, **kwargs)


def import_symbol(qualname, fail_silent=False):
    """Import a symbol. The symbol may be one of the following and
    are considered in this order:

    -   A module;
    -   A class, function or variable in a module;
    -   A builtin type, or a member of a builtin type.
    """
    parts = qualname.rsplit('.', 1)
    if len(parts) == 1:
        result = import_module(parts[0], True) or import_builtin(parts[0], True)
        if result is None and not fail_silent:
            raise ImportError(qualname)

        return result

    namespace, name = parts
    if namespace.count('.') == 0: # Module or builtin type
        parent = import_symbol(namespace, True)
    else:
        parent = import_module(namespace, True)\
            or import_symbol(namespace, True)

    if parent is None and not fail_silent:
        raise ImportError(qualname)

    try:
        return getattr(parent, name)
    except AttributeError:
        if not fail_silent:
            raise ImportError(qualname)

        return None
