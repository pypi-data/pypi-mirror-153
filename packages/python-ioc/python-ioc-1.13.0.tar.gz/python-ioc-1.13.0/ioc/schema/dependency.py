from ioc.schema.iresolvable import IResolvable


class Dependency(IResolvable):
    """Represents a dependency declared in the configuration
    file.
    """

    @property
    def key(self):
        return self.name

    def __init__(self, visibility='public', tags=None, mode=None, **kwargs):
        self.visibility = visibility
        self.tags = tags or []
        self.mode = mode or None
        self.append_existing = self.mode == 'declare'

    def requires(self):
        """Return a list containing all the requirements of this
        dependency. Only applicable to ``NestedDependency`` instances.
        """
        raise NotImplementedError


class SimpleDependency(Dependency):

    def __init__(self, name, value, invoke=False, args=None, kwargs=None, **params):
        self.name = name
        self.value = value
        self.invoke = invoke or bool(args or kwargs)
        self.args = args or []
        self.kwargs = kwargs or {}
        Dependency.__init__(self, **params)

    def requires_invocation(self):
        return self.invoke

    def is_symbol(self):
        return True


class LiteralDependency(Dependency):

    def __init__(self, name, value, **kwargs):
        Dependency.__init__(self, **kwargs)
        self.name = name
        self.value = value

    def is_literal(self):
        return True


class NestedDependency(Dependency):

    def __init__(self, name, factory, args=None, kwargs=None, chain=None, **params):
        self.name = name
        self.factory = factory
        self.args = args or []
        self.kwargs = kwargs or {}
        self.chain = chain or []
        Dependency.__init__(self, **params)

    def has_factory(self):
        return True

    def is_injected(self):
        return True

    def requires(self):
        return ([self.factory.value] if self.factory.is_injected() else [])\
            + [x.value for x in self.args if x.is_injected()]\
            + [x.value for x in self.kwargs.values() if x.is_injected()]\
            + [x.value for x in self.chain if x.is_injected()]


class DependencyCollection(Dependency):

    def __init__(self, name, members, **kwargs):
        Dependency.__init__(self, **kwargs)
        self.name = name
        self.members = members

    def is_collection(self):
        return True
