from os.path import abspath
from os.path import dirname
from os.path import join
import unittest

import yaml

import ioc


class SchemaTaggingTestCase(unittest.TestCase):

    def setUp(self):
        self.config = abspath(join(dirname(__file__), 'collection.ioc'))
        with open(self.config) as f:
            ioc.load(yaml.safe_load(f.read()))

        self.collection = ioc.require('foo')

    def test_iterable_contains_declared_members(self):
        members = list(self.collection)
        self.assertEqual(set(members), set([1,2,3]), members)

    def test_value_changes_after_override(self):
        ioc.override('baz', 4)
        members = list(self.collection)
        self.assertEqual(set(members), set([1,4,3]), members)

    def test_getitem(self):
        value = self.collection[1] # baz
        self.assertEqual(value, 2)

    def test_getitem_changes_after_override(self):
        ioc.override('baz', 4)
        value = self.collection[1] # baz
        self.assertEqual(value, 4)

    def test_getitem_with_slice(self):
        values = self.collection[1:]
        self.assertEqual(set(values), set([2,3]))

    def test_getitem_with_slice_changes_after_override(self):
        ioc.override('baz', 4)
        values = self.collection[1:]
        self.assertEqual(set(values), set([4,3]))

    def tearDown(self):
        ioc.teardown()
