import unittest

import ioc


class DefaultValueTestCase(unittest.TestCase):

    def setUp(self):
        ioc.provide('foo', 1)
        ioc.provide('bar', 1)

    def tearDown(self):
        ioc.teardown()

    def test_default_with_no_dep_set(self):
        value = ioc.require('baz', default=2)
        self.assertEqual(value, 2)

    def test_default_removed_after_provided(self):
        value = ioc.require('baz', default=2)
        ioc.provide('baz', 3)
        self.assertEqual(value, 3)

    def test_default_with_existing_dependency(self):
        value = int(ioc.require('foo', default=2))
        self.assertEqual(value, 1)

    def test_default_updated_after_override(self):
        value = int(ioc.require('foo', default=2))
        self.assertEqual(value, 1)

        ioc.override('foo', 3)
        value = int(ioc.require('foo', default=2))
        self.assertEqual(value, 3)
