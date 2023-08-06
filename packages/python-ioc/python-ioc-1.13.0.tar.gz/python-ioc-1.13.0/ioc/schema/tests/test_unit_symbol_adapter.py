import unittest

import marshmallow

from ioc.schema.dependency import SimpleDependency
from ioc.schema.adapters import SymbolDependencyAdapter


class SymbolDependencyAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.schema = SymbolDependencyAdapter(strict=True)

    @unittest.skip("Symbol dependencies are loaded by the resolver")
    def test_builtin_dependency(self):
        params = {
            'name': 'foo',
            'type': 'symbol',
            'value': 'int'
        }

        dep, errors = self.schema.load(params)
        self.assertIsInstance(dep, SimpleDependency)
        self.assertEqual(dep.value, int)

    @unittest.skip("Symbol dependencies are loaded by the resolver")
    def test_builtin_invoked(self):
        params = {
            'name': 'foo',
            'type': 'symbol',
            'value': "int",
            'callable': True,
            'args': ["1"]
        }

        dep, errors = self.schema.load(params)
        self.assertIsInstance(dep, SimpleDependency)
        self.assertEqual(dep.value, 1)

    @unittest.skip("Symbol dependencies are loaded by the resolver")
    def test_non_existing_symbol_raises_validationerror(self):
        params = {
            'name': 'foo',
            'type': 'symbol',
            'value': 'foo1'
        }
        with self.assertRaises(marshmallow.ValidationError):
            dep, errors = self.schema.load(params)

    @unittest.skip("Symbol dependencies are loaded by the resolver")
    def test_non_callable_raises_validationerror(self):
        params = {
            'name': 'foo',
            'type': 'symbol',
            'value': 'sys.version',
            'invoke': True
        }
        with self.assertRaises(marshmallow.ValidationError):
            dep, errors = self.schema.load(params)
