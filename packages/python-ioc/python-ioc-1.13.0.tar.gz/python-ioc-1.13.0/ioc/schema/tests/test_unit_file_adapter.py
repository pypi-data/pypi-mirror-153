import unittest

import marshmallow

from ioc.schema.dependency import LiteralDependency
from ioc.schema.adapters import FileDependencyAdapter


class FileDependencyAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.schema = FileDependencyAdapter()

    def test_literal_dependency_str(self):
        params = {
            'name': 'foo',
            'type': 'file',
            'path': 'README.md'
        }

        dep = self.schema.load(params)
        self.assertIsInstance(dep, LiteralDependency)
        self.assertEqual(dep.value, open('README.md', 'rb').read())
