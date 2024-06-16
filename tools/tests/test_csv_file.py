import unittest

from tools.config.config import CsvPosition


class TestCsv(unittest.TestCase):
    header = ['Referencia', 'Artista', 'Trabajo', 'Fecha Publicación', 'Tipo', 'Medio', 'Preservado en digital', 'Formato digital', 'Bitrate', 'Preservado por', 'Fecha preservado', 'Fecha modificado', 'Fuente', 'Visto online', 'Notas']

    def _create_line(self, album_id: str, artist: str, title: str, preserver: str = '') -> list:
        line = ['' for _ in range(len(self.header))]

        line[CsvPosition.ID.value] = album_id
        line[CsvPosition.ARTIST.value] = artist
        line[CsvPosition.TITLE.value] = title
        line[CsvPosition.PRESERVER.value] = preserver

        return line
