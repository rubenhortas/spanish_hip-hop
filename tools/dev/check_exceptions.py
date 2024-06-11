#!/usr/bin/env python
from tools.libraries.exceptions import EXCEPTIONS
from tools.libraries.config import CSV_FILE, CSV_SEPARATOR, CsvPosition
from tools.helpers.file_helpers import read_file, write_file
from tools.utils.string_utils import replace_exceptions

_LINES_WITH_EXCEPTIONS_FILE = 'excepciones - lineas con excepciones.txt'
_LINES_WITHOUT_EXCEPTIONS_FILE = 'excepciones - lineas sin excepciones.txt'
_UNUSED_EXCEPTIONS_FILE = 'excepciones - excepciones sin usar.txt'


def _get_lines(lines: list) -> (list, list):
    lines_with_exceptions = []
    lines_without_exceptions = []

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        artist = line_[CsvPosition.ARTIST.value]
        title = line_[CsvPosition.TITLE.value]
        formatted_artist = replace_exceptions(artist)
        formated_title = replace_exceptions(title)

        if artist != formatted_artist or title != formated_title:
            data = f"'{artist}{CSV_SEPARATOR}{title}'"
            formatted_data = f"'{formatted_artist}{CSV_SEPARATOR}{formated_title}'"
            lines_with_exceptions.append(f"{data} -> {formatted_data}\n")
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
        _find_exceptions(line_[CsvPosition.ARTIST.value].lower().split())
        _find_exceptions(line_[CsvPosition.TITLE.value].lower().split())

    for k in EXCEPTIONS:
        if k not in used_exceptions:
            unused_exceptions.append(f"{k}\n")

    return unused_exceptions


if __name__ == '__main__':
    lines = read_file(CSV_FILE)[1:]
    lines_with_exceptions, lines_without_exceptions = _get_lines(lines)
    unused_exceptions = _get_unused_exceptions(lines)

    write_file(_LINES_WITH_EXCEPTIONS_FILE, lines_with_exceptions)
    write_file(_LINES_WITHOUT_EXCEPTIONS_FILE, lines_without_exceptions)
    write_file(_UNUSED_EXCEPTIONS_FILE, unused_exceptions)
