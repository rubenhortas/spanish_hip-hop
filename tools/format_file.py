#!/usr/bin/env python3

import signal

from tools.libraries.album import Album
from tools.libraries.config import CSV_FILE, CSV_HEADER, CSV_SEPARATOR
from tools.libraries.file_helpers import write_file, read_file
from tools.libraries.format_helpers import has_correct_number_separators
from tools.libraries.os_helpers import handle_sigint, clear_screen

_OUTPUT_FILE = f"{CSV_FILE[:-4]} - formateado.csv"
_ERROR_FILE = f"errores - {CSV_FILE}.txt"


def _get_albums(line: list) -> (list, list):
    lines_ = [line.strip() for line in line]
    albums = []
    errors = []

    for line in lines_:
        if has_correct_number_separators(line):
            album = Album(line)
            albums.append(album)
        else:
            errors.append(line)

    return sorted(albums), errors


def _write_output_file(albums: list) -> None:
    result = [f"{CSV_HEADER}\n"]
    result.extend([f"{str(album)}\n" for album in albums])
    write_file(_OUTPUT_FILE, result)


def _write_error_file(errors: list) -> None:
    result = ['Bad formatted lines (extra separators)\n\n']
    result.extend([f"{error}\n" for error in errors])
    write_file(_ERROR_FILE, result)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Generating {_OUTPUT_FILE}...")

    lines = read_file(CSV_FILE)[1:]
    albums, errors = _get_albums(lines)

    if albums:
        _write_output_file(albums)

    if errors:
        _write_error_file(errors)

    print('Done')
