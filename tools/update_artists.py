#!/usr/bin/env python3
import os
import signal

from tools.config.config import CSV_FILE
from tools.crosscutting.strings import GENERATING_NEW, DONE
from tools.domain.album import Album
from tools.helpers.file_helpers import read_file, backup, write_file
from tools.helpers.os_helpers import handle_sigint
from tools.utils.list_utils import create_python_list, create_python_dictionary

_INPUT_FILE = os.path.join(os.path.abspath(''), CSV_FILE)
_OUTPUT_FILE = f"{os.path.join(os.path.abspath(''), 'config', 'artists.py')}"


def _get_artists(lines: list) -> (dict, list):
    artists = {}
    separators = set()

    for line in lines:
        album = Album(line)

        key = album.artist.lower()

        if not album.artist.isnumeric():
            if key in artists and album.has_preserver():
                artists[key] = album.artist
            else:
                artists[key] = album.artist

        album_artists, album_separators = album.get_artists()

        for artist in album_artists:
            if artist.isalnum() and not artist.isnumeric():
                key = artist.lower()

                if key in artists and album.has_preserver():
                    artists[key] = album.artist
                else:
                    artists[key] = album.artist

        for separator in album_separators:
            separators.add(separator)

    return dict(sorted(artists.items())), sorted(list(separators))


def _write_output_file(artists: dict, separators: list) -> None:
    separators = create_python_list('SEPARATORS', separators)
    art = create_python_dictionary('ARTISTS', artists)

    result = []
    result.extend(separators)
    result.append('\n')
    result.extend(art)

    write_file(_OUTPUT_FILE, result)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    lines = read_file(_INPUT_FILE)[1:]
    artists, separators = _get_artists(lines)

    backup(_OUTPUT_FILE)
    _write_output_file(artists, separators)

    print(DONE)
