from enum import Enum

# User configs
ALBUM_FORMATS = ['Directo', 'Doble LP', 'EP', 'LP', 'Maqueta', 'Maxi Single', 'Mixtape', 'Promo', 'Recopilatorio',
                 'Single']
CSV_FILE = 'Spanish hip-hop list - Lista de trabajos.csv'
CSV_HEADER = ['Referencia', 'Artista', 'Trabajo', 'Fecha Publicación', 'Tipo', 'Medio', 'Preservado en digital',
              'Formato digital', 'Bitrate', 'Preservado por', 'Fecha preservado', 'Fecha modificado', 'Fuente',
              'Visto online', 'Notas']
CSV_DELIMITER = ','
CSV_EMPTY_FIELD_VALUE = '-'

# Fix mismatched parentheses
# 'Album (instrumentals' -> 'Album (instrumentals)'
# 'Album instrumentals)' -> 'Album (instrumentals)'
FIX_MISMATCHED_PARENTHESES = True  # True/False

# Fix mismatched quotes
# 'Album "instrumentals' -> 'Album "instrumentals"'
# 'Album instrumentals"' -> 'Album "instrumentals"'
FIX_MISMATCHED_QUOTES = True  # True/False

# Fix mismatched quotes
# 'Album [instrumentals' -> 'Album [instrumentals]'
# 'Album instrumentals]' -> 'Album [instrumentals]'
FIX_MISMATCHED_SQUARE_BRACKETS = True  # True/False

# Fix volume names
# 'vol?.?1' -> 'Vol. 1'
# 'vol.01' -> 'Vol. 01'
# 'vol.1' -> 'Vol. 1'
# 'vol. 1' -> 'Vol. 1'
# 'Vol .1' -> 'Vol. 1'
# 'vol. 01' -> 'Vol. 01'
# 'vol 1' -> 'Vol. 1'
# 'volume 1' -> 'Volume 1'
# 'volumen 1' -> 'Volumen 1'
# 'volume 1.5' -> 'Volume 1.5'
# 'vol i' -> 'Vol. I'
FIX_VOLUMES = True  # True/False

# Capitalize acronyms
# 'f.o.o.b.a.r.' -> 'F.O.O.B.A.R.'
# 'f.o.o.b.a.r' -> 'F.O.O.B.A.R'
CAPITALIZE_ACRONYMS = True  # True/False

# Replace artist in titles
# artist = { 'bob mc', 'BoB MC' }
# '"alice", "beef with bob mc"' -> '"Alice", "Beef with BoB MC"'
REPLACE_ARTISTS_IN_TITLES = True  # True/False


# Application configs.
# DO NOT MODIFY.

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
