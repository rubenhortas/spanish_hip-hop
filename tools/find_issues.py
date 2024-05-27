#!/usr/bin/env python3

from collections import Counter

CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_SEPARATOR = ','


def _get_issues(lines):
    extra_separators = []
    parentheses_issues = []

    for line in lines:
        line_counter = Counter(line)

        if line_counter[CSV_SEPARATOR] > 3:
            extra_separators.append(line)

        if line_counter['('] != line_counter[')']:
            parentheses_issues.append(line)

    return extra_separators, parentheses_issues


def _print_list(name: str, lines: list) -> None:
    print(f"{name}:\n")

    for line in lines:
        print(line.strip())


if __name__ == '__main__':
    try:
        with open(CSV_FILE, 'r') as f:
            lines = f.readlines()

        extra_separators, parentheses_issues = _get_issues(lines)

        if extra_separators or parentheses_issues:
            if extra_separators:
                _print_list('Lines with extra separators:\n', extra_separators)
                print()

            if parentheses_issues:
                _print_list('Lines with parentheses issues:\n', parentheses_issues)
        else:
            print('No issues found.')
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{CSV_FILE}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{CSV_FILE}' OSError: {os_error}")
        exit(-1)
