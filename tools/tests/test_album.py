import unittest

from tools.format_file import Album


class TestAlbum(unittest.TestCase):
    def setUp(self):
        self.lines = [
            ('1,bob mc & alice dj,,,,,,,,,,,,,', '1,Bob MC & Alice DJ,,,,,,,,,,,,,'),
            ('1,cpv,,,,,,,,,,,,,', '1,CPV,,,,,,,,,,,,,'),
            ('1,bob mc,the album vol. ii,,,,,,,,,,,,', '1,Bob MC,The album Vol. II,,,,,,,,,,,,'),
            ('1,BoB Mc, ThE aLBuM,,,,,,,preserver,,,,,', '1,BoB Mc,ThE aLBuM,,,,,,,preserver,,,,,')
        ]

        self.artists = [
            ('1,bob mc & alice,,,,,,,,,,,,,', ['bob mc', 'alice']),
            ('1,bob mc + 1234,,,,,,,,,,,,,', ['bob mc', '1234']),
            ('2,bob mc + alice & foobar (01.02.2024,,,,,,,,,,,,,', ['bob mc', 'alice', 'foobar 01.02.2024'])
        ]

    def test_format_album(self):
        for line, expected_result in self.lines:
            album = Album(line)
            self.assertEqual(expected_result, str(album))

    def test_get_artists(self):
        for line, expected_result in self.artists:
            album = Album(line)
            self.assertEqual(expected_result, [artist.lower() for artist in album.get_artists()])
