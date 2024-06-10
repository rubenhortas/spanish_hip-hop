#!/usr/bin/env python3
import os
import signal

from tools.exceptions import EXCEPTIONS
from tools.libraries.config import CSV_SEPARATOR, CSV_FILE
from tools.libraries.file_helpers import write_file, read_file
from tools.libraries.os_helpers import handle_sigint

_OUTPUT_FILE = f"{os.path.join(os.path.abspath('..'), 'libraries', 'artists.py')}"


def _get_artists_from_file() -> list:
    lines = read_file(os.path.join(os.path.abspath('..'), CSV_FILE))[1:]
    artists_ = set()

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        artists_.add(line_[1].strip())

    artists = [f"{artist}" for artist in artists_]

    return artists


def _create_dict(artists: list) -> list:
    artists_ = []

    for artist in artists:
        key = artist.lower().replace("'", "\\'")

        if key in EXCEPTIONS:
            value = EXCEPTIONS[key]
        else:
            value = artist.replace("'", "\\'")

        artists_.append(f"\t'{key.lower()}':'{value}',\n")

    return artists_


def _write_output_file(keys):
    artists_dictionary = ['ARTISTS = {\n']
    artists_dictionary.extend(keys)
    artists_dictionary.append('}\n')
    write_file(_OUTPUT_FILE, artists_dictionary)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"Generating new {_OUTPUT_FILE}...")

    artists = _get_artists_from_file()
    artists = _create_dict(artists)
    _write_output_file(artists)

    print('Done')
