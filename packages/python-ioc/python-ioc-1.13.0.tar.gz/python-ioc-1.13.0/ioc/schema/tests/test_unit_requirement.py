import unittest

from ioc.schema.requirement import SchemaRequirement


class SchemaRequirementTestCase(unittest.TestCase):

    def test_key_raises_attributeerror_on_non_injected(self):
        req = SchemaRequirement('literal', 1)
        with self.assertRaises(AttributeError):
            req.key
