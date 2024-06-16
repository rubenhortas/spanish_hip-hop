#!/usr/bin/env python3
import signal

from tools.config.config import CSV_FILE
from tools.crosscutting.strings import SEARCHING_FOR_LINES_WITH_PROBLEMS_IN, DONE, NO_PROBLEMS_FOUND, ERRORS, \
    WRONG_FIELDS_NUMBER, MISMATCHED_PARENTHESES, MISMATCHED_SQUARE_BRACKETS
from tools.helpers.file_helpers import read_csv_file, write_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen
from tools.utils.string_utils import has_mismatched_parentheses, has_mismatched_square_brackets

_WRONG_FIELDS_NUMBER = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{WRONG_FIELDS_NUMBER}.csv"
_MISMATCHED_PARENTHESES_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_PARENTHESES}.csv"
_MISMATCHED_SQUARE_BRACKETS_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_SQUARE_BRACKETS}.csv"


def _get_issues(lines, num_fields) -> (list, list, list):
    wrong_fields_number = []
    mismatched_parentheses = []
    mismatched_square_brackets = []

    for line in lines:
        if len(line) != num_fields:
            wrong_fields_number.append(line)

        if _has_mismatched_parentheses(line):
            mismatched_parentheses.append(line)

        if _has_mismatched_square_brackets(line):
            mismatched_square_brackets.append(line)

    return wrong_fields_number, mismatched_parentheses, mismatched_square_brackets


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


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{SEARCHING_FOR_LINES_WITH_PROBLEMS_IN} '{CSV_FILE}'...")

    lines = read_csv_file(CSV_FILE)
    if lines:
        csv_header = lines[0]
        wrong_fields_number_lines, mismatched_parentheses_lines, mismatched_square_brackets_lines = _get_issues(lines, len(csv_header))

        if wrong_fields_number_lines or mismatched_parentheses_lines or mismatched_square_brackets_lines:
            write_csv_file(_WRONG_FIELDS_NUMBER, wrong_fields_number_lines)
            write_csv_file(_MISMATCHED_PARENTHESES_FILE, mismatched_parentheses_lines)
            write_csv_file(_MISMATCHED_SQUARE_BRACKETS_FILE, mismatched_square_brackets_lines)
            print(DONE)
        else:
            print(NO_PROBLEMS_FOUND)
