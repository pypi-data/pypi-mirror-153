from ioc.schema.iresolvable import IResolvable


class SchemaRequirement(IResolvable):
    """Represents a requirement stated in the dependency configuration
    file.
    """

    @property
    def key(self):
        if not self.is_injected():
            raise AttributeError('key')
        return self.value

    def __init__(self, type, value, **params):
        self.type = type
        self.value = value
        self.mode = params.get('mode') or 'declare'

    def is_symbol(self):
        return self.type == 'symbol'

    def is_injected(self):
        return self.type == 'ioc'

    def is_literal(self):
        return self.type == 'literal'

    def resolve(self, resolver):
        """Resolve the dependency using `resolver`."""
        return resolver.resolve(self)

    def __iter__(self):
        return iter([self.type, self.value])

    def __hash__(self):
        return hash(type(self).__name__ + self.type + self.value)

    def __eq__(self, other):
        return hash(self) == hash(other) and type(self) == type(other)
