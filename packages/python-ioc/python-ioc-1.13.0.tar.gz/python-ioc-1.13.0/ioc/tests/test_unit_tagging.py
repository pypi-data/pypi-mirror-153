from os.path import abspath
from os.path import dirname
from os.path import join
import unittest

import yaml

import ioc


class SchemaTaggingTestCase(unittest.TestCase):

    def setUp(self):
        self.config = abspath(join(dirname(__file__), 'tags.ioc'))
        with open(self.config) as f:
            ioc.load(yaml.safe_load(f.read()))

    def tearDown(self):
        ioc.teardown()

    def test_tagged_returns_foo_and_bar(self):
        names = ioc.tagged('test')
        self.assertEqual(set(names), set([1, 2]))
