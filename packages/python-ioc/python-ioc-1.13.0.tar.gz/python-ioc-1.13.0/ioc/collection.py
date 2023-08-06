

class DependencyCollection(object):

    def __init__(self, provider, members):
        self._names = members
        self._provider = provider
        self._members = []

    def __getitem__(self, arg):
        members = self._names.__getitem__(arg)
        return [self._provider.resolve(x) for x in members]\
            if isinstance(arg, slice)\
            else self._provider.resolve(members)

    def __iter__(self):
        for _, name in enumerate(self._names):
            yield self._provider.resolve(name)
