# pylint: skip-file
import unittest

import ioc
from ioc.exc import MissingDependencies


class UnsatisfiedDependenciesTestCase(unittest.TestCase):

    def test_required_dep_in_unsatisfied(self):
        dep = ioc.require('foo')
        unsatisfied = ioc.get_unsatisfied_dependencies()
        self.assertIn('foo', unsatisfied, msg=unsatisfied)

    def test_check_raises(self):
        dep = ioc.require('foo')
        with self.assertRaises(MissingDependencies):
            ioc.check()
