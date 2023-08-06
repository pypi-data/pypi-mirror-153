

class ConfigurationError(Exception):
    """An :exc:`ConfigurationError` is raised when a malformed or invalid
    configuration is parsed by the framework.
    """
    pass


class RequirementAlreadyResolved(Exception):
    pass


class UnsatisfiedDependency(LookupError):
    """The :exc:`UnsatisfiedDependency` exception is raised when an unknown
    dependency is requested from the provider.
    """
    pass


class MissingDependencies(Exception):
    """The :exc:`MissingDependencies` exception is raised when there are
    dependencies not injected.
    """
    pass


class EnvironmentVariableNotDefined(EnvironmentError):
    """Raises when an environment variable does not exist."""
    pass


class DependencySatisfied(Exception):
    """Raised when a duplicate dependency is provided."""
