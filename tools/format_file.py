#!/usr/bin/env python3

import signal

from tools.libraries.album import Album
from tools.libraries.config import CSV_FILE, CSV_HEADER, CSV_SEPARATOR
from tools.libraries.file_helpers import write_file, read_file
from tools.libraries.os_helpers import handle_sigint, clear_screen
from tools.libraries.string_utils import replace_exceptions, replace_volumes

_OUTPUT_FILE = f"{CSV_FILE[:-4]} - formateado.csv"


def _get_formatted_lines(line: list) -> list:
    lines_ = [line.strip() for line in line]
    albums = []

    for line in lines_:
        try:
            line_ = line.split(CSV_SEPARATOR)
            album = Album(line_[0], line_[1], line_[2], line_[3])  # artist, title, date, format
            album.artist = _format_artist(album.artist)

            albums.append(album)
        except IndexError:
            print(f"'{line}: bad format")

    return sorted(albums)


def _format_artist(artist: str) -> str:
    return replace_exceptions(artist)


def _format_title(title: str) -> str:
    formatted_title = replace_exceptions(title)
    formatted_title = replace_volumes(formatted_title)

    return formatted_title


def _write_output_file(albums: list) -> None:
    result = [f"{CSV_HEADER}\n"]
    result.extend([f"{str(album)}\n" for album in albums])
    write_file(_OUTPUT_FILE, result)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Generating {_OUTPUT_FILE}...")

    lines = read_file(CSV_FILE)[1:]
    formatted_lines = _get_formatted_lines(lines)
    _write_output_file(formatted_lines)

    print('Done')
