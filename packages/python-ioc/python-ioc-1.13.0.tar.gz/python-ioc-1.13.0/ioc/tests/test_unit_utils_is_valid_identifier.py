# -*- coding: UTF-8 -*-
import unittest

import six

from ioc.utils import is_valid_identifier


class IsValidIdentifierTestCase(unittest.TestCase):

    def test_with_keyword(self):
        self.assertFalse(is_valid_identifier('return'))

    def test_with_leading_number(self):
        self.assertFalse(is_valid_identifier('1a'))

    @unittest.skipIf(six.PY2, "No unicode testing needed on Py2")
    def test_with_unicode(self):
        self.assertTrue(is_valid_identifier('aå'))
