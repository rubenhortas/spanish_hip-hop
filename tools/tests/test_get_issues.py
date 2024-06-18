from tools.get_issues import _get_issues
from tools.tests.test_csv_file import TestCsv


class TestFindIssues(TestCsv):
    def setUp(self):
        line = self._create_line('1', 'Bob', 'Album')

        extra_separator_line = line.copy()
        extra_separator_line[0] = '6'
        extra_separator_line.append('extra field')

        self.lines = [
            line,  # Ok
            self._create_line('2', 'Bob', '(Album)'),  # Ok
            self._create_line('3', 'Bob', '[Album]'),  # Ok
            self._create_line('4', 'Bob', '(Album'),  # Mismatched parentheses
            self._create_line('5', 'Bob', '[Album'),  # Mismatched square brackets
            extra_separator_line,
        ]

        self.wrong_field_numbers_expected = [
            ['6', 'Bob', 'Album', '', '', '', '', '', '', '', '', '', '', '', '', 'extra field']]
        self.mismatched_parentheses_expected = [
            ['4', 'Bob', '(Album', '', '', '', '', '', '', '', '', '', '', '', '']
        ]
        self.mismatched_square_brackets_expected = [
            ['5', 'Bob', '[Album', '', '', '', '', '', '', '', '', '', '', '', '']]

    def test_get_issues(self):
        issues = _get_issues(self.lines, len(self.header))
        self.assertEqual(self.wrong_field_numbers_expected, issues.wrong_fields_number)
        self.assertEqual(self.mismatched_parentheses_expected, issues.mismatched_parentheses)
        self.assertEqual(self.mismatched_square_brackets_expected, issues.mismatched_square_brackets)
