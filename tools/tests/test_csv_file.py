import unittest

from config.config import CsvPosition, CSV_HEADER


class TestCsv(unittest.TestCase):
    header = CSV_HEADER

    def _create_line(self, album_id: str, artist: str, title: str, preserver: str = '') -> list:
        line = ['' for _ in range(len(self.header))]

        line[CsvPosition.ID.value] = album_id
        line[CsvPosition.ARTIST.value] = artist
        line[CsvPosition.TITLE.value] = title
        line[CsvPosition.PRESERVER.value] = preserver

        return line
