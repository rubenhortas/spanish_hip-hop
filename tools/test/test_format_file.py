import unittest

from tools.format_file import Album
from tools.libraries.config import CSV_SEPARATOR
from tools.format_file import _format_artist, _format_title


class TestFormatFile(unittest.TestCase):
    def setUp(self):
        self.albums = [
            ('bob mc & alice dj,-,-,-', 'Bob MC & Alice DJ,-,-,-'),
            ('cpv,-,-,-', 'CPV,-,-,-'),
            ('bob mc,the album vol. ii,-,-', 'Bob MC,The album Vol. II,-,-')
        ]

    def test_format_file(self):
        for album, expected_result in self.albums:
            album_ = album.split(CSV_SEPARATOR)
            formatted_album = Album(album_[0], album_[1], album_[2], album_[3])  # artist, title, date, format
            formatted_album.artist = _format_artist(formatted_album.artist)
            formatted_album.title = _format_title(formatted_album.title)
            self.assertEqual(expected_result, str(formatted_album))
