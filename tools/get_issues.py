#!/usr/bin/env python3

"""
Get CSV file issues:
    - Lines with wrong fields number
    - Lines with mismatched parentheses
    - Lines with mismatched square brackets
    - Lines with mismatched quotes
    - Lines with possible publication date on title but not on its field
    - Lines with possible album format on title but not on its field

Output:
    - CSV file with lines with wrong fields number (if any)
    - CSV file with lines with mismatched parentheses (if any)
    - CSV file with lines with mismatched square brackets (if any)
    - CSV file with lines with mismatched quotes (if any)
    - CSV file with lines with possible publication date on title but not on its field (if any)
    - CSV file with lines with possible album format on title but not on its field (if any)
"""

import re
import signal

from tools.config.config import CSV_FILE, CSV_HEADER, CsvPosition, ALBUM_FORMATS, CSV_EMPTY_FIELD_VALUE
from tools.crosscutting.strings import SEARCHING_FOR_LINES_WITH_PROBLEMS_IN, DONE, NO_PROBLEMS_FOUND, ERRORS, \
    WRONG_FIELDS_NUMBER, MISMATCHED_PARENTHESES, MISMATCHED_SQUARE_BRACKETS, MISMATCHED_QUOTES, IMPROVEMENTS, \
    POSSIBLE_PUBLICATION_DATE_IN_TITLE, POSSIBLE_ALBUM_FORMAT_IN_TITLE
from tools.helpers.file_helpers import read_csv_file, write_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen
from tools.utils.string_utils import has_mismatched_parentheses, has_mismatched_square_brackets, has_mismatched_quotes

_WRONG_FIELDS_NUMBER = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{WRONG_FIELDS_NUMBER.lower()}.csv"
_MISMATCHED_PARENTHESES_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_PARENTHESES.lower()}.csv"
_MISMATCHED_SQUARE_BRACKETS_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_SQUARE_BRACKETS.lower()}.csv"
_MISMATCHED_QUOTES_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}-{MISMATCHED_QUOTES.lower()}.csv"
_POSSIBLE_PUBLICATION_DATE = f"{CSV_FILE[:-4]}-{IMPROVEMENTS.lower()}-{POSSIBLE_PUBLICATION_DATE_IN_TITLE.lower()}.csv"
_POSSIBLE_ALBUM_FORMAT = f"{CSV_FILE[:-4]}-{IMPROVEMENTS.lower()}-{POSSIBLE_ALBUM_FORMAT_IN_TITLE.lower()}.csv"
_REGEX_YEAR = r'.*\d{4}.*'


class FileIssues:
    wrong_fields_number = []
    mismatched_parentheses = []
    mismatched_square_brackets = []
    mismatched_quotes = []
    possible_publication_date = []
    possible_album_format = []

    def there_are_issues(self) -> bool:
        return (len(self.wrong_fields_number) > 0
                or len(self.mismatched_parentheses) > 0
                or len(self.mismatched_square_brackets) > 0
                or len(self.mismatched_quotes) > 0
                or len(self.possible_publication_date) > 0
                or len(self.possible_album_format) > 0)


def _get_issues(lines: list, fields_num: int) -> FileIssues:
    issues = FileIssues()

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

            if _has_possible_publication_date(line):
                issues.possible_publication_date.append(line)

            if _has_possible_album_format(line):
                issues.possible_album_format.append(line)

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


def _has_possible_publication_date(line: list) -> bool:
    publication_date = line[CsvPosition.PUBLICATION_DATE.value]

    if publication_date == '' or publication_date == CSV_EMPTY_FIELD_VALUE:
        match = re.search(_REGEX_YEAR, line[CsvPosition.ARTIST.value])

        if match:
            return True

    return False


def _has_possible_album_format(line: list) -> bool:
    album_format = line[CsvPosition.FORMAT.value]

    if album_format == '' or album_format == CSV_EMPTY_FIELD_VALUE:
        for album_format in ALBUM_FORMATS:
            if album_format in line[CsvPosition.ARTIST.value]:
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
            write_csv_file(_POSSIBLE_PUBLICATION_DATE, issues.possible_publication_date)
            write_csv_file(_POSSIBLE_ALBUM_FORMAT, issues.possible_album_format)
            print(DONE)
        else:
            print(NO_PROBLEMS_FOUND)
