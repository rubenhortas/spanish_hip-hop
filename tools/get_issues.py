#!/usr/bin/env python3
import signal

from tools.config.config import CSV_FILE, CSV_HEADER
from tools.crosscutting.strings import SEARCHING_FOR_LINES_WITH_PROBLEMS_IN, DONE, NO_PROBLEMS_FOUND, ERRORS, \
    WRONG_FIELDS_NUMBER, MISMATCHED_PARENTHESES, MISMATCHED_SQUARE_BRACKETS, MISMATCHED_QUOTES
from tools.helpers.file_helpers import read_csv_file, write_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen
from tools.utils.string_utils import has_mismatched_parentheses, has_mismatched_square_brackets, has_mismatched_quotes

_WRONG_FIELDS_NUMBER = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{WRONG_FIELDS_NUMBER.lower()}.csv"
_MISMATCHED_PARENTHESES_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_PARENTHESES.lower()}.csv"
_MISMATCHED_SQUARE_BRACKETS_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_SQUARE_BRACKETS.lower()}.csv"
_MISMATCHED_QUOTES_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_QUOTES.lower()}.csv"


class _FileIssues:
    wrong_fields_number: []
    mismatched_parentheses = []
    mismatched_square_brackets = []
    mismatched_quotes = []

    def __init__(self):
        self.wrong_fields_number = []
        self.mismatched_parentheses = []
        self.mismatched_square_brackets = []
        self.mismatched_quotes = []

    def there_are_issues(self) -> bool:
        return (len(self.wrong_fields_number) > 0
                or len(self.mismatched_parentheses) > 0
                or len(self.mismatched_square_brackets) > 0
                or len(self.mismatched_quotes) > 0)


def _get_issues(lines: list, fields_num: int) -> _FileIssues:
    issues = _FileIssues()

    for line in lines:
        if line:
            if len(line) != fields_num:
                issues.wrong_fields_number.append(line)

            if _has_mismatched_parentheses(line):
                issues.mismatched_parentheses.append(line)

            if _has_mismatched_square_brackets(line):
                issues.mismatched_square_brackets.append(line)

            if _has_mismatched_quotes(line):
                issues.mismatched_quotes.append(line)

    return issues


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


def _has_mismatched_quotes(line: list) -> bool:
    for value in line:
        if has_mismatched_quotes(value):
            return True

    return False


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{SEARCHING_FOR_LINES_WITH_PROBLEMS_IN} '{CSV_FILE}'...")

    lines = read_csv_file(CSV_FILE)[1:]

    if lines:
        issues = _get_issues(lines, len(CSV_HEADER))

        if issues.there_are_issues():
            write_csv_file(_WRONG_FIELDS_NUMBER, issues.wrong_fields_number)
            write_csv_file(_MISMATCHED_PARENTHESES_FILE, issues.mismatched_parentheses)
            write_csv_file(_MISMATCHED_SQUARE_BRACKETS_FILE, issues.mismatched_square_brackets)
            write_csv_file(_MISMATCHED_QUOTES_FILE, issues.mismatched_quotes)
            print(DONE)
        else:
            print(NO_PROBLEMS_FOUND)
