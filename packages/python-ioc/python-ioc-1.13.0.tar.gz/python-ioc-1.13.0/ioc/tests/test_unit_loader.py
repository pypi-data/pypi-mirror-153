import unittest

from ioc import loader


class LoaderTestCase(unittest.TestCase):

    def test_import_module_fail_silent_true(self):
        """Import a non-existing module with the `fail_silent` flag
        set to true. None must be returned.
        """
        self.assertEqual(loader.import_module('foo', True), None)

    def test_import_module_fail_silent_false(self):
        """Import a non-existing module with the `fail_silent` flag
        set to false. An ImportError must be raised.
        """
        with self.assertRaises(ImportError):
            loader.import_module('foo', False)

    def test_import_module(self):
        import os

        self.assertEqual(loader.import_module('os'), os)

    def test_import_nested_module(self):
        import os.path

        self.assertEqual(loader.import_module('os.path'), os.path)

    def test_import_builtin(self):
        self.assertEqual(loader.import_builtin('int'), int)

    def test_import_builtin_fail_silent_true(self):
        self.assertEqual(loader.import_builtin('foo', True), None)

    def test_import_builtin_fail_silent_false(self):
        with self.assertRaises(ImportError):
            loader.import_builtin('foo', False)

    def test_import_symbol_from_builtin(self):
        self.assertEqual(loader.import_symbol('int'), int)

    def test_import_symbol_classmethod_from_builtin(self):
        self.assertEqual(loader.import_symbol('dict.fromkeys'), dict.fromkeys)

    def test_import_symbol_module(self):
        import os
        self.assertEqual(loader.import_symbol('os'), os)

    def test_import_symbol_nested_module(self):
        import os.path
        self.assertEqual(loader.import_symbol('os.path'), os.path)

    def test_import_symbol_attribute_from_module(self):
        import os
        self.assertEqual(loader.import_symbol('os.chmod'), os.chmod)

    def test_import_symbol_attribute_from_nested_module(self):
        import os.path
        self.assertEqual(loader.import_symbol('os.path.join'), os.path.join)

    def test_import_symbol_attribute_from_member_in_module(self):
        import fractions
        self.assertEqual(loader.import_symbol('fractions.Fraction.from_float'),
            fractions.Fraction.from_float)

    def test_import_symbol_fail_silent_is_true_with_no_dots(self):
        self.assertEqual(loader.import_symbol('foo', True), None)

    def test_import_symbol_fail_silent_is_false_with_no_dots(self):
        with self.assertRaises(ImportError):
            loader.import_symbol('foo', False)

    def test_import_symbol_fail_silent_is_true_with_one_dots(self):
        self.assertEqual(loader.import_symbol('foo.bar', True), None)

    def test_import_symbol_fail_silent_is_false_with_one_dots(self):
        with self.assertRaises(ImportError):
            loader.import_symbol('foo.bar', False)

    def test_import_symbol_fail_silent_is_true_with_existing_parent(self):
        self.assertEqual(loader.import_symbol('os.foo', True), None)

    def test_import_symbol_fail_silent_is_false_with_existing_parent(self):
        with self.assertRaises(ImportError):
            loader.import_symbol('os.foo', False)

    def test_import_symbol_fail_silent_is_true_with_existing_nested_parent(self):
        self.assertEqual(loader.import_symbol('os.path.foo', True), None)

    def test_import_symbol_fail_silent_is_false_with_existing_nested_parent(self):
        with self.assertRaises(ImportError):
            loader.import_symbol('os.path.foo', False)
