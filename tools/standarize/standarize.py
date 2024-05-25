#!/usr/bin/env python3

import os
import signal
from exceptions import Artist, Title
from types import FrameType

CSV_HEADER = 'Artista,Trabajo,Fecha Publicación,Tipo'
CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_OUTPUT_FILE = f"{CSV_FILE[:-4]} - formateado.csv"
CSV_SEPARATOR = ','


class Album:
    artist_exceptions = Artist.EXCEPTIONS
    title_exceptions = Title.EXCEPTIONS

    def __init__(self, artist: str, title: str, publication_date: str, album_format: str, csv_separator: str):
        self._format_artist(artist)
        self._format_title(title)
        self.publication_date = publication_date
        self.format = album_format
        self.csv_separator = csv_separator

    def __str__(self):
        return f"{self.artist}{self.csv_separator}{self.title}{self.csv_separator}{self.publication_date}{self.csv_separator}{self.format}"

    def list(self):
        return [self.artist, self.title, self.publication_date, self.format]

    def _format_artist(self, artist: str) -> None:
        self.artist = artist.title()

        for word in self.artist:
            if word in self.artist_exceptions:
                self.artist.replace(word, self.artist_exceptions[word])

    def _format_title(self, title: str) -> None:
        self.title = title.capitalize()

        for word in self.title:
            if word in self.title_exceptions:
                self.title.replace(word, self.title_exceptions[word])


def _handle_sigint(signal: int, frame: FrameType) -> None:
    print('\rStopped')
    exit(0)


def _clear_screen() -> None:
    if 'nt' in os.name:
        os.system('cls')
    elif 'posix' in os.name:
        os.system('clear')


def _format_entries() -> list:
    original_entries = [line.strip() for line in _read_file()][1:]
    formatted_entries = []

    for entry in original_entries:
        entry_ = entry.split(CSV_SEPARATOR)
        album = Album(entry_[0], entry_[1], entry_[2], entry_[3], CSV_SEPARATOR)  # artist, title, date, format
        formatted_entries.append(album.list())

    sorted_formatted_entries = sorted(formatted_entries, key=lambda album: (album[0], album[2], album[1]))
    result = [f"{CSV_SEPARATOR.join(e)}\n" for e in sorted_formatted_entries]
    result.insert(0, f"{CSV_HEADER}\n")

    return result


def _read_file() -> list:
    try:
        with open(CSV_FILE, 'r') as f:
            return f.readlines()
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{CSV_FILE}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{CSV_FILE}' OSError: {os_error}")
        exit(-1)


def _write_output_file(lines: list) -> None:
    try:
        with open(CSV_OUTPUT_FILE, 'w') as f:
            f.writelines(lines)
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{CSV_OUTPUT_FILE}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{CSV_OUTPUT_FILE}' OSError: {os_error}")
        exit(-1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handle_sigint)
    _clear_screen()
    formatted_entries = _format_entries()
    _write_output_file(formatted_entries)
