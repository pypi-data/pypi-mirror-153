import unittest

import marshmallow

from ioc.schema.dependency import LiteralDependency
from ioc.schema.adapters import LiteralDependencyAdapter


class LiteralDependencyAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.schema = LiteralDependencyAdapter()

    def test_literal_dependency_str(self):
        params = {
            'name': 'foo',
            'type': 'literal',
            'value': 'int'
        }

        dep = self.schema.load(params)
        self.assertIsInstance(dep, LiteralDependency)
        self.assertEqual(dep.value, 'int')

    def test_literal_dependency_int(self):
        params = {
            'name': 'foo',
            'type': 'literal',
            'value': 1
        }

        dep = self.schema.load(params)
        self.assertIsInstance(dep, LiteralDependency)
        self.assertEqual(dep.value, 1)
