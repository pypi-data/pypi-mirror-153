import unittest

import ioc


class PublicInterfaceTestCase(unittest.TestCase):

    def tearDown(self):
        ioc.provider.teardown()

    def test_provide_satisfies_name(self):
        ioc.provide('foo', 1)
        self.assertTrue(ioc.provider.is_satisfied('foo'))

    def test_teardown_clears_dependencies(self):
        ioc.provide('foo', 1)
        ioc.teardown()
        self.assertTrue(not ioc.provider.is_satisfied('foo'))
