

class Dependency(object):
    """Wraps an injected dependency."""

    def __init__(self, name, value, visibility, **kwargs):
        self.name = name
        self.value = value
        self.visibility = visibility
