#!/usr/bin/env python

from tools.exceptions import EXCEPTIONS
from tools.libraries.album import Album
from tools.libraries.config import CSV_FILE, CSV_SEPARATOR
from tools.libraries.file_helpers import read_file, write_file


def _get_albums(lines: list) -> list:
    albums = []

    for line in lines:
        line_ = line.strip().split(CSV_SEPARATOR)
        artist = line_[0]
        title = line_[1]
        publication_date = line_[2]
        format_ = line_[3]

        album = Album(artist, title, publication_date, format_)
        albums.append(album)

    return albums


def _get_lines(lines: list, albums: list) -> (list, list):
    lines_with_exceptions = []
    lines_without_exceptions = []

    for line, album in zip(lines, albums):
        line_ = line.split(CSV_SEPARATOR)
        line_artist = line_[0]
        line_title = line_[1]

        if line_artist != album.artist or line_title != album.title:
            data = f"'{line_artist}{CSV_SEPARATOR}{line_title}'"
            formatted_data = f"'{album.artist}{CSV_SEPARATOR}{album.title}'"
            lines_with_exceptions.append(f"{data} -> {formatted_data}\n")
        else:
            lines_without_exceptions.append(line)

    return lines_with_exceptions, lines_without_exceptions


def _get_unused_exceptions(albums: list) -> list:
    def _find_exceptions(words: list):
        for word in words:
            if word in EXCEPTIONS and word not in used_exceptions:
                used_exceptions.add(word)

    unused_exceptions = []
    used_exceptions = set()

    for album in albums:
        _find_exceptions(album.artist.lower().split())
        _find_exceptions(album.title.lower().split())

    for k in EXCEPTIONS:
        if k not in used_exceptions:
            unused_exceptions.append(f"{k}\n")

    return unused_exceptions


if __name__ == '__main__':
    lines = read_file(CSV_FILE)[1:]
    albums = _get_albums(lines)
    lines_with_exceptions, lines_without_exceptions = _get_lines(lines, albums)
    unused_exceptions = _get_unused_exceptions(albums)

    write_file('lines_with_exceptions.txt', lines_with_exceptions)
    write_file('lines_without_exceptions.txt', lines_without_exceptions)
    write_file('unused_exceptions.txt', unused_exceptions)
