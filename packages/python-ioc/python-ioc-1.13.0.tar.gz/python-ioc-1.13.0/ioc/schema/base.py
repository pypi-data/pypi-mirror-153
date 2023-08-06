

class Schema(object):
    """Represents a syntactically correct dependency
    configuration.
    """

    def __init__(self, provider, override=False):
        self.provider = provider
        self.override = override
        self.dependencies = []

    def add(self, dep):
        self.dependencies.append(dep)

    def resolve(self, resolver):
        """Resolve all dependencies and register them with the provider. This
        method is atomic: if one dependency fails, none of the dependencies
        are added to the provider.
        """
        for dep in self.dependencies:
            if dep.mode == 'append':
                seq = self.provider.resolve(dep.name)
                seq.append(dep.resolve(resolver))
            else:
                self.provider.register(
                    dep.key, dep.resolve(resolver), force=self.override,
                    tags=dep.tags
                )
