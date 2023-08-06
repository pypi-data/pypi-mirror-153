import copy
import unittest

from marshmallow.exceptions import ValidationError
import marshmallow

from ioc.schema.adapters import NestedDependencyAdapter
from ioc.schema.dependency import NestedDependency
from ioc.schema.requirement import SchemaRequirement


class NestedDependencyAdapterTestCase(unittest.TestCase):

    def setUp(self):
        self.schema = NestedDependencyAdapter()

    def test_with_valid_keyword_arguments(self):
        params = {
            "name" : "foo",
            "factory": {"type":"symbol", "value": "str"},
            "kwargs": {
                "bar": {
                    "type": "literal",
                    "value": "baz"
                }
            }
        }
        dep = self.schema.load(params)
        self.assertIsInstance(dep, NestedDependency)
        self.assertIn('bar', dep.kwargs)

    def test_factory_is_required(self):
        params = {
            "name" : "foo",
        }
        with self.assertRaises(ValidationError):
            dep = self.schema.load(params)

    def test_factory_must_be_callable_dependency(self):
        params = {
            "name" : "foo",
            "factory": None
        }
        with self.assertRaises(ValidationError):
            dep = self.schema.load(params)

    def test_load_returns_nested_dependency(self):
        params = {
            "name" : "foo",
            "factory": {"type":"symbol", "value": "str"}
        }
        dep = self.schema.load(params)
        self.assertIsInstance(dep, NestedDependency)
