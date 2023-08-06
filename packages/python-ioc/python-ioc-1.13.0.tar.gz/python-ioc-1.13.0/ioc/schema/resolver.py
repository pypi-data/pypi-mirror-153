from ioc.loader import import_symbol
from ioc.exc import UnsatisfiedDependency
from ioc.provider import Provider
from ioc.collection import DependencyCollection


class SchemaResolver(object):
    """Resolves the dependencies declared in a schema."""

    def __init__(self, provider: Provider):
        self.provider = provider

    def resolve(self, dep):
        """Resolves a dependency `dep` and returns its declared Python
        object.
        """
        # If a string value on a dependency starts with a dollar-sign, it is
        # considered to be an environment variable.
        #if isinstance(getattr(dep, 'value', None), str) and dep.value.startswith('$'):

        #    # For security purposes, importing and instantiation symbols
        #    # from environment variables is not allowed.
        #    if dep.is_symbol():
        #        raise ConfigurationError("Can not use environment variable %s as symbol."
        #            % dep.value)

        #    varname = dep.value[1:]
        #    value = os.getenv(varname)
        #    if value is None:
        #        raise EnvironmentVariableNotDefined(varname)
        #    dep.value = value

        # For literal dependencies, we only have to return the value
        # specified in the configuration file.
        if dep.is_literal():
            return dep.value

        # Symbol dependencies can be resolved using the import_symbol()
        # function.
        if dep.is_symbol():
            symbol = import_symbol(dep.value)
            if dep.requires_invocation():
                symbol = symbol(*dep.args, **dep.kwargs)

            #if dep.mode == 'append':
            #    seq = provider.provider._Provider__resolved.get(dep.name)
            #    seq.append(symbol)

            return symbol

        # Dependency collections are simple lists of dependencies.
        if dep.is_collection():
            return DependencyCollection(self.provider, dep.members)

        # In this implementation, nested dependencies MUST be declared
        # in order e.g. if B depends on A, then A has to be already
        # resolved. In practice this means that in the configuration file,
        # nested dependencies can not refer to dependencies declared after
        # themselves.
        for name in dep.requires():
            if not self.provider.is_satisfied(name):
                raise UnsatisfiedDependency(name)

        # If the dependency is in injected but does not have a factor,
        # it simply points to an already resolved declaration.
        if dep.is_injected() and not dep.has_factory():
            return self.provider.resolve(dep.key)

        # Get the factory, positional and keyword arguments, and
        # chained dependencies from the provider.
        f = dep.factory.resolve(self)
        args = [x.resolve(self) for x in dep.args]
        kwargs = {x: y.resolve(self) for x, y in dep.kwargs.items()}
        chain = [x.resolve(self) for x in dep.chain]

        # So now we invoke f using args and kwargs, and map it
        # to all functions in chain.
        result = f(*args, **kwargs)
        for f in chain:
            result = f(result)
        return result
