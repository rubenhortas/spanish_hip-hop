from tools.domain.album import WrongFieldsNumberException
from tools.format_file import Album
from tools.tests.test_csv_file import TestCsv


class TestAlbum(TestCsv):
    def setUp(self):
        self.albums = [
            (self._create_line('1', 'bob and alice', 'the album'), self._create_line('1', 'Bob And Alice', 'The album')),  # Artist titlecased and title capitalized
            (self._create_line('1', ' bob and alice ', ' the album '), self._create_line('1', 'Bob And Alice', 'The album')),  # Delete whitespaces from fields
            (self._create_line('1', 'bob', 'the [true album'), self._create_line('1', 'Bob', 'The [true album]')),  # fix square brackets
            (self._create_line('1', 'bob', 'the (true album'), self._create_line('1', 'Bob', 'The (true album)')),  # fix parentheses
            (self._create_line('1', 'bob', 'the album vol. ii'), self._create_line('1', 'Bob', 'The album Vol. II')),  # fix volumes
            (self._create_line('1', 'BoB Mc', 'ThE aLBuM', 'Alice'), self._create_line('1', 'BoB Mc', 'ThE aLBuM', 'Alice')),  # Do not modify preserved albums
            (self._create_line('1', 'bob', 'i love you, music'), self._create_line('1', 'Bob', 'I love you, music')),  # Keep commas
        ]

        self.artists = [
            ('bob mc & alice', ['bob mc', 'alice']),
            ('bob mc + 1234', ['bob mc', '1234']),
            ('bob mc + alice & foobar (01.02.2024', ['bob mc', 'alice', 'foobar 01.02.2024']),
            ('&bob', ['&bob']),
            ('&bob & alice', ['&bob', 'alice'])
        ]

    def test_wrong_fields_number_exception(self):
        wrong_field_lines = []
        line = self._create_line('1', 'bob and alice', 'the album')

        extra_field_line = line
        extra_field_line.append('extra field')
        wrong_field_lines.append(extra_field_line)

        less_fields_line = line[1:3]
        wrong_field_lines.append(less_fields_line)

        for _ in wrong_field_lines:
            with self.assertRaises(WrongFieldsNumberException):
                Album(extra_field_line, len(self.header))

    def test_format_album(self):
        for line, expected_result in self.albums:
            album = Album(line, len(self.header))
            self.assertEqual(expected_result, album.list())

    def test_get_artists(self):
        for artist, expected_result in self.artists:
            artists, _ = Album.get_artists(artist)
            # lower to test the resulting lists only
            self.assertEqual(expected_result, [artist.lower() for artist in artists])
