#!/usr/bin/env python3
import signal

from tools.crosscutting.strings import FORMATTING_LINES, REPLACING_ARTISTS_IN_TITLES, \
    POORLY_FORMATTED_LINES_INVALID_NUMBER_OF_SEPARATORS, GENERATING, DONE, FORMATTED, ERRORS
from tools.domain.album import Album, WrongSeparatorsException
from tools.config.config import CSV_FILE, CSV_HEADER
from tools.helpers.file_helpers import write_file, read_file
from tools.helpers.os_helpers import handle_sigint, clear_screen

_OUTPUT_FILE = f"{CSV_FILE[:-4]}-{FORMATTED.lower()}.csv"
_ERROR_FILE = f"{CSV_FILE[:-4]}-{ERRORS.lower()}.csv"


def _get_formatted_lines(line: list) -> (list, list):
    lines_ = [line.strip() for line in line]
    len_lines = len(lines_)
    albums = []
    errors = []
    artists = set()
    current_line = 0

    print(f"{FORMATTING_LINES}...")

    for line in lines_:
        current_line += 1

        print(f"\r{current_line}/{len_lines}", end='')

        try:
            album = Album(line)

            for artist in album.get_artists():
                if artist:
                    artists.add(artist)

            albums.append(album)
        except WrongSeparatorsException:
            errors.append(line)

    print()

    _replace_artists_in_titles(albums, list(artists))

    return sorted(albums), errors


def _replace_artists_in_titles(albums: list, artists: list) -> None:
    len_albums = len(albums)
    current_album = 0

    print(f"{REPLACING_ARTISTS_IN_TITLES}...")

    for album in albums:
        current_album += 1

        print(f"\r{current_album}/{len_albums}", end='')

        title = album.title.split()

        for artist in artists:
            artist_ = artist.split()
            artist_in_title = True

            for word in artist_:
                if word.lower() not in title:
                    artist_in_title = False
                    break

            if artist_in_title:
                for word in artist_:
                    album.title = album.title.replace(word.lower(), word)

    print()


def _write_output_file(albums: list) -> None:
    if albums:
        result = [f"{CSV_HEADER}\n"]
        result.extend([f"{str(album)}\n" for album in albums])
        write_file(_OUTPUT_FILE, result)


def _write_error_file(errors: list) -> None:
    if errors:
        result = [f"{POORLY_FORMATTED_LINES_INVALID_NUMBER_OF_SEPARATORS}:\n\n"]
        result.extend([f"{error}\n" for error in errors])
        write_file(_ERROR_FILE, result)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{GENERATING} '{_OUTPUT_FILE}'...")

    lines = read_file(CSV_FILE)[1:]
    formatted_lines, errors = _get_formatted_lines(lines)

    _write_output_file(formatted_lines)
    _write_error_file(errors)

    print(DONE)
