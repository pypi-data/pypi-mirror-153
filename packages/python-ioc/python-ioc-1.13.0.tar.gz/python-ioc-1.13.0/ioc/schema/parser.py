import copy
import importlib

from marshmallow.exceptions import ValidationError

from ioc.schema.exc import InvalidDeclaration
from ioc.schema.adapters import SymbolDependencyAdapter
from ioc.schema.adapters import FileDependencyAdapter
from ioc.schema.adapters import LiteralDependencyAdapter
from ioc.schema.adapters import NestedDependencyAdapter
from ioc.schema.adapters import DependencyCollectionAdapter
from ioc.schema.base import Schema


class SchemaParser(object):
    """Parses the dependency configuration schema."""

    def __init__(self, provider=None, override=False):
        self.provider = provider or importlib.import_module('ioc.provider')
        self.override = override

    def load(self, dependencies):
        """Inspect the dependency configuration and validate the declared
        items.
        """
        schema = Schema(self.provider, override=self.override)

        # Check that each dependency has at least a name.
        names = set()
        for dep in dependencies:
            name = dep.get('name')
            if name is None:
                raise InvalidDeclaration(dep, "No name specified")

            if not isinstance(name, str):
                raise InvalidDeclaration(dep, "Invalid name specified: %s" % repr(name))
            if name in names:
                raise InvalidDeclaration(dep, "Duplicate name: %s" % name)

            names.add(name)

        # For each dependency, try to load them as either a Simple, Literal
        # or NestedDependency.
        adapters = [
            SymbolDependencyAdapter(),
            NestedDependencyAdapter(),
            FileDependencyAdapter(),
            LiteralDependencyAdapter(),
            DependencyCollectionAdapter(),
        ]

        for dep in dependencies:
            cleaned_dep = None
            for adapter in adapters:
                try:
                    cleaned_dep = adapter.load(copy.deepcopy(dep))
                    break
                except ValidationError:
                    pass

                cleaned_dep = None

            # If there is still no dependency loaded at this point, this
            # means the declaration was invalid.
            if cleaned_dep is None:
                raise InvalidDeclaration(dep, "Invalid dependency declaration")
            schema.add(cleaned_dep)

        return schema
