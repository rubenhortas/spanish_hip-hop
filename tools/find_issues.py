#!/usr/bin/env python3

from collections import Counter

from tools.libraries.config import CSV_HEADER, CSV_SEPARATOR, CSV_FILE
from tools.libraries.file_helpers import read_file


def _get_issues(lines):
    expected_separators = Counter(CSV_HEADER)[CSV_SEPARATOR]
    extra_separators = []
    parentheses_issues = []

    for line in lines:
        line_counter = Counter(line)

        if line_counter[CSV_SEPARATOR] > expected_separators:
            extra_separators.append(line)

        if line_counter['('] != line_counter[')']:
            parentheses_issues.append(line)

    return extra_separators, parentheses_issues


def _print_list(name: str, lines: list) -> None:
    print(f"{name}:\n")

    for line in lines:
        print(line.strip())


if __name__ == '__main__':
    lines = read_file(CSV_FILE)[1:]
    extra_separators, parentheses_issues = _get_issues(lines)

    if extra_separators or parentheses_issues:
        if extra_separators:
            _print_list('Lines with extra separators:\n', extra_separators)
            print()

        if parentheses_issues:
            _print_list('Lines with parentheses issues:\n', parentheses_issues)
    else:
        print('No issues found.')
