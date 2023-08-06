import unittest

import ioc


class FailedBytesImportTestCase(unittest.TestCase):
    params = [
        {
            'name': 'VerificationService.secret_key',
            'type': 'symbol',
            'value': 'bytes',
            'callable': True,
            'args': ['4bb'],
            'kwargs': {'encoding': "ascii"}
        }
    ]

    def test_is_fixed(self):
        ioc.load(self.params)
