import unittest

from ioc.schema.parser import SchemaParser
from ioc.schema.exc import InvalidDeclaration


class SchemaParserTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = SchemaParser()

    def test_duplicate_name_raises_error(self):
        deps = [
            {'name': 'foo', 'value': 1},
            {'name': 'foo', 'value': 2},
        ]
        with self.assertRaises(InvalidDeclaration):
            self.parser.load(deps)

    def test_missing_name_raises_error(self):
        deps = [
            {'value': 1},
            {'value': 2},
        ]
        with self.assertRaises(InvalidDeclaration):
            self.parser.load(deps)

    def test_invalid_name_raises_error(self):
        deps = [
            {'name': 1, 'value': 1},
        ]
        with self.assertRaises(InvalidDeclaration):
            self.parser.load(deps)

    def test_invalid_declaration_raises_error(self):
        deps = [
            {'name': "1", 'foo': 'bar'},
        ]
        with self.assertRaises(InvalidDeclaration):
            self.parser.load(deps)

    def test_with_valid_literal_declaration(self):
        deps = [
            {'name': "foo", 'value': 'bar', 'type':'literal'},
        ]
        self.parser.load(deps)
