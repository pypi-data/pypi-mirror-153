from collections import defaultdict

from ioc.exc import UnsatisfiedDependency
from ioc.exc import DependencySatisfied


class Provider(object):

    def __init__(self):
        self.__dependencies = {}
        self.__requirements = {}
        self.__resolved = {}
        self.__listeners = defaultdict(list)
        self.__tags = defaultdict(set)

    def add_listener(self, names, callback):
        """Adds a dependency as a listener to the provider. This
        is used to notify them in changes of dependencies.
        """
        for name in names:
            self.__listeners[name].append(callback)

    def get_requirement(self, name):
        """Get the declared requirement by name, or ``None``."""
        if not isinstance(name, str):
            raise ValueError("`name` must be a string.")
        return self.__requirements.get(name)

    def is_satisfied(self, name):
        """Return a boolean indicating if the dependency identified by
        `name` is satisfied.
        """
        return name in self.__resolved

    def resolve(self, name):
        """Return the Python object to which the dependency `name` resolved."""
        if name not in self.__resolved:
            raise UnsatisfiedDependency(name)
        return self.__resolved[name]

    def retire(self, name):
        """Remove a depedency from the registry. This is mainly used
        during testing. Return a boolean indicating if a dependency
        was removed.
        """
        if name not in self.__resolved:
            return False

        del self.__resolved[name]
        for tag in dict.keys(self.__tags):
            if name not in self.__tags[tag]:
                continue
            self.__tags[tag].remove(name)

        return True

    def require(self, names, requirement):
        """Register a requirement."""
        for name in names:
            self.__requirements[name] = requirement

    def register(self, name, value, force=False, tags=None):
        """Register `value` as resolved under `name`."""
        if name in self.__resolved and not force:
            raise DependencySatisfied(name)
        self.__resolved[name] = value
        for callback in self.__listeners[name]:
            callback(name, value)

        for tag in (tags or []):
            self.__tags[tag].add(name)

    def provide(self, dep, force=False):
        """Satisfy the requirement identified by :attr:`Dependency.name`,
        optionally force overwrite by providing ``force=True``.
        """
        if force:
            raise NotImplementedError

        if dep.name in self.__dependencies:
            raise DependencySatisfied("Dependency already satisfied: %s" % dep.name)

        self.__dependencies[dep.name] = dep

    def get(self, name, *names):
        """Return the dependency that is identified by `name`."""
        if names:
            raise NotImplementedError

        if name not in self.__dependencies:
            raise UnsatisfiedDependency(name)

        return self.__dependencies.get(name)

    def teardown(self):
        """Tears down all dependencies and requirements."""
        self.__dependencies = {}
        self.__requirements = {}
        self.__resolved = {}

    def tagged(self, tag):
        """Return the identifiers of all dependencies tagged with
        `tag`.
        """
        return list(map(self.resolve, sorted(self.__tags[tag])))

    def get_unsatisfied_dependencies(self):
        """Return the list of dependencies that are not injected."""
        return set(dict.keys(self.__requirements))\
            - set(dict.keys(self.__dependencies))

    #def require(self, names):
    #    return DeclaredRequirement(self, names)


provider = Provider()
provide = provider.provide
retire = provider.retire
teardown = provider.teardown
get = provider.get
get_requirement = provider.get_requirement
get_unsatisfied_dependencies = provider.get_unsatisfied_dependencies
register = provider.register
require = provider.require
is_satisfied = provider.is_satisfied
resolve = provider.resolve
add_listener = provider.add_listener
tagged = provider.tagged
#require = provider.require
