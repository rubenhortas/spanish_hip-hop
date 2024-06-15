from enum import Enum

CSV_FILE = 'Spanish hip-hop list - Lista de trabajos.csv'
CSV_DELIMITER = ','


class CsvPosition(Enum):
    ID = 0  # referencia
    ARTIST = 1  # artista
    TITLE = 2  # trabajo
    PUBLICATION_DATE = 3  # fecha publicación: año
    FORMAT = 4  # tipo:  'Directo', 'Doble LP', 'EP', 'LP', 'Maqueta', 'Maxi Single', 'Mixtape', 'Promo', 'Recopilatorio','Single'
    MEDIUM = 5  # medio: 'CAS', 'CD', 'UNK', 'VIN', 'WEB'
    PRESERVED_IN_DIGITAL = 6  # preservado en digital: 'Sí'/'No'
    DIGITAL_FORMAT = 7  # Formato digital en el que lo tenemos preservado: 'FLAC', 'M4A', 'MP3', 'WAV'. 'WMA'
    BIT_RATE = 8  # Bit rate: 'CBR128', 'CBR154', 'CBR160', ..., 'VBR122', 'VBR124', ...
    PRESERVER = 9  # Preserver
    PRESERVATION_DATE = 10  # fecha preservado: fecha
    MODIFICATION_DATE = 11  # fecha modificado: fecha
    SOURCE = 12  # fuente
    SEEN_ONLINE = 13  # visto online: 'Sí'/'No'
    NOTES = 14  # notas
