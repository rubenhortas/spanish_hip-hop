#!/usr/bin/env python3
import signal

from tools.config.config import CSV_FILE, CSV_HEADER, CSV_DELIMITER
from tools.crosscutting.strings import SEARCHING_FOR_LINES_WITH_PROBLEMS_IN, DONE, NO_PROBLEMS_FOUND, ERRORS, \
    WRONG_FIELDS_NUMBER, MISMATCHED_PARENTHESES, MISMATCHED_SQUARE_BRACKETS
from tools.helpers.file_helpers import read_csv_file, write_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen
from tools.utils.string_utils import has_mismatched_parentheses, has_mismatched_square_brackets

_WRONG_FIELDS_NUMBER = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{WRONG_FIELDS_NUMBER}.csv"
_MISMATCHED_PARENTHESES_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_PARENTHESES}.csv"
_MISMATCHED_SQUARE_BRACKETS_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_SQUARE_BRACKETS}.csv"

_issues = {
    'wrong_fields_number': [],
    'mismatched_parentheses': [],
    'mismatched_square_brackets': []
}


def _get_issues(lines: list, fields_num: int) -> None:
    for line in lines:
        if line:
            if len(line) != fields_num:
                _issues['wrong_fields_number'].append(line)

            if _has_mismatched_parentheses(line):
                _issues['mismatched_parentheses'].append(line)

            if _has_mismatched_square_brackets(line):
                _issues['mismatched_square_brackets'].append(line)


def _has_mismatched_parentheses(line: list) -> bool:
    for value in line:
        if has_mismatched_parentheses(value):
            return True

    return False


def _has_mismatched_square_brackets(line: list) -> bool:
    for value in line:
        if has_mismatched_square_brackets(value):
            return True

    return False


def there_are_issues() -> bool:
    return (_issues['wrong_fields_number'] is not None or _issues['mismatched_parentheses'] is not None
            or _issues['mismatched_square_brackets'] is not None)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{SEARCHING_FOR_LINES_WITH_PROBLEMS_IN} '{CSV_FILE}'...")

    lines = read_csv_file(CSV_FILE)[1:]

    if lines:
        _get_issues(lines, len(CSV_HEADER))

        if there_are_issues():
            write_csv_file(_WRONG_FIELDS_NUMBER, _issues['wrong_fields_number'])
            write_csv_file(_MISMATCHED_PARENTHESES_FILE, _issues['mismatched_parentheses'])
            write_csv_file(_MISMATCHED_SQUARE_BRACKETS_FILE, _issues['mismatched_square_brackets'])
            print(DONE)
        else:
            print(NO_PROBLEMS_FOUND)
