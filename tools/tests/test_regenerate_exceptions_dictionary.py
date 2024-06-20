import unittest

from tools.regenerate_exceptions_dictionary import _get_exceptions


class TestGenerateExceptionsDictionary(unittest.TestCase):
    def setUp(self):
        self.dictionary = {
            'key1': 'KEY11',
            'key1': 'KEY1',  # Duplicated key
            'key2': 'KEY2',
            'foo\'s bar': 'FOO\'S BAR'  # Escaped chars
        }

        self.expected_result = ["\t'foo\\'s bar': 'FOO\\'S BAR',\n", "\t'key1': 'KEY1',\n", "\t'key2': 'KEY2',\n"]

    def test_get_keys(self):
        self.assertEqual(self.expected_result, _get_exceptions(self.dictionary))
