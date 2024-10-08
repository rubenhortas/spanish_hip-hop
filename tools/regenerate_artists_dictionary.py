#!/usr/bin/env python3
import os
import signal

from config.artists import ARTISTS
from config.config import CSV_FILE, CsvPosition, CSV_EMPTY_FIELD_VALUE
from crosscutting.strings import GENERATING_NEW, DONE, PRESERVED_BY
from domain.album import Album
from helpers.file_helpers import write_file, read_csv_file, backup
from helpers.os_helpers import handle_sigint
from utils.list_utils import create_python_dictionary

_INPUT_FILE = os.path.join(os.path.abspath(''), CSV_FILE)
_OUTPUT_FILE = f"{os.path.join(os.path.abspath(''), 'config', 'artists.py')}"


def regenerate_artists_dictionary(lines: list) -> None:
    """
    Updates the artist name translation dictionary 'ARTISTS' (file '/config/artists.py').
    Combines the artist names from the 'ARTISTS' dictionary (file '/config/artists.py') with the artist names
    from the albums in the CSV file.
    The resulting dictionary will be free of duplicates and sorted alphabetically.

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
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    artists = _get_artists(lines)

    backup(_OUTPUT_FILE)
    _write_output_file(artists)


def _get_artists(lines: list) -> dict:
    def _update_artists_dictionary(artist: str) -> None:
        if not artist.isnumeric():  # Numbers will not be transformed
            preserver = line[CsvPosition.PRESERVER.value]
            is_preserved = preserver != '' and preserver != CSV_EMPTY_FIELD_VALUE
            key = artist.lower().strip()
            used_keys.add(key)

            if key not in artists and not is_preserved:
                artists[key] = (artist.strip().title(), '')  # 'key': ('value', 'comment')

            if is_preserved:  # If the album is preserved, the prevailing value is the preserved one
                artists[key] = (artist.strip(), f"{PRESERVED_BY} {preserver}")

    artists = {}
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

            album_artists = Album.get_artists(artist)

            for artist in album_artists:
                _update_artists_dictionary(artist)

    if lines:
        artists = _delete_unused_keys(artists, used_keys)
        print()

    return dict(sorted(artists.items()))


def _delete_unused_keys(artists: dict, used_keys: set) -> dict:
    artists_keys = [key for key in artists]

    for key in artists_keys:
        if key not in used_keys:
            artists.pop(key)

    return artists


def _write_output_file(artists: dict) -> None:
    artists_ = create_python_dictionary('ARTISTS', artists)
    write_file(_OUTPUT_FILE, artists_)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)

    lines = read_csv_file(_INPUT_FILE)[1:]
    regenerate_artists_dictionary(lines)

    print(DONE)
