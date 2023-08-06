import unittest

import ioc


class DependencyTagTestCase(unittest.TestCase):

    def setUp(self):
        ioc.provide('foo', 1, tags=['test'])
        ioc.provide('bar', 2, tags=['test'])

    def tearDown(self):
        ioc.teardown()

    def test_get_by_tag(self):
        deps = ioc.tagged('test')
        self.assertEqual(set(deps), set([1, 2]))
