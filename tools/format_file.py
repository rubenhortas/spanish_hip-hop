#!/usr/bin/env python3
import signal

from tools.config.config import CSV_FILE
from tools.crosscutting.strings import FORMATTING_LINES, GENERATING, DONE, FORMATTED, ERRORS, WRONG_FIELDS_NUMBER
from tools.domain.album import Album, WrongFieldsNumberException
from tools.helpers.file_helpers import read_csv_file, write_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen

_OUTPUT_FILE = f"{CSV_FILE[:-4]}-{FORMATTED.lower()}.csv"
_ERROR_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{WRONG_FIELDS_NUMBER}.csv"


def _get_formatted_lines(lines: list, fields_number: int) -> (list, list):
    albums = []
    wrong_lines = []
    num_lines = len(lines)
    current_line = 0

    print(f"{FORMATTING_LINES}...")

    for line in lines:
        current_line += 1
        print(f"\r{current_line}/{num_lines}", end='')

        try:
            albums.append(Album(line, fields_number).list())
        except WrongFieldsNumberException:
            wrong_lines.append(line)

    print()

    return sorted(albums), wrong_lines


def _write_output_file(header: list, albums: list) -> None:
    if albums:
        result = [header]
        result.extend(albums)
        write_csv_file(_OUTPUT_FILE, result)


def _write_error_file(header: list, errors: list) -> None:
    if errors:
        result = [header]
        result.extend(errors)
        write_csv_file(_ERROR_FILE, result)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{GENERATING} '{_OUTPUT_FILE}'...")

    lines = read_csv_file(CSV_FILE)

    if lines:
        header = lines[0]
        formatted_lines, wrong_lines = _get_formatted_lines(lines[1:], len(header))

        _write_output_file(header, formatted_lines)
        _write_error_file(header, wrong_lines)

    print(DONE)
