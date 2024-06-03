import unittest

from tools.format_file import Album


class TestFormatFile(unittest.TestCase):
    def setUp(self):
        self.lines = [
            ('0,bob,album,2024,maqueta,unk,sí,mp3,192,rodrigozzz,2023-02-14,,maximorespeto,sí,-',
             '0,Bob,Album,2024,Maqueta,UNK,Sí,MP3,192,rodrigozzz,2023-02-14,,maximorespeto,Sí,-'),
            ('1,bob mc & alice dj,-,-,-,-,-,-,-,-,-,-,-,-,-', '1,Bob mc & alice dj,-,-,-,-,-,-,-,-,-,-,-,-,-'),
            ('2,bob mc,the album vol. ii,-,-,-,-,-,-,-,-,-,-,-,-', '2,Bob mc,The album vol. ii,-,-,-,-,-,-,-,-,-,-,-,-')
        ]

    def test_format_file(self):
        for line, expected_result in self.lines:
            album = Album(line)
            self.assertEqual(expected_result, str(album))
