import unittest

from ioc.dependency import Dependency
from ioc.exc import DependencySatisfied
from ioc.exc import UnsatisfiedDependency
from ioc import provider


class ProviderTestCase(unittest.TestCase):

    def setUp(self):
        self.dep = Dependency('foo', int, 'public')
        provider.provide(self.dep)

    def tearDown(self):
        provider.teardown()

    def test_get_unknown_raises(self):
        with self.assertRaises(UnsatisfiedDependency):
            provider.get('bar')

    def test_provide_with_force_overwrite_raises(self):
        with self.assertRaises(NotImplementedError):
            provider.provide(self.dep, force=True)

    def test_get_multiple_names_raises(self):
        with self.assertRaises(NotImplementedError):
            provider.get('foo','bar')

    def test_multiple_register_without_force_raises(self):
        with self.assertRaises(DependencySatisfied):
            provider.provide(self.dep)

    def test_get_returns_dependency(self):
        dep = provider.get('foo')
        self.assertIsInstance(dep, Dependency)
        self.assertEqual(dep.name, 'foo')
        self.assertEqual(dep.value, int)

    def test_resolve_raises_on_unsatisfied(self):
        with self.assertRaises(UnsatisfiedDependency):
            provider.resolve('foo')

    def test_register_raises_on_satisfied(self):
        provider.register('foo', 1)
        with self.assertRaises(DependencySatisfied):
            provider.register('foo', 1)
