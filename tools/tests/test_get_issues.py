import unittest

from tools.config.config import CsvPosition
from tools.get_issues import _get_issues


class TestFindIssues(unittest.TestCase):
    def _create_line(self, album_id: str, artist: str, title: str) -> list:
        line = ['' for _ in range(len(self.header))]

        line[CsvPosition.ID.value] = album_id
        line[CsvPosition.ARTIST.value] = artist
        line[CsvPosition.TITLE.value] = title

        return line

    def setUp(self):
        self.header = ['Referencia', 'Artista', 'Trabajo', 'Fecha Publicación', 'Tipo', 'Medio', 'Preservado en digital', 'Formato digital', 'Bitrate', 'Preservado por', 'Fecha preservado', 'Fecha modificado', 'Fuente', 'Visto online', 'Notas']

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

        self.extra_separators_expected = [['6', 'Bob', 'Album', '', '', '', '', '', '', '', '', '', '', '', '', 'extra field']]
        self.mismatched_parentheses_expected = [['4', 'Bob', '(Album', '', '', '', '', '', '', '', '', '', '', '', '']]
        self.mismatched_square_brackets_expected = [['5', 'Bob', '[Album', '', '', '', '', '', '', '', '', '', '', '', '']]

    def test_get_issues(self):
        wrong_field_numbers, mismatched_parentheses, mismatched_square_brackets = _get_issues(self.lines, len(self.header))
        self.assertEqual(self.extra_separators_expected, wrong_field_numbers)
        self.assertEqual(self.mismatched_parentheses_expected, mismatched_parentheses)
        self.assertEqual(self.mismatched_square_brackets_expected, mismatched_square_brackets)
