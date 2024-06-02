#!/usr/bin/env python3

import signal
from collections import Counter

from tools.libraries.config import CSV_SEPARATOR, CSV_FILE, SEPARATOR_NUMBER
from tools.libraries.file_helpers import read_file, write_file
from tools.libraries.os_helpers import handle_sigint, clear_screen

_EXTRA_SEPARATORS_FILE = 'errores - separadores extra.txt'
_MISMATCHED_PARENTHESES_FILE = 'errores - parentesis.txt'
_MISMATCHED_SQUARE_BRACKETS_FILE = 'errores - corchetes.txt'


def _get_issues(lines) -> (list, list, list):
    bad_formatted = []
    mismatched_parentheses = []
    mismatched_square_brackets = []

    for line in lines:
        line_counter = Counter(line)

        if not _has_correct_number_separators(line_counter):
            bad_formatted.append(line)

        if _has_mismatched_symbols(line, line_counter, '(', ')'):
            mismatched_parentheses.append(line)

        if _has_mismatched_symbols(line, line_counter, '[', ']'):
            mismatched_square_brackets.append(line)

    return bad_formatted, mismatched_parentheses, mismatched_square_brackets


def _has_correct_number_separators(line_counter: Counter):
    return line_counter[CSV_SEPARATOR] == SEPARATOR_NUMBER


def _has_mismatched_symbols(line: str, line_counter: Counter, left_symbol: str, right_symbol: str) -> bool:
    def has_mismatched_symbols(counter: Counter) -> bool:
        if counter[left_symbol] != counter[right_symbol]:
            return True

        return False

    if has_mismatched_symbols(line_counter):
        return True
    else:
        fields = line.split(CSV_SEPARATOR)

        for field in fields:
            if has_mismatched_symbols(Counter(field)):
                return True

    return False


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Finding lines with issues in {CSV_FILE}...")

    lines = read_file(CSV_FILE)[1:]
    extra_separators, mismatched_parentheses, mismatched_square_brackets = _get_issues(lines)

    if extra_separators or mismatched_parentheses or mismatched_square_brackets:
        if extra_separators:
            write_file(_EXTRA_SEPARATORS_FILE, extra_separators)

        if mismatched_parentheses:
            write_file(_MISMATCHED_PARENTHESES_FILE, mismatched_parentheses)

        if mismatched_square_brackets:
            write_file(_MISMATCHED_SQUARE_BRACKETS_FILE, mismatched_square_brackets)

        print('Done')
    else:
        print('No issues found.')
