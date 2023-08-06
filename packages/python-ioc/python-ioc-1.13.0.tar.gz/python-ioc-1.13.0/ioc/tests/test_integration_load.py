import os
import unittest

import ioc


WORKDIR = os.path.dirname(__file__)


class LoadConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.dirname = WORKDIR

    def tearDown(self):
        ioc.teardown()

    def test_load_config_with_path(self):
        ioc.load_config([self.dirname + "/test_load.ioc"])
        self.assertTrue(ioc.is_satisfied('foo'))
