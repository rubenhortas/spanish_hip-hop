#!/usr/bin/env python3

import signal

from tools.libraries.config import CSV_FILE, CSV_HEADER, CSV_SEPARATOR
from tools.libraries.file_helpers import write_file, read_file
from tools.libraries.os_helpers import handle_sigint, clear_screen
from tools.libraries.album import Album

CSV_OUTPUT_FILE = f"{CSV_FILE[:-4]} - formateado.csv"


def _get_albums(line: list) -> list:
    lines_ = [line.strip() for line in line]
    albums = []

    for line in lines_:
        try:
            line_ = line.split(CSV_SEPARATOR)
            album = Album(line_[0], line_[1], line_[2], line_[3])  # artist, title, date, format
            albums.append(album)
        except IndexError:
            print(f"'{line}: bad format")

    return sorted(albums)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Generating {CSV_OUTPUT_FILE}")
    lines = read_file(CSV_FILE)[1:]
    albums = _get_albums(lines)
    result = [f"{CSV_HEADER}\n"]
    result.extend([f"{str(album)}\n" for album in albums])
    write_file(CSV_OUTPUT_FILE, result)
    print('Done')
