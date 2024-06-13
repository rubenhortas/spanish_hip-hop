#!/usr/bin/env python3
import signal
from collections import Counter

from tools.config.config import CSV_SEPARATOR, CSV_FILE, SEPARATOR_NUMBER
from tools.crosscutting.strings import SEARCHING_FOR_LINES_WITH_PROBLEMS_IN, DONE, NO_PROBLEMS_FOUND, ERRORS, \
    WRONG_SEPARATORS_NUMBER, MISMATCHED_PARENTHESES, MISMATCHED_SQUARE_BRACKETS
from tools.helpers.file_helpers import read_file, write_file
from tools.helpers.os_helpers import handle_sigint, clear_screen

_WRONG_SEPARATORS_NUMBER = f"{ERRORS}-{WRONG_SEPARATORS_NUMBER}.txt"
_MISMATCHED_PARENTHESES_FILE = f"{ERRORS}-{MISMATCHED_PARENTHESES}.txt"
_MISMATCHED_SQUARE_BRACKETS_FILE = f"{ERRORS}-{MISMATCHED_SQUARE_BRACKETS}.txt"


def _get_issues(lines) -> (list, list, list):
    wrong_separators_number = []
    mismatched_parentheses = []
    mismatched_square_brackets = []

    for line in lines:
        line_counter = Counter(line)

        if not _has_correct_number_separators(line_counter):
            wrong_separators_number.append(line)

        if _has_mismatched(line, line_counter, '(', ')'):
            mismatched_parentheses.append(line)

        if _has_mismatched(line, line_counter, '[', ']'):
            mismatched_square_brackets.append(line)

    return wrong_separators_number, mismatched_parentheses, mismatched_square_brackets


def _has_correct_number_separators(line_counter: Counter):
    return line_counter[CSV_SEPARATOR] == SEPARATOR_NUMBER


def _has_mismatched(line: str, line_counter: Counter, left_symbol: str, right_symbol: str) -> bool:
    def has_mismatched_symbols(counter: Counter) -> bool:
        if counter[left_symbol] != counter[right_symbol]:
            return True

        return False

    if has_mismatched_symbols(line_counter):
        return True
    else:
        values = line.split(CSV_SEPARATOR)

        for value in values:
            if has_mismatched_symbols(Counter(value)):
                return True

    return False


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{SEARCHING_FOR_LINES_WITH_PROBLEMS_IN} '{CSV_FILE}'...")

    lines = read_file(CSV_FILE)[1:]
    wrong_separators_number, mismatched_parentheses, mismatched_square_brackets = _get_issues(lines)

    if wrong_separators_number or mismatched_parentheses or mismatched_square_brackets:
        write_file(_WRONG_SEPARATORS_NUMBER, wrong_separators_number)
        write_file(_MISMATCHED_PARENTHESES_FILE, mismatched_parentheses)
        write_file(_MISMATCHED_SQUARE_BRACKETS_FILE, mismatched_square_brackets)
        print(DONE)
    else:
        print(NO_PROBLEMS_FOUND)
