#!/usr/bin/env python3
import signal

from tools.config.config import CSV_FILE, CSV_HEADER
from tools.crosscutting.strings import FORMATTING_LINES, GENERATING, DONE, FORMATTED, ERRORS, WRONG_FIELDS_NUMBER, \
    FORMATTING
from tools.domain.album import Album, WrongFieldsNumberException
from tools.helpers.file_helpers import read_csv_file, write_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen
from tools.regenerate_artists_dictionary import regenerate_artists_dictionary
from tools.regenerate_exceptions_dictionary import regenerate_exceptions_dictionary

_OUTPUT_FILE = f"{CSV_FILE[:-4]}-{FORMATTED.lower()}.csv"
_ERROR_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{WRONG_FIELDS_NUMBER}.csv"


def _format_file(lines: list) -> None:
    print(f"{GENERATING} '{_OUTPUT_FILE}'...")

    formatted_lines, wrong_lines = _get_formatted_lines(lines[1:], len(CSV_HEADER))

    _write_output_file(formatted_lines)
    _write_error_file(wrong_lines)


def _get_formatted_lines(lines: list, fields_number: int) -> (list, list):
    albums = []
    wrong_lines = []
    lines_num = len(lines)
    current_line = 0

    print(f"{FORMATTING_LINES}...")

    for line in lines:
        current_line += 1
        print(f"\r{current_line}/{lines_num}", end='')

        try:
            albums.append(Album(line, fields_number).list())
        except WrongFieldsNumberException:
            wrong_lines.append(line)

    print()

    return sorted(albums), wrong_lines


def _write_output_file(albums: list) -> None:
    if albums:
        result = [CSV_HEADER]
        result.extend(albums)
        write_csv_file(_OUTPUT_FILE, result)


def _write_error_file(errors: list) -> None:
    if errors:
        result = [CSV_HEADER]
        result.extend(errors)
        write_csv_file(_ERROR_FILE, result)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{FORMATTING} '{CSV_FILE}'...")

    lines = read_csv_file(CSV_FILE)

    if lines:
        regenerate_exceptions_dictionary()
        regenerate_artists_dictionary(lines[1:])
        _format_file(lines[1:])

    print(DONE)
