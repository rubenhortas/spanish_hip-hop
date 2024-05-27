import unittest

from tools.generate_exceptions_dictionary import _get_keys


class TestGenerateExceptionsDictionary(unittest.TestCase):
    def setUp(self):
        self.dictionary = {
            'key1': 'KEY1',
            'key1': 'KEY1',
            'key2': 'KEY2'
        }

        self.expected_entries = ["\t'key1': 'KEY1',\n", "\t'key2': 'KEY2',\n"]

    def test_get_keys(self):
        self.assertEqual(self.expected_entries, _get_keys(self.dictionary))
