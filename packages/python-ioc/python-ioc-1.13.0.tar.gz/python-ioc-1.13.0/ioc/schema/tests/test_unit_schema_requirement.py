import unittest

from ioc.schema.requirement import SchemaRequirement


class SchemaRequirementTestCase(unittest.TestCase):

    def test_equality(self):
        req1 = SchemaRequirement('symbol', 'foo')
        req2 = SchemaRequirement('symbol', 'foo')
        self.assertEqual(req1, req2)

    def test_is_symbol_returns_true_for_symbol(self):
        req = SchemaRequirement('symbol', 'foo')
        self.assertTrue(req.is_symbol())

    def test_is_injected_returns_true_for_ioc(self):
        req = SchemaRequirement('ioc', 'foo')
        self.assertTrue(req.is_injected())

    def test_is_literal_returns_true_for_literal(self):
        req = SchemaRequirement('literal', 'foo')
        self.assertTrue(req.is_literal())

    def test_iter_returns_type_and_value(self):
        args = ('symbol','foo')
        req = SchemaRequirement(*args)
        self.assertEqual(tuple(req), args)
