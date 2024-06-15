#!/usr/bin/env python3
import os
import signal

from tools.config.artists import ARTISTS
from tools.config.config import CSV_FILE, CSV_SEPARATOR, CsvPosition
from tools.crosscutting.strings import GETTING_DICTIONARY_UNUSED_ARTIST_NAMES, DONE
from tools.domain.album import Album
from tools.helpers.file_helpers import read_file
from tools.helpers.os_helpers import handle_sigint

_INPUT_FILE = os.path.join(os.path.abspath('..'), CSV_FILE)


def _get_dictionary_unused_artist_names(lines: list) -> None:
    def _update_unused_names(artist: str) -> None:
        if not artist.isnumeric():
            key = artist.lower()

            if key in ARTISTS:
                used_names.add(key)

    used_names = set()

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        artist = line_[CsvPosition.ARTIST.value]
        artists_, _ = Album.get_artists(artist)

        _update_unused_names(artist)
        map(_update_unused_names, artists_)

    for key in ARTISTS:
        if key not in used_names:
            print(f"{key}")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"{GETTING_DICTIONARY_UNUSED_ARTIST_NAMES}'...")

    lines = read_file(_INPUT_FILE)[1:]

    _get_dictionary_unused_artist_names(lines)

    print(DONE)
