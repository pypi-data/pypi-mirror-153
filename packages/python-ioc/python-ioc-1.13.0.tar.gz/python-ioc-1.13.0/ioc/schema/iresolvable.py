

class IResolvable(object):
    """Base class for resolvable objects."""

    def has_factory(self):
        return False

    def requires(self):
        return []

    def requires_invocation(self):
        return False

    def is_injected(self):
        return False

    def is_symbol(self):
        return False

    def is_literal(self):
        return False

    def is_collection(self):
        return False

    def resolve(self, resolver):
        return resolver.resolve(self)

