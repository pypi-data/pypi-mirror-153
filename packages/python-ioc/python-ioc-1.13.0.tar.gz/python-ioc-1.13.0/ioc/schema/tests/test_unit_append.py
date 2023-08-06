import unittest

import ioc


class AppendTestCase(unittest.TestCase):

    def setUp(self):
        ioc.provide('foo', [])
        ioc.provide('bar', None)

    def tearDown(self):
        ioc.teardown()

    def test_append_to_list(self):
        ioc.load([{
            'type': 'symbol',
            'name': 'foo',
            'mode': 'append',
            'value': 'int',
            'callable': True,
            'args': [1]
        }])
        self.assertIn(1, ioc.require('foo'))
