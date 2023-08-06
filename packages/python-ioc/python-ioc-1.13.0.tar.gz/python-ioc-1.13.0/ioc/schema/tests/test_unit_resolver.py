import copy
import fractions
import os
import sys
import unittest

from ioc.exc import EnvironmentVariableNotDefined
from ioc.exc import UnsatisfiedDependency
from ioc.schema.requirement import SchemaRequirement
from ioc.schema.resolver import SchemaResolver
from ioc.schema.dependency import LiteralDependency
from ioc.schema.dependency import SimpleDependency
from ioc.schema.dependency import NestedDependency
from ioc import provider


class SchemaResolverTestCase(unittest.TestCase):

    def setUp(self):
        self.resolver = SchemaResolver(provider)
        os.environ.pop('IOC_ENV_VAR', None)

    def tearDown(self):
        # Remove any leftover dependencies.
        provider.teardown()

    def test_resolve_with_literal_schema_requirement(self):
        req = SchemaRequirement('literal', 1)
        self.assertEqual(req.resolve(self.resolver), 1)

    def test_resolve_with_symbol_schema_requirement(self):
        req = SchemaRequirement('symbol', 'sys.version')
        self.assertEqual(req.resolve(self.resolver), sys.version)

    def test_resolve_with_symbol_attr_schema_requirement(self):
        req = SchemaRequirement('symbol', 'fractions.Fraction.from_float')
        self.assertEqual(req.resolve(self.resolver), fractions.Fraction.from_float)

    def test_resolve_with_literal_dependency(self):
        req = LiteralDependency('foo', 1)
        self.assertEqual(req.resolve(self.resolver), 1)

    def test_resolve_with_symbol_dependency(self):
        req = SimpleDependency('foo', 'sys.version')
        self.assertEqual(req.resolve(self.resolver), sys.version)

    def test_resolve_with_invoked_symbol_dependency(self):
        req = SimpleDependency('foo', 'int', args=["0xff", 16])
        self.assertEqual(req.resolve(self.resolver), 255)

    def test_with_nested_and_injected_factory(self):
        # Resolve the dependency foo so that it becomes available
        # for b
        provider.register('foo', int)

        dep = NestedDependency(
            name='bar',
            factory=SchemaRequirement('ioc', 'foo'),
            args=[SchemaRequirement('literal', "1")]
        )

        self.assertEqual(dep.resolve(self.resolver), 1)

    def test_with_nested_and_chained_output(self):
        # Resolve the dependency foo so that it becomes available
        # for b
        provider.register('foo', int)

        dep = NestedDependency(
            name='bar',
            factory=SchemaRequirement('ioc', 'foo'),
            args=[SchemaRequirement('literal', "1")],
            chain=[SchemaRequirement('symbol', 'str')]
        )

        self.assertEqual(dep.resolve(self.resolver), '1')

    def test_resolving_raises_exception_on_unsatisfied_dependency(self):
        dep = NestedDependency(
            name='bar',
            factory=SchemaRequirement('ioc', 'foo')
        )
        with self.assertRaises(UnsatisfiedDependency):
            dep.resolve(self.resolver)
