# pylint: skip-file
import unittest

import django
from django.conf import settings

import ioc


class DjangoAppTestCase(unittest.TestCase):

    def setUp(self):
        ioc.teardown()
        settings.configure(
            INSTALLED_APPS=['ioc']
        )
        django.setup()

    def test_django_dependency_is_provided(self):
        self.assertTrue(ioc.is_satisfied('DjangoDependency'))
