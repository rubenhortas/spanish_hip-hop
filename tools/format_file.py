#!/usr/bin/env python3

import os
import signal
from tools.exception import EXCEPTIONS
from types import FrameType

CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_HEADER = 'Artista,Trabajo,Fecha Publicación,Tipo'
CSV_SEPARATOR = ','
CSV_OUTPUT_FILE = f"{CSV_FILE[:-4]} - formateado.csv"


class Album:
    def __init__(self, artist: str, title: str, publication_date: str, album_format: str):
        self._format_artist(artist)
        self._format_title(title)
        self.publication_date = publication_date.strip()
        self.format = album_format.strip().upper()

    def __str__(self):
        return f"{self.artist}{CSV_SEPARATOR}{self.title}{CSV_SEPARATOR}{self.publication_date}{CSV_SEPARATOR}{self.format}"

    def list(self):
        return [self.artist, self.title, self.publication_date, self.format]

    def _format_artist(self, artist: str) -> None:
        self.artist = artist.title().strip()
        artist = self.artist.split()

        for word in artist:
            if word.lower() in EXCEPTIONS:
                self.artist = self.artist.replace(word, EXCEPTIONS[word.lower()])

    def _format_title(self, title: str) -> None:
        self.title = title.capitalize().strip()
        title = self.title.split()

        for word in title:
            if word.lower() in EXCEPTIONS:
                self.title = self.title.replace(word, EXCEPTIONS[word.lower()])


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
    entry_num = 1
    entries_num = len(original_entries)

    for entry in original_entries:
        print(f"\r{entry_num}/{entries_num}", end='')

        try:
            entry_ = entry.split(CSV_SEPARATOR)
            album = Album(entry_[0], entry_[1], entry_[2], entry_[3])  # artist, title, date, format
            formatted_entries.append(album.list())

            # Debug
            # if entry_[0] != album.artist or entry_[1] != album.title:
            #     print(f": '{entry_[0]},{entry_[1]}' -> '{album.artist},{album.title}'")
        except IndexError:
            print(f"'{entry}: bad format")

        entry_num += 1

    print()

    sorted_formatted_entries = sorted(formatted_entries, key=lambda entry: (entry[0], entry[2], entry[1]))
    result = [f"{CSV_HEADER}\n"]
    result.extend([f"{CSV_SEPARATOR.join(e)}\n" for e in sorted_formatted_entries])

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
    print(f"Generating {CSV_OUTPUT_FILE}")
    formatted_entries = _format_entries()
    _write_output_file(formatted_entries)
    print('Done')
