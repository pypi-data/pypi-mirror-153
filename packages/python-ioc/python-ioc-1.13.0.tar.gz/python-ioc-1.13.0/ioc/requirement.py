import copy
import operator

import six

from ioc.exc import UnsatisfiedDependency

NOT_PROVIDED = object()
NO_DEFAULT = object()


def new_method_proxy(func):
    def inner(self, *args):
        if self._injected is NOT_PROVIDED:
            self._setup()
        value = self._injected
        return func(value, *args)
    return inner


class DeclaredRequirement(object):
    """Represents a requirement declared by a consumer module."""
    _provider = None
    _injected = NOT_PROVIDED
    _names = None

    def __init__(self, provider, names, default=NO_DEFAULT):
        self._injected = NOT_PROVIDED
        self._provider = provider
        self._names = names
        self._default = default
        if isinstance(names, six.string_types):
            self._names = [names]
        self._provider.add_listener(
            self._names,
            lambda k, v: setattr(self, '_injected', NOT_PROVIDED)
        )
        provider.require(self._names, self)

    __getattr__ = new_method_proxy(getattr)


    def __setattr__(self, name, value):
        if name in ("_injected","_provider","_names","_default"):
            # Assign to __dict__ to avoid infinite __setattr__ loops.
            self.__dict__[name] = value
        else:
            if self._injected is NOT_PROVIDED:
                self._setup()
            setattr(self._injected, name, value)

    def __delattr__(self, name):
        if name in ("_injected","_provider","_names","_default"):
            raise TypeError("can't delete %s." % name)
        if self._injected is NOT_PROVIDED:
            self._setup()
        delattr(self._injected, name)

    def __call__(self, *args, **kwargs):
        if self._injected is NOT_PROVIDED: # pragma: no cover
            self._setup()
        return self._injected(*args, **kwargs) # pragma: no cover

    def _setup(self):
        try:
            self._injected = self._provider.resolve(self._names[0])
        except UnsatisfiedDependency:
            if self._default is NO_DEFAULT:
                raise
            self._injected = self._default

    def __instancecheck__(self, instance):
        if self._injected is NOT_PROVIDED:
            self._setup()
        return isinstance(instance, type(self._injected))

    def __reduce__(self):
        raise NotImplementedError

    def __getstate__(self):
        raise NotImplementedError

    if six.PY3:
        __bytes__ = new_method_proxy(bytes)
        __str__ = new_method_proxy(str)
        __bool__ = new_method_proxy(bool)
    elif six.PY2:
        __str__ = new_method_proxy(str)
        __unicode__ = new_method_proxy(unicode)
        __nonzero__ = new_method_proxy(bool)

    __copy__ = new_method_proxy(copy.copy)
    __deepcopy__ = new_method_proxy(copy.deepcopy)
    __repr__ = new_method_proxy(repr)
    __int__ = new_method_proxy(int)
    __float__ = new_method_proxy(float)
    __dir__ = new_method_proxy(dir)
    __complex__ = new_method_proxy(complex)
    __round__ = new_method_proxy(round)
    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)
    __getitem__ = new_method_proxy(operator.getitem)
    __setitem__ = new_method_proxy(operator.setitem)
    __delitem__ = new_method_proxy(operator.delitem)
    __iter__ = new_method_proxy(iter)
    __len__ = new_method_proxy(len)
    __contains__ = new_method_proxy(operator.contains)
