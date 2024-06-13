import unittest

from tools.regenerate_exceptions import _get_exceptions


class TestGenerateExceptionsDictionary(unittest.TestCase):
    def setUp(self):
        self.dictionary = {
            'key1': 'KEY1',
            'key1': 'KEY1',
            'key2': 'KEY2'
        }

        self.expected_result = ["\t'key1': 'KEY1',\n", "\t'key2': 'KEY2',\n"]

    def test_get_keys(self):
        self.assertEqual(self.expected_result, _get_exceptions(self.dictionary))
