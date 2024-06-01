import unittest

from tools.format_file import Album
from tools.libraries.string_utils import capitalize_first_letter


class TestFormatFile(unittest.TestCase):
    def setUp(self):
        self.csv_separator = ','
        self.albums = [
            ('bob mc & alice dj,-,-,-', 'Bob mc & alice dj,-,-,-'),
            ('cpv,-,-,-', 'Cpv,-,-,-'),
            ('bob mc,the album vol. ii,-,-', 'Bob mc,The album vol. ii,-,-')
        ]

    def test_format_file(self):
        for album, expected_result in self.albums:
            entry_ = album.split(self.csv_separator)

            formatted_album = Album(entry_[0], entry_[1], entry_[2], entry_[3])  # artist, title, date, format
            formatted_album.artist = capitalize_first_letter(formatted_album.artist)
            formatted_album.title = capitalize_first_letter(formatted_album.title)

            self.assertEqual(expected_result, str(formatted_album))
