import unittest

from tools.get_duplicates import _get_duplicates, Line


class TestGetDuplicates(unittest.TestCase):
    def setUp(self):
        line1 = ['1', 'Bob', 'Title vol.1']
        line2 = ['2', 'Bob', 'Title vol.2']
        line3 = ['3', 'Bob', 'Title']
        line4 = ['4', 'Bob', 'Title@?!$']
        line5 = ['5', 'Bob', 'Title (more words)']
        line6 = ['6', 'Bob', 'T.i.t.l.@']
        line7 = ['7', 'Alice', 'Another title']

        self.lines = [
            line1,
            line2,
            line3,
            line4,
            line5,
            line6,
            line7
        ]

        expected_duplicates_line1 = Line(line1)
        expected_duplicates_line1.similar.append(Line(line2))

        expected_duplicates_line2 = Line(line3)
        expected_duplicates_line2.duplicates.append(Line(line4))
        expected_duplicates_line2.similar.append(Line(line6))

        self.expected_duplicates = [
            expected_duplicates_line1,
            expected_duplicates_line2
        ]

    def test_get_duplicates(self):
        self.assertEqual(self.expected_duplicates, _get_duplicates(self.lines))
