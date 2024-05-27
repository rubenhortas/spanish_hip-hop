import unittest

from tools.find_issues import _get_issues


class TestFindIssues(unittest.TestCase):
    def setUp(self):
        self.lines = [
            'Bob,Album1,2024, Ok\n',
            'Bob,Album1,2024,Extra separator,\n',
            'Bob,(Album1,2024,Parentheses issue\n',
            'Bob,(Album1,2024,Extra separator + Parentheses issue,\n'
        ]

        self.extra_separators_expected = [
            'Bob,Album1,2024,Extra separator,\n',
            'Bob,(Album1,2024,Extra separator + Parentheses issue,\n'
        ]

        self.parentheses_issues_expected = [
            'Bob,(Album1,2024,Parentheses issue\n',
            'Bob,(Album1,2024,Extra separator + Parentheses issue,\n'
        ]

    def test_get_issues(self):
        extra_separators, parentheses_issues = _get_issues(self.lines)
        self.assertEqual(self.extra_separators_expected, extra_separators)
        self.assertEqual(self.parentheses_issues_expected, parentheses_issues)
