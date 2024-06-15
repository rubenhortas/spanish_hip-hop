import unittest

from tools.format_file import Album


class TestAlbum(unittest.TestCase):
    def setUp(self):
        self.albums = [
            # ('1,bob mc & alice dj,,,,,,,,,,,,,', '1,Bob MC & Alice DJ,,,,,,,,,,,,,'),
            # ('1,bob mc,the album vol. ii,,,,,,,,,,,,', '1,Bob MC,The album Vol. II,,,,,,,,,,,,'),
            # ('1,BoB Mc, ThE aLBuM,,,,,,,preserver,,,,,', '1,BoB Mc,ThE aLBuM,,,,,,,preserver,,,,,'),
            ('1,bob,"bob, the foobar",,,,,,,,,,,,', '1,Bob,"Bob the foobar",,,,,,,,,,,,')
        ]

        self.artists = [
            ('bob mc & alice', ['bob mc', 'alice']),
            ('bob mc + 1234', ['bob mc', '1234']),
            ('bob mc + alice & foobar (01.02.2024', ['bob mc', 'alice', 'foobar 01.02.2024']),
            ('&bob', ['&bob']),
            ('&bob & alice', ['&bob', 'alice'])
        ]

    def test_format_album(self):
        for line, expected_result in self.albums:
            album = Album(line)
            self.assertEqual(expected_result, str(album))

    def test_get_artists(self):
        for artist, expected_result in self.artists:
            # lower to test the resulting lists only
            self.assertEqual(expected_result, [artist.lower() for artist in Album.get_artists(artist)])
