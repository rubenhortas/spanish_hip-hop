#!/usr/bin/env python3
import os
import signal

from tools.config.artists import ARTISTS, DELIMITERS
from tools.config.config import CSV_FILE, CsvPosition
from tools.crosscutting.strings import GENERATING_NEW, DONE, PRESERVED_BY
from tools.domain.album import Album
from tools.helpers.file_helpers import write_file, read_csv_file, backup
from tools.helpers.os_helpers import handle_sigint
from tools.utils.list_utils import create_python_list

_INPUT_FILE = os.path.join(os.path.abspath(''), CSV_FILE)
_OUTPUT_FILE = f"{os.path.join(os.path.abspath(''), 'config', 'artists.py')}"


def regenerate_artists_dictionary(lines: list) -> None:
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    artists, delimiters = _get_artists(lines)

    backup(_OUTPUT_FILE)
    _write_output_file(artists, delimiters)


def _get_artists(lines: list) -> (dict, list):
    def _update_artists_dictionary(artist: str) -> None:
        if not artist.isnumeric():  # Numbers will not be transformed
            preserver = line[CsvPosition.PRESERVER.value]
            is_preserved = preserver != '' and preserver != '-'
            key = artist.lower()
            used_keys.add(key)

            if key not in artists and not is_preserved:
                artists[key] = (artist.title(), '')  # 'key': ('value', 'comment')

            if is_preserved:  # If the album is preserved, the prevailing value is the preserved one
                artists[key] = (artist, f"{PRESERVED_BY} {preserver}")

    artists = {}
    delimiters = DELIMITERS
    current_line = 0
    len_lines = len(lines)
    used_keys = set()

    for key in ARTISTS:
        artists[key] = (ARTISTS[key], '')  # 'key': ('value', 'comment')

    for line in lines:
        current_line += 1
        print(f"\r{current_line}/{len_lines}", end='')

        if line:
            artist = line[CsvPosition.ARTIST.value]

            _update_artists_dictionary(artist)

            album_artists, artists_delimiters = Album.get_artists(artist)

            for artist in album_artists:
                _update_artists_dictionary(artist)

            for delimiter in artists_delimiters:
                if delimiter not in delimiters:
                    delimiters.append(delimiter)

    if lines:
        artists = _delete_unused_keys(artists, used_keys)
        print()

    return dict(sorted(artists.items())), sorted(list(delimiters))


def _delete_unused_keys(artists: dict, used_keys: set) -> dict:
    artists_keys = [key for key in artists]

    for key in artists_keys:
        if key not in used_keys:
            artists.pop(key)

    return artists


def _write_output_file(artists: dict, delimiters: list) -> None:
    delimiters = create_python_list('DELIMITERS', delimiters)
    artists = create_python_list('ARTISTS', artists)

    result = []
    result.extend(delimiters)
    result.append('\n')
    result.extend(artists)

    write_file(_OUTPUT_FILE, result)


if __name__ == '__main__':
    """
    Updates the artist name translation dictionary 'ARTISTS' (file '/config/artists.py').
    Combines the artist names from the 'ARTISTS' dictionary (file '/config/artists.py') with the artist names 
    from the albums in the albums file (the CSV file).
    The resulting dictionary will be free of duplicates and alphabetically sorted.

    Dictionary format: 'key': 'value',
        ARTISTS = {
            'bob the foobar': 'Bob The Foobar',
        }

        * 'key': The artist name in lowercase
        * 'value': The name that the artist name will be transformed to.
            - The default format is 'titlecase' (the first letter of each word in uppercase), i.e:  'Bob The Foobar'.
            - Setting an artist name format is used to preserve uppercase, lowercase, special words, etc.,
              i.e.: 'BoB ThE FooBaR'.
            - When formatting the name exceptions defined in the EXCEPTIONS dictionary (file '/config/exceptions.py') 
              will *not* be applied to the artist.
    """

    signal.signal(signal.SIGINT, handle_sigint)

    lines = read_csv_file(_INPUT_FILE)[1:]
    regenerate_artists_dictionary(lines)

    print(DONE)
