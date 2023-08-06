import unittest

from ioc.injector import ArgumentDependencyInjector
from ioc.injector import Resolvable


class ArgumentDependencyInjectorTestCase(unittest.TestCase):

    def setUp(self):
        self.injector = ArgumentDependencyInjector()
        self.injector.provide('foo', 1)
        self.injector.add(TestResolvable())
        self.cls = TestDepender
        self.obj = self.cls()

    def test_default_value_for_argument(self):

        def f(foo, baz=2):
            self.assertEqual(foo, 1)
            self.assertEqual(baz, 2)

        self.injector.call(f)

    def test_can_not_inject_reserved_name(self):
        with self.assertRaises(ValueError):
            self.injector.provide('injector', None)

    def test_missing_dependency_raises(self):
        with self.assertRaises(self.injector.MissingDependency):
            self.injector.resolve(self.obj.missing)

    def test_missingdependency_formatting(self):
        try:
            self.injector.resolve(self.obj.missing)
        except self.injector.MissingDependency as e:
            text = str(e)
            self.assertTrue(repr(self.obj.missing) in text)
            self.assertTrue(text.find('missing') >= 0)
        else:
            self.fail("MissingDependency not raised.")

    def test_inject_with_bound_method(self):
        args, _ = self.injector.resolve(self.obj.method)
        self.assertEqual(args[0], 1)

    def test_resolvable_is_resolved(self):
        args, _ = self.injector.resolve(self.obj.resolvable)
        self.assertIsInstance(args[0], TestResolvable)
        self.assertTrue(self.injector.is_resolvable(args[0]))

    def test_run_in_context(self):
        self.assertTrue(not self.injector.is_provided('baz'))
        with self.injector.context({'baz': 1}):
            self.assertTrue(self.injector.is_provided('baz'))

        self.assertTrue(not self.injector.is_provided('baz'))


class TestDepender:

    def missing(self, missing):
        pass

    def method(self, foo):
        pass

    def resolvable(self, bar):
        pass


class TestResolvable(Resolvable):
    resolver_name = 'bar'
