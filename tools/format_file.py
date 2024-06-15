#!/usr/bin/env python3
import signal

from tools.config.config import CSV_FILE, CSV_HEADER
from tools.crosscutting.strings import FORMATTING_LINES, POORLY_FORMATTED_LINES_INVALID_NUMBER_OF_SEPARATORS, \
    GENERATING, DONE, FORMATTED, ERRORS
from tools.domain.album import Album, WrongSeparatorsException
from tools.helpers.file_helpers import write_file, read_file
from tools.helpers.os_helpers import handle_sigint, clear_screen

_OUTPUT_FILE = f"{CSV_FILE[:-4]}-{FORMATTED.lower()}.csv"
_ERROR_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}.csv"


def _get_formatted_lines(line: list) -> (list, list):
    albums = []
    errors = []
    lines_ = [line.strip() for line in line]
    len_lines = len(lines_)
    current_line = 0

    print(f"{FORMATTING_LINES}...")

    for line in lines_:
        current_line += 1
        print(f"\r{current_line}/{len_lines}", end='')

        try:
            albums.append(Album(line))
        except WrongSeparatorsException:
            errors.append(line)

    print()

    return sorted(albums), errors


def _write_output_file(albums: list) -> None:
    if albums:
        result = [f"{CSV_HEADER}\n"]
        result.extend([f"{str(album)}\n" for album in albums])
        write_file(_OUTPUT_FILE, result)


def _write_error_file(errors: list) -> None:
    if errors:
        result = [f"{POORLY_FORMATTED_LINES_INVALID_NUMBER_OF_SEPARATORS}:\n\n"]
        result.extend([f"{error}\n" for error in errors])
        write_file(_ERROR_FILE, result)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{GENERATING} '{_OUTPUT_FILE}'...")

    lines = read_file(CSV_FILE)[1:]
    formatted_lines, errors = _get_formatted_lines(lines)

    _write_output_file(formatted_lines)
    _write_error_file(errors)

    print(DONE)
