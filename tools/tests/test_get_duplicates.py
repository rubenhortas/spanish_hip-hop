import unittest

from tools.get_duplicates import _get_duplicates


class TestGetDuplicates(unittest.TestCase):
    def setUp(self):
        self.lines = [
            '1,Bob,Title vol.1,,,,,,,,,,,,',
            '2,Bob,Title vol.2,,,,,,,,,,,,',
            '3,Bob,Title,,,,,,,,,,,,',
            '4,Bob,Title@?!$,,,,,,,,,,,,',
            '5,Bob,Title (more words),,,,,,,,,,,,',
            '6,Bob,T.i.t.l.@,,,,,,,,,,,,',
            '7,Alice,Another title,,,,,,,,,,,,'
        ]

        self.expected_duplicates = ['3,Bob,Title,,,,,,,,,,,,  -> 4,Bob,Title@?!$,,,,,,,,,,,,']
        self.expected_possible_duplicates = [
            '1,Bob,Title vol.1,,,,,,,,,,,,  -> 2,Bob,Title vol.2,,,,,,,,,,,,',
            '4,Bob,Title@?!$,,,,,,,,,,,,  -> 6,Bob,T.i.t.l.@,,,,,,,,,,,,']

    def test_get_duplicates(self):
        duplicates, possible_duplicates = _get_duplicates(self.lines)
        self.assertEqual(self.expected_duplicates, duplicates)
        self.assertEqual(self.expected_possible_duplicates, possible_duplicates)
