#!/usr/bin/env python3
import copy
import os
import signal

from tools.config.artists import ARTISTS, SEPARATORS
from tools.config.config import CSV_FILE, CSV_SEPARATOR, CsvPosition
from tools.crosscutting.strings import GENERATING_NEW, DONE
from tools.domain.album import Album
from tools.helpers.file_helpers import read_file, backup, write_file
from tools.helpers.os_helpers import handle_sigint
from tools.utils.list_utils import create_python_list

_INPUT_FILE = os.path.join(os.path.abspath(''), CSV_FILE)
_OUTPUT_FILE = f"{os.path.join(os.path.abspath(''), 'config', 'artists.py')}"


def _get_artists(lines: list) -> (dict, list):
    def _update_artists(artist: str) -> None:
        if not artist.isnumeric():  # Numbers will not be transformed
            key = artist.lower()

            if key not in artists or is_preserved:
                # If the album is preserved, the prevailing value is the preserved one
                artists[key] = artist

    artists = copy.deepcopy(ARTISTS)  # Deep copy
    separators = SEPARATORS

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        artist = line_[CsvPosition.ARTIST.value]
        is_preserved = line_[CsvPosition.PRESERVER.value] != '' and line_[CsvPosition.PRESERVER.value] != '-'

        _update_artists(artist)

        artists_, separators_ = Album.get_artists(artist)

        for artist in artists_:
            _update_artists(artist)

        for separator in separators_:
            if separator not in separators:
                separators.append(separator)

    return dict(sorted(artists.items())), sorted(list(separators))


def _write_output_file(artists: dict, separators: list) -> None:
    separators = create_python_list('SEPARATORS', separators)
    artists = create_python_list('ARTISTS', artists)

    result = []
    result.extend(separators)
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
        * 'value': The name that the artist name will be formatted to, and will appear as in the final file.
            - The default format is 'titlecase', i.e. the first letter of each word in uppercase, 
              for example: 'Bob The Foobar'.
            - Setting an artist name format is used to preserve uppercase, lowercase, special words, etc.,
              for example: 'BoB ThE FooBaR'.
            - When formatting the name exceptions defined in the EXCEPTIONS dictionary (file '/config/exceptions.py') 
              will also apply to the artist.
    """

    signal.signal(signal.SIGINT, handle_sigint)
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    lines = read_file(_INPUT_FILE)[1:]
    artists, separators = _get_artists(lines)

    backup(_OUTPUT_FILE)
    _write_output_file(artists, separators)

    print(DONE)
