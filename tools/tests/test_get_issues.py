from tools.get_issues import _get_issues
from tools.tests.test_csv_file import TestCsv


class TestFindIssues(TestCsv):
    def setUp(self):
        line_ok_len = self._create_line('1', 'Bob', 'Album')

        extra_delimiter_line = line_ok_len.copy()
        extra_delimiter_line[0] = '6'
        extra_delimiter_line.append('extra field')

        minus_delimiter_line = line_ok_len[:-1]
        minus_delimiter_line[0] = '7'

        self.lines = [
            line_ok_len,  # Ok
            self._create_line('2', 'Bob', '(Album)'),  # Ok
            self._create_line('3', 'Bob', '[Album]'),  # Ok
            self._create_line('4', 'Bob', '(Album'),  # Mismatched parentheses
            self._create_line('5', 'Bob', '[Album'),  # Mismatched square brackets
            extra_delimiter_line,
            minus_delimiter_line,

            # Publication date in title, but not in field
            self._create_line('6', 'Bob 2024', 'Album'),
            self._create_line('7', 'Bob [2024]', 'Album'),
            self._create_line('8', 'Bob (2024) foo year', 'Album'),

            # Album format in title, but not in field
            self._create_line('8', 'Bob (EP) foo format', 'Album')
        ]

        self.wrong_field_numbers_expected = [
            extra_delimiter_line,
            minus_delimiter_line
        ]

        self.mismatched_parentheses_expected = [
            self._create_line('4', 'Bob', '(Album')
        ]

        self.mismatched_square_brackets_expected = [
            self._create_line('5', 'Bob', '[Album')
        ]

        self.publication_date_in_title_expected = [
            self._create_line('6', 'Bob 2024', 'Album'),
            self._create_line('7', 'Bob [2024]', 'Album'),
            self._create_line('8', 'Bob (2024) foo year', 'Album')
        ]

        self.album_format_in_title_expected = [
            self._create_line('8', 'Bob (EP) foo format', 'Album')
        ]

    def test_get_issues(self):
        issues = _get_issues(self.lines, len(self.header))
        self.assertEqual(self.wrong_field_numbers_expected, issues.wrong_fields_number)
        self.assertEqual(self.mismatched_parentheses_expected, issues.mismatched_parentheses)
        self.assertEqual(self.mismatched_square_brackets_expected, issues.mismatched_square_brackets)
        self.assertEqual(self.publication_date_in_title_expected, issues.possible_publication_date)
        self.assertEqual(self.album_format_in_title_expected, issues.possible_album_format)
