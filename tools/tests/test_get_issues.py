from tools.get_issues import _get_issues
from tools.tests.test_csv_file import TestCsv


class TestFindIssues(TestCsv):
    def setUp(self):
        self.line_ok_len = self._create_line('1', 'Bob', 'Album')  # Ok
        self.line2 = self._create_line('2', 'Bob', '(Album)')  # Ok
        self.line3 = self._create_line('3', 'Bob', '[Album]')  # Ok
        self.line4 = self._create_line('4', 'Bob', '(Album')  # Mismatched parentheses
        self.line5 = self._create_line('5', 'Bob', '[Album')  # Mismatched square brackets

        self.line6 = self.line_ok_len.copy()  # Line with extra fields
        self.line6[0] = '6'
        self.line6.append('extra field')

        self.line7 = self.line_ok_len[:-1]  # Line with minus fields
        self.line7[0] = '7'

        # Lines with publication date in title, but not in field
        self.line8 = self._create_line('8', 'Bob 2024', 'Album')
        self.line9 = self._create_line('9', 'Bob [2024]', 'Album')
        self.line10 = self._create_line('10', 'Bob (2024) foo year', 'Album')

        # Lines with album format in title, but not in field
        self.line11 = self._create_line('11', 'Bob (EP) foo format', 'Album')

        self.lines = [
            self.line_ok_len,
            self.line2,
            self.line3,
            self.line4,
            self.line5,
            self.line6,
            self.line7,
            self.line8,
            self.line9,
            self.line10,
            self.line11
        ]

        self.mismatched_parentheses_expected = [
            self.line4
        ]

        self.mismatched_square_brackets_expected = [
            self.line5
        ]

        self.wrong_field_numbers_expected = [
            self.line6,
            self.line7
        ]

        self.publication_date_in_title_expected = [
            self.line8,
            self.line9,
            self.line10
        ]

        self.album_format_in_title_expected = [
            self.line11
        ]

    def test_get_issues(self):
        issues = _get_issues(self.lines, len(self.header))
        self.assertEqual(self.wrong_field_numbers_expected, issues.wrong_fields_number)
        self.assertEqual(self.mismatched_parentheses_expected, issues.mismatched_parentheses)
        self.assertEqual(self.mismatched_square_brackets_expected, issues.mismatched_square_brackets)
        self.assertEqual(self.publication_date_in_title_expected, issues.possible_publication_date)
        self.assertEqual(self.album_format_in_title_expected, issues.possible_album_format)
