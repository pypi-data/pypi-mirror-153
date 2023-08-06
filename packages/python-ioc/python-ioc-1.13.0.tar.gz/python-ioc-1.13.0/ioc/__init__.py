import collections
import contextlib
import glob
import inspect
import itertools
import functools
import typing

from ioc import provider
from ioc import schema
from ioc.requirement import DeclaredRequirement
from ioc.requirement import NOT_PROVIDED
from ioc.requirement import NO_DEFAULT
from ioc.exc import UnsatisfiedDependency
from ioc.exc import MissingDependencies
from ioc.pkg import setup
from ioc.pkg import teardown
from ioc.provider import get_unsatisfied_dependencies
from . import etc


__version__ = '1.3.11'


__all__ = [
    'inject',
    'is_satisfied',
    'provide',
    'require',
    'setup',
    'teardown',
]


def require(names, *args, **kwargs):
    req = provider.get_requirement(names)
    if req is not None:
        return req

    return DeclaredRequirement(provider, names, *args, **kwargs)


def provide(
    name: str,
    value: object,
    force: bool = False,
    tags: list = None
) -> object:
    """Register Python object `value` as a dependency under the key `name` and
    return the object.

    The `force` argument indicates if any existing dependency under `name`
    must be overwrriten. If `force` is ``False``, an exception is raised if
    `name` is already provided.
    """
    provider.register(name, value, force=force, tags=tags)
    return value


def retire(name):
    return provider.retire(name)


def override(name, value):
    return provide(name, value, force=True)


def load(dependencies, override=False, using: typing.Optional[provider.Provider] = None):
    p = using or provider
    s = schema.Parser(provider=p, override=override).load(dependencies)
    s.resolve(schema.Resolver(p))


def load_config(
    filenames: list = ['etc/ioc.conf', 'etc/ioc.conf.d/*'],
    override: bool = True,
    using: typing.Optional[provider.Provider] = None
):
    """Configure dependencies from the given configuration files. The
    `filenames` parameter is a list of string containing the files to read
    the dependency configuration from, in the specified order.

    The `override` parameter indicates if existing dependencies must be
    overridden (instead of raising an error on observation on the first
    duplicate). If `override` is ``False`` and the files specified by the
    `filename` parameter contain duplicate dependency declarations, then the
    invocation will always fail.
    """
    if isinstance(filenames, str):
        filenames = [filenames]
    for filepath in itertools.chain(*[glob.glob(x) for x in filenames]):
        load(etc.read(filepath), override=override, using=using)


def is_satisfied(name: str) -> bool:
    """Return a boolean indicating if the dependency specified by `name`
    is satisfied.
    """
    return provider.is_satisfied(name)


def tagged(tag):
    return provider.tagged(tag)


class class_property(object):

    def __init__(self, name, factory=None, default=NO_DEFAULT):
        self.name = name
        self.factory = factory or (lambda x: x)
        self.dep = require(name, default=default)
        self.default = default

    def __get__(self, obj, objtype):
        if self.dep._injected is NOT_PROVIDED:
            self.dep._setup()
        return self.factory(self.dep)


def context(name: str, injected: object):
    """Like :func:`inject`, but determine if the :term:`Dependency` is a
    context-manager. In that case, run the decorated function within a
    context (e.g. using ``with`` or ``async with``).
    """
    return _inject.context(name, injected)


def inject(*args, **kwargs):
    """Ensures that `injected` is made available under
    `name`.

    If the decorated object is a *function*, then `injected` is appended to the
    function signature e.g.:

    .. code:: python

        import ioc

        ioc.provide('ExampleDependency', 'This is injected into the signature.')

        @ioc.inject('dep', 'ExampleDependency')
        def f(a, b, dep):
            return a, b, dep

    The function `f()` may then be invoked by providing the `a` and `b`
    arguments; the `dep` argument is injected by the framework.

    For decorated classes, this implies that the decorator
    sets an attribute `name` on the class with a
    :class:`class_property` instance pointing to `injected`.
    """
    kwargs.setdefault('scope', 'process')
    if len(args) > 1:
        return _inject(*args, **kwargs)

    # The first argument is a function where each parameter that is annotated
    # with a string value is considered to refer to an injected dependency.
    func = args[0]
    sig = inspect.signature(func)
    for param in sig.parameters.values():
        if not isinstance(param.annotation, str):
            continue
        func = _inject(param.name, param.annotation)(func)
    return func


class _inject:

    @classmethod
    def context(cls, name, injected):
        """Shortcut to inject a contextual dependency in the function call
        scope.
        """
        return cls(name, injected, scope='function')

    def __init__(self, name, injected, scope='process'):
        self.attname = name
        self.injected = injected
        self.scope = scope

    def __call__(self, obj):
        if inspect.isclass(obj):
            d = self._decorate_class(obj)
        elif inspect.iscoroutinefunction(obj):
            d = self._decorate_coroutinefunction(obj)
        elif inspect.isfunction(obj):
            d = self._decorate_function(obj)
        else:
            raise ValueError("Can only decorate classes and functions atm.")
        return d

    def _decorate_class(self, obj):
        setattr(obj, self.attname, class_property(self.injected))
        return obj

    def _decorate_function(self, obj):
        @functools.wraps(obj)
        def f(*args, **kwargs):
            kwargs[self.attname] = require(self.injected)
            return obj(*args, **kwargs)
        self._update_signature(f)
        return f

    def _decorate_coroutinefunction(self, obj):
        @functools.wraps(obj)
        async def f(*args, **kwargs):
            dep = require(self.injected)
            if hasattr(dep, 'as_context'):
                dep = dep.as_context()
            async with _ensure_async_context(dep, self.scope) as ctx:
                kwargs[self.attname] = ctx
                return await obj(*args, **kwargs)
        self._update_signature(f)
        return f

    def _update_signature(self, f):
        sig = inspect.signature(f)
        parameters = collections.OrderedDict(
            [
                (n, p) for n, p in list(sig.parameters.items())
                if n != self.attname

            ]
        )
        f.__annotations__ = collections.OrderedDict(
            [(n, p.annotation)
            for n, p in list(parameters.items()) if p.annotation]
        )
        f.__signature__ = sig.replace(parameters=list(parameters.values()))


@contextlib.asynccontextmanager
async def _ensure_async_context(dep, scope):
    if scope != 'function':
        yield dep
    else:
        is_context_manager = hasattr(dep, '__aenter__')
        try:
            yield (await dep.__aenter__()) if is_context_manager else dep
        except Exception as e:
            if is_context_manager:
                await dep.__aexit__(type(e), e, None)
            raise
        else:
            if is_context_manager:
                await dep.__aexit__(None, None, None)


def call(name, *args, **kwargs):
    """Invoke the dependency identified by `name` with
    the given positional and keyword arguments.
    """
    return require(name)(*args, **kwargs)


def check():
    """Inspect the provider and raise an exception if there are missing
    dependencies.
    """
    missing = get_unsatisfied_dependencies()
    if missing:
        raise MissingDependencies(missing)
