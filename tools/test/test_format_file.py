import unittest

from tools.format_file import Album


class TestFormatFile(unittest.TestCase):
    def setUp(self):
        self.csv_separator = ','
        self.albums = [
            'bob mc & alice dj,-,-,-',
            'cpv,-,-,-',
            'bob mc,the album vol. ii,-,-'
        ]
        self.expected_result = [
            'Bob MC & Alice DJ,-,-,-',
            'CPV,-,-,-',
            'Bob MC,The album Vol. II,-,-'
        ]

    def test_format_file(self):
        result = []

        for entry in self.albums:
            entry_ = entry.split(self.csv_separator)
            album = Album(entry_[0], entry_[1], entry_[2], entry_[3])  # artist, title, date, format
            result.append(str(album))

        self.assertEqual(self.expected_result, result)
