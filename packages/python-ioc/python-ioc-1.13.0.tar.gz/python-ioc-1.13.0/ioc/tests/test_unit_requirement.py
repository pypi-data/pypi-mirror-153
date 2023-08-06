import unittest

from ioc import provider
from ioc.exc import UnsatisfiedDependency
import ioc


class StringRequirementTestCase(unittest.TestCase):
    dep = {
        'name': 'foo',
        'value': "bar"
    }

    def setUp(self):
        self.req = ioc.require('foo')
        self.unr = ioc.require('bar')
        ioc.load([self.dep])

    def tearDown(self):
        provider.teardown()

    def test_contains(self):
        self.assertIn('bar', self.req, self.req._injected)

    def test_setattr(self):
        # Strings are immutable, so setattr will raise AttributeError
        with self.assertRaises(AttributeError):
            self.req.foo = 'foo'

    def test_cannot_delete_injected(self):
        with self.assertRaises(TypeError):
            del self.req._injected

    def test_cannot_delete_names(self):
        with self.assertRaises(TypeError):
            del self.req._names

    def test_cannot_delete_provider(self):
        with self.assertRaises(TypeError):
            del self.req._names

    def test_delattr_invoked(self):
        with self.assertRaises(AttributeError):
            del self.req.foo

    def test_getattr(self):
        self.assertEqual(self.req.upper(), 'BAR')

    def test_bool(self):
        self.assertTrue(bool(self.req))

    def test_dir(self):
        self.assertEqual(dir(self.req), dir('bar'))

    def test_class_property_raises_when_not_injected(self):

        class A(object):
            bar = ioc.class_property('bar', str)

        obj = A()
        self.assertTrue(not provider.is_satisfied('bar'))
        with self.assertRaises(UnsatisfiedDependency):
            obj.bar

    def test_class_property_on_class(self):
        class A(object):
            foo = ioc.class_property('foo', str)

        self.assertTrue(provider.is_satisfied('foo'))
        self.assertIsInstance(A.foo, str)
        self.assertEqual(A.foo, 'bar')

    def test_class_property_set_value_on_class(self):
        class A(object):
            foo = ioc.class_property('foo', str)

        self.assertTrue(provider.is_satisfied('foo'))
        A.foo = 1
        self.assertEqual(A.foo, 1)
        self.assertEqual(ioc.require('foo'), 'bar')

    def test_class_property_set_value_on_instance(self):
        class A(object):
            foo = ioc.class_property('foo', str)

        self.assertTrue(provider.is_satisfied('foo'))
        a = A()
        a.foo = 1
        self.assertEqual(a.foo, 1)
        self.assertEqual(A.foo, 'bar')
        self.assertEqual(ioc.require('foo'), 'bar')

    def test_class_property_is_correct_datatype(self):
        class A(object):
            foo = ioc.class_property('foo', str)

        obj = A()
        self.assertTrue(provider.is_satisfied('foo'))
        self.assertIsInstance(obj.foo, str)
        self.assertEqual(obj.foo, 'bar')

    def test_class_property_unsatisfied_with_default(self):
        class A(object):
            taz = ioc.class_property('taz', str, default=1)

        obj = A()
        self.assertEqual(obj.taz, '1')

    def test_class_property_unsatisfied_with_default_without_factory(self):
        class A(object):
            taz = ioc.class_property('taz', default=1)

        obj = A()
        self.assertEqual(obj.taz, 1)

    def test_class_property_satisfied_with_default(self):
        ioc.provide('taz', 2)
        class A(object):
            taz = ioc.class_property('taz', str, default=1)

        obj = A()
        self.assertEqual(obj.taz, '2')

    def test_class_property_satisfied_with_default_without_factory(self):
        ioc.provide('taz', 2)
        class A(object):
            taz = ioc.class_property('taz', default=1)

        obj = A()
        self.assertEqual(obj.taz, 2)

    def test_class_property_dynamic_set(self):
        class A(object):
            foo1 = ioc.class_property('foo')
            foo2 = ioc.class_property('foo')
            def __init__(self):
                self.foo1 = 'baz'

        obj = A()
        self.assertEqual(obj.foo1, 'baz')
        self.assertEqual(obj.foo2, 'bar')
