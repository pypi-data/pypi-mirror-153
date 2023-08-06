"""Provides the interface to load configuration files."""
import yaml
from unimatrix import etc

from .provider import get_requirement


class TemplateDependencyProvider:
    """A dependency provider for use in templates."""

    def __getitem__(self, name):
        r = get_requirement(name)
        return r


def read(fp: str) -> list:
    """Read configuration from `fp`, replace and inject variables, and
    return a list containing the declared dependencies.
    """
    return yaml.safe_load(
        etc.read(fp, ioc=TemplateDependencyProvider())
    )
