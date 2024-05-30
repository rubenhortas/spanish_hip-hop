#!/usr/bin/env python
from tools.exceptions import EXCEPTIONS
from tools.libraries.config import CSV_FILE, CSV_SEPARATOR
from tools.libraries.file_helpers import read_file, write_file


def _format(string: str) -> (bool, str):
    result = string.strip().capitalize()
    string_ = result.split()
    used_exception = False

    for word in string_:
        if word.lower() in EXCEPTIONS:
            used_exception = True
            used_exceptions.add(word.lower())
            result = result.replace(word, EXCEPTIONS[word.lower()])

    return used_exception, result


if __name__ == '__main__':
    lines = read_file(CSV_FILE)[1:]
    lines_with_exceptions = []
    lines_without_exceptions = []
    used_exceptions = set()
    unused_exceptions = []

    for line in lines:
        line_ = line.strip().split(CSV_SEPARATOR)
        artist = line_[0]
        title = line_[1]
        artist_has_exceptions, formatted_artist = _format(artist)
        title_has_exceptions, formatted_title = _format(title)

        if artist_has_exceptions or title_has_exceptions:
            data = f"'{artist}{CSV_SEPARATOR}{title}'"
            formatted_data = f"'{formatted_artist}{CSV_SEPARATOR}{formatted_title}'"
            lines_with_exceptions.append(f"{data} -> {formatted_data}\n")
        else:
            lines_without_exceptions.append(line)

    for k in EXCEPTIONS:
        if k not in used_exceptions:
            unused_exceptions.append(f"{k}\n")

    write_file('lines_with_exceptions.txt', lines_with_exceptions)
    write_file('lines_without_exceptions.txt', lines_without_exceptions)
    write_file('unused_exceptions.txt', unused_exceptions)
