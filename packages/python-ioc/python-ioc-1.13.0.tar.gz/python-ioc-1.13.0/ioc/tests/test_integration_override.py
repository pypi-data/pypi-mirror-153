from os.path import abspath
from os.path import dirname
from os.path import join
import unittest

import yaml

from ioc.exc import UnsatisfiedDependency
import ioc


class OverrideTestCase(unittest.TestCase):

    def setUp(self):
        self.pre = abspath(join(dirname(__file__), 'pre-override.ioc'))
        self.post = abspath(join(dirname(__file__), 'post-override.ioc'))

    def test_override_returns_new_value(self):
        req = ioc.require('foo')

        ioc.provide('foo', 'bar')
        self.assertEqual(str(req), 'bar')

        ioc.override('foo', 'baz')
        self.assertEqual(str(req), 'baz')

    def test_override_with_schema(self):
        req = ioc.require('foo')
        with self.assertRaises(UnsatisfiedDependency):
            bool(req)

        with open(self.pre) as f:
            ioc.load(yaml.safe_load(f.read()))

        self.assertEqual(req, 'bar')

        with open(self.post) as f:
            ioc.load(yaml.safe_load(f.read()), override=True)

        self.assertEqual(req, 'baz')


    def tearDown(self):
        ioc.teardown()
