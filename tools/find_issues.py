#!/usr/bin/env python3

import signal
from collections import Counter

from tools.libraries.config import CSV_SEPARATOR, CSV_FILE, SEPARATOR_NUMBER
from tools.libraries.file_helpers import read_file
from tools.libraries.os_helpers import handle_sigint, clear_screen


def _get_issues(lines):
    bad_formatted = []
    mismatched_parentheses = []

    for line in lines:
        line_counter = Counter(line)

        if not _has_correct_number_separators(line_counter):
            bad_formatted.append(line)

        if _has_mismatched_parentheses(line, line_counter):
            mismatched_parentheses.append(line)

    return bad_formatted, mismatched_parentheses


def _has_correct_number_separators(line_counter: Counter):
    return line_counter[CSV_SEPARATOR] == SEPARATOR_NUMBER


def _has_mismatched_parentheses(line: str, line_counter: Counter) -> bool:
    def has_mismatched_parentheses(counter: Counter) -> bool:
        if counter['('] != counter[')']:
            return True

        return False

    if has_mismatched_parentheses(line_counter):
        return True
    else:
        words = line.split()

        for word in words:
            if has_mismatched_parentheses(Counter(word)):
                return True

    return False


def _print_list(name: str, lines: list) -> None:
    if list:
        print(f"{name}:\n")

        for line in lines:
            print(line, end='')

        print()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Finding lines with issues in {CSV_FILE}...")

    lines = read_file(CSV_FILE)[1:]
    extra_separators, parentheses_issues = _get_issues(lines)

    if extra_separators or parentheses_issues:
        _print_list('Bad formatted lines (extra separators)', extra_separators)
        _print_list('Lines with mismatched parentheses', parentheses_issues)
    else:
        print('No issues found.')
