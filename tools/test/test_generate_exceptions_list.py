import unittest

from tools.generate_exceptions_list import _get_exceptions


class TestGenerateExceptionsDictionary(unittest.TestCase):
    def setUp(self):
        self.exceptions = [
            'key1',
            'Key1',
            'key2'
        ]

        self.expected_result = ["\t'Key1,'\n", "\t'key1,'\n", "\t'key2,'\n"]

    def test_get_keys(self):
        self.assertEqual(self.expected_result, _get_exceptions(self.exceptions))
