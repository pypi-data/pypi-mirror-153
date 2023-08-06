import copy
import unittest

from marshmallow.exceptions import ValidationError

from ioc.schema.adapters import ArgumentDependencyAdapter
from ioc.schema.requirement import SchemaRequirement


class ArgumentDependencyAdapterTestCase(unittest.TestCase):
    params = {
        'type': "literal",
        'value': 1
    }

    def setUp(self):
        self.schema = ArgumentDependencyAdapter()

    def test_parser_with_valid_params(self):
        params = self.schema.load(copy.copy(self.params))

    def test_parser_with_valid_params_returns_correct_type(self):
        params = self.schema.load(copy.copy(self.params))

        self.assertIsInstance(params, SchemaRequirement)

    def test_parser_requires_string_if_symbol(self):
        params = {
            'type': 'symbol',
            'value': 1 # not a string
        }
        with self.assertRaises(ValidationError):
            params = self.schema.load(params)
            self.assertTrue('value' in errors)

    def test_parser_requires_string_if_ioc(self):
        params = {
            'type': 'ioc',
            'value': 1 # not a string
        }
        with self.assertRaises(ValidationError):
            params = self.schema.load(params)
            self.assertTrue('value' in errors)

    def test_symbol_must_be_not_a_keyword(self):
        params = {
            'type': 'symbol',
            'value': 'return'
        }
        with self.assertRaises(ValidationError):
            params = self.schema.load(params)
            self.assertTrue('value' in errors)

    def test_symbol_must_be_valid_identifier(self):
        params = {
            'type': 'symbol',
            'value': '1a'
        }
        with self.assertRaises(ValidationError):
            params = self.schema.load(params)
            self.assertTrue('value' in errors)
