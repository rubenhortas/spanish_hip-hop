import unittest

from tools.format_file import Album
from tools.libraries.config import CSV_SEPARATOR


class TestAlbum(unittest.TestCase):
    def setUp(self):
        self.lines = [
            ('1,bob mc & alice dj,-,-,-,-,-,-,-,-,-,-,-,-,', '1,Bob MC & Alice DJ,-,-,-,-,-,-,-,-,-,-,-,-,'),
            ('1,cpv,-,-,-,-,-,-,-,-,-,-,-,-,', '1,CPV,-,-,-,-,-,-,-,-,-,-,-,-,'),
            ('1,bob mc,the album vol. ii,-,-,-,-,-,-,-,-,-,-,-,', '1,Bob MC,The album Vol. II,-,-,-,-,-,-,-,-,-,-,-,')
        ]

    def test_format_album(self):
        for line, expected_result in self.lines:
            album = Album(line)
            self.assertEqual(expected_result, str(album))
