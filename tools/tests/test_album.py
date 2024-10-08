from config.config import CsvPosition, CSV_EMPTY_FIELD_VALUE
from domain.album import WrongFieldsNumberException, Album
from tests.test_csv_file import TestCsv


class TestAlbum(TestCsv):
    def setUp(self):
        self.album_formats = [
            # Check that artist is titlecased and title is capitalized
            (self._create_line('1', 'bob and alice', 'the album'),
             self._create_line('1', 'Bob And Alice', 'The album')),

            # Delete whitespaces from fields
            (self._create_line('2', ' bob and alice ', ' the album '),
             self._create_line('2', 'Bob And Alice', 'The album')),

            # fix square brackets
            (self._create_line('3', 'bob', 'the [true album'),
             self._create_line('3', 'Bob', 'The [true album]')),
            (self._create_line('4', 'bob', 'the true] album'),
             self._create_line('4', 'Bob', 'The [true] album')),

            # fix parentheses
            (self._create_line('5', 'bob', 'the (true album'),
             self._create_line('5', 'Bob', 'The (true album)')),
            (self._create_line('6', 'bob', 'the true) album'),
             self._create_line('6', 'Bob', 'The (true) album')),

            # fix quotes
            (self._create_line('7', 'bob', 'the "true album'),
             self._create_line('7', 'Bob', 'The "true album"')),
            (self._create_line('8', 'bob', 'the true album"'),
             self._create_line('8', 'Bob', 'The true "album"')),

            # fix volumes
            (self._create_line('9', 'bob', 'the album vol. ii'),
             self._create_line('9', 'Bob', 'The album Vol. II')),

            # Do not modify preserved albums
            (self._create_line('10', 'BoB Mc', 'ThE aLBuM', 'Alice'),
             self._create_line('10', 'BoB Mc', 'ThE aLBuM', 'Alice')),

            # Keep commas
            (self._create_line('11', 'bob', 'i love you, music'),
             self._create_line('11', 'Bob', 'I love you, music')),
        ]

        line_ok_len = self._create_line('12', 'bob and alice', 'the album')

        extra_field_line = line_ok_len
        extra_field_line[CsvPosition.ID.value] = '13'
        extra_field_line.append('extra field')

        less_fields_line = line_ok_len[1:3]
        less_fields_line[CsvPosition.ID.value] = '14'

        self.wrong_fields_number_lines = [
            extra_field_line,
            less_fields_line
        ]

        self.album_artists = [
            ('bob mc & alice', ['bob mc', 'alice']),
            ('bob mc + 1234', ['bob mc', '1234']),
            ('bob mc + alice & foobar (01.02.2024', ['bob mc', 'alice', 'foobar 01.02.2024']),
            ('&bob', ['&bob']),
            ('&bob & alice', ['&bob', 'alice']),
            ('bob (con alice)', ['bob', 'alice']),
            ('bob, alice', ['bob', 'alice'])
        ]

        self.empty_fields = [
            ('', CSV_EMPTY_FIELD_VALUE),
            (' ', CSV_EMPTY_FIELD_VALUE),
            (' foo  bar     ', 'foo bar')
        ]

    def test_wrong_fields_number_exception(self):
        for line in self.wrong_fields_number_lines:
            with self.assertRaises(WrongFieldsNumberException):
                Album(line, len(self.header))

    def test_format_album(self):
        for line, expected_result in self.album_formats:
            album = Album(line, len(self.header))
            self.assertEqual(expected_result, album.list())

    def test_get_artists(self):
        for album_artist, expected_result in self.album_artists:
            self.assertEqual(expected_result, [artist for artist in Album.get_artists(album_artist)])

    def test_get_value(self):
        for string, expected in self.empty_fields:
            self.assertEqual(expected, Album._get_field_value(string))
