import unittest

from ioc import provider
from ioc.schema.base import Schema
from ioc.schema.dependency import LiteralDependency
from ioc.schema.dependency import NestedDependency
from ioc.schema.resolver import SchemaResolver
from ioc.schema.requirement import SchemaRequirement


class SchemaTestCase(unittest.TestCase):

    def setUp(self):
        self.resolver = SchemaResolver(provider)

    def tearDown(self):
        provider.teardown()

    def test_add(self):
        dep = LiteralDependency('foo', 1)
        schema = Schema(provider)
        schema.add(dep)

    def test_resolve_with_literal_dependency(self):
        schema = Schema(provider)
        deps = [
            LiteralDependency('foo', 1)
        ]
        for dep in deps:
            schema.add(dep)

        schema.resolve(self.resolver)

        # The 'foo' dependency must now be resolved
        self.assertTrue(provider.is_satisfied('foo'))

    def test_resolve_with_multiple_literal_dependency(self):
        schema = Schema(provider)
        deps = [
            LiteralDependency('foo', 1),
            LiteralDependency('baz', 2),
            LiteralDependency('bar', 3)
        ]
        for dep in deps:
            schema.add(dep)

        schema.resolve(self.resolver)

        self.assertTrue(provider.is_satisfied('foo'))
        self.assertTrue(provider.is_satisfied('bar'))
        self.assertTrue(provider.is_satisfied('baz'))

    def test_with_dependency_tree(self):
        schema = Schema(provider)
        deps = [
            LiteralDependency('foo', 1),
            LiteralDependency('bar', 2),
            NestedDependency(
                name='baz',
                factory=SchemaRequirement('symbol', 'int'),
                args=[
                    SchemaRequirement('literal','0xff'),
                    SchemaRequirement('literal', 16),
                ]
            )
        ]

        for dep in deps:
            schema.add(dep)

        schema.resolve(self.resolver)

        self.assertTrue(provider.is_satisfied('foo'))
        self.assertTrue(provider.is_satisfied('bar'))
        self.assertTrue(provider.is_satisfied('baz'))
