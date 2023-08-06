import collections
import contextlib
import inspect


class MissingDependency(LookupError):

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def __str__(self):
        return "%s specifies dependency `%s` but its not provided by "\
            "the current context." % (repr(self.func), self.name)


class ArgumentDependencyInjector:
    """Resolves dependencies by inspecting the argument names
    in a function signature.
    """
    missing = object()
    MissingDependency = MissingDependency

    def __init__(self):
        self.reset()

    def call(self, func):
        """Call `func` and inject arguments based on its signature.

        Args:
            func (callable): the callable that specified dependencies
                in its signature.
        """
        args, kwargs = self.resolve(func)
        return func(*args, **kwargs)

    def reset(self):
        """Unregister all dependencies."""
        self.ctx = {'resolver': self}

    def provide(self, name, value):
        """Provide dependency `name` with `value`."""
        if name == 'injector':
            raise ValueError('`injector` is a reserved name.')
        self.ctx[name] = value

    def resolve(self, func):
        """Inspect the signature of callable `func` and return
        the positional arguments it requires based on the context.

        Args:
            func (callable): the callable that specified dependencies
                in its signature.

        Raises:
            MissingDependency: no dependency was registered for `name`.
        """
        args, *_ = inspect.getfullargspec(func)
        signature = inspect.signature(func)

        # For instance methods, ignore the self argument.
        if inspect.ismethod(func):
            args = args[1:]

        injected_args, injected_kwargs = [], {}
        for arg in args:
            default = signature.parameters[arg].default
            value = self.get(arg)
            if value == self.missing:
                if default == inspect.Parameter.empty:
                    raise self.MissingDependency(arg, func)
                value = default
            injected_args.append(value)

        return tuple(injected_args), injected_kwargs

    def get(self, name):
        """Return the dependency identified by name.

        Args:
            name (str): the name of the dependency.

        Returns:
            object
        """
        return self.ctx.get(name, self.missing)

    def add(self, resolvables):
        """Add one or many resolvables to the resolver."""
        if not isinstance(resolvables, collections.abc.Sequence):
            resolvables = [resolvables]
        for obj in resolvables:
            self.provide(obj.resolver_name, obj)

    def is_resolvable(self, obj):
        """Return a boolean indicating if `obj` is resolvable."""
        return isinstance(obj, Resolvable)

    def is_provided(self, name):
        """Return a boolean indicating if the dependency identified by
        string `name` is provided.
        """
        return name in self.ctx

    @contextlib.contextmanager
    def context(self, ctx):
        """Setup the context using `ctx` and tear it down after
        exiting.
        """
        for key, value in ctx.items():
            self.provide(key, value)
        try:
            yield
        finally:
            self.reset()


class Resolvable:
    """Mixin class that allows the resolver to detect an instance
    as resolvable and register it.
    """
    resolver_name = None
