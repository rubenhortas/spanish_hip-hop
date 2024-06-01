#!/usr/bin/env python

from tools.exceptions import EXCEPTIONS
from tools.libraries.config import CSV_FILE, CSV_SEPARATOR
from tools.libraries.file_helpers import read_file, write_file


def _get_lines(lines: list) -> (list, list):
    lines_with_exceptions = []
    lines_without_exceptions = []
    lower_exceptions = [exception.lower() for exception in EXCEPTIONS]

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        artist_fist_word = line_[0].split()[0]
        title_first_word = line_[1].split()[0]

        if artist_fist_word in lower_exceptions or title_first_word in lower_exceptions:
            lines_with_exceptions.append(line)
        else:
            lines_without_exceptions.append(line)

    return lines_with_exceptions, lines_without_exceptions


def _get_unused_exceptions(lines: list) -> list:
    def _find_exceptions(words: list):
        for word in words:
            if word in EXCEPTIONS and word not in used_exceptions:
                used_exceptions.add(word)

    unused_exceptions = []
    used_exceptions = set()

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        _find_exceptions(line_[0].lower().split())
        _find_exceptions(line_[1].lower().split())

    for k in EXCEPTIONS:
        if k not in used_exceptions:
            unused_exceptions.append(f"{k}\n")

    return unused_exceptions


if __name__ == '__main__':
    lines = read_file(CSV_FILE)[1:]
    lines_with_exceptions, lines_without_exceptions = _get_lines(lines)
    unused_exceptions = _get_unused_exceptions(lines)

    write_file('lines_with_exceptions.txt', lines_with_exceptions)
    write_file('lines_without_exceptions.txt', lines_without_exceptions)
    write_file('unused_exceptions.txt', unused_exceptions)
