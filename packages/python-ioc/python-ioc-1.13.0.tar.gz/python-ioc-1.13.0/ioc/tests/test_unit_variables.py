# pylint: skip-file
import os
import unittest

import ioc


class VariableTestCase(unittest.TestCase):

    def setUp(self):
        ioc.load_config()

    def test_environment_variable_is_replaced(self):
        self.assertEqual(
            str(ioc.require('EnvironmentVariable')),
            os.environ.get('IOC_TEST_VALUE')
        )
