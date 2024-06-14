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
        artist = line_[CsvPosition.ARTIST]
        is_preserved = line_[CsvPosition.PRESERVER] != '' and line_[CsvPosition.PRESERVER] != '-'

        _update_artists(artist)

        artists, separators = Album.get_artists(artist)

        for artist in artists:
            _update_artists(artist)

        for separator in separators:
            separators.add(separator)

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
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    lines = read_file(_INPUT_FILE)[1:]
    artists, separators = _get_artists(lines)

    backup(_OUTPUT_FILE)
    _write_output_file(artists, separators)

    print(DONE)
