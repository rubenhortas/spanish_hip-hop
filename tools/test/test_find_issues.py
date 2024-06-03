import unittest

from tools.find_issues import _get_issues


class TestFindIssues(unittest.TestCase):
    def setUp(self):
        self.lines = [
            # '1,bob,album1,2024,-,-,-,-,-,-,-,-,-,-,-'
            '1,Bob,Album1,2024,-,-,-,-,-,-,-,-,-,-,Ok\n',
            '2,Bob,(Album1),2024,-,-,-,-,-,-,-,-,-,-,Ok\n',
            '3,Bob,[Album1],2024,-,-,-,-,-,-,-,-,-,-,Ok\n',
            '4,Bob,Album1,2024,-,-,-,-,-,-,-,-,-,-,Extra separator,\n',
            '5,Bob,(Album1,2024,-,-,-,-,-,-,-,-,-,-,Mismatched parentheses\n',
            '6,Bob,(Album1,2024,-,-,-,-,-,-,-,-,-,-,Extra separator + Mismatched parentheses,\n',
            '7,Bob,[Album1,2024,-,-,-,-,-,-,-,-,-,-,Mismatched square brackets\n',
        ]

        self.extra_separators_expected = [
            '4,Bob,Album1,2024,-,-,-,-,-,-,-,-,-,-,Extra separator,\n',
            '6,Bob,(Album1,2024,-,-,-,-,-,-,-,-,-,-,Extra separator + Mismatched parentheses,\n'
        ]

        self.mismatched_parentheses_expected = [
            '5,Bob,(Album1,2024,-,-,-,-,-,-,-,-,-,-,Mismatched parentheses\n',
            '6,Bob,(Album1,2024,-,-,-,-,-,-,-,-,-,-,Extra separator + Mismatched parentheses,\n'
        ]

        self.mismatched_square_brackets_expected = ['7,Bob,[Album1,2024,-,-,-,-,-,-,-,-,-,-,Mismatched square brackets\n']

    def test_get_issues(self):
        extra_separators, mismatched_parentheses, mismatched_square_brackets = _get_issues(self.lines)
        self.assertEqual(self.extra_separators_expected, extra_separators)
        self.assertEqual(self.mismatched_parentheses_expected, mismatched_parentheses)
        self.assertEqual(self.mismatched_square_brackets_expected, mismatched_square_brackets)
