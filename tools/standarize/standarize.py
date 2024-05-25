#!/usr/bin/env python3

import os
import signal
from types import FrameType

from tools.capitalize.Album import Album

CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_SEPARATOR = ','


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
        album = Album(entry_[0], entry_[1], entry_[2], entry_[3], CSV_SEPARATOR)
        formatted_entries.append(f"{str(album)}\n")

    # TODO: Sort list by artist/year/title before return
    return formatted_entries


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


def _write_output_file(file: str, lines: list) -> None:
    try:
        with open(file, 'w') as f:
            f.writelines(lines)
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{file}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{file}' OSError: {os_error}")
        exit(-1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handle_sigint)
    _clear_screen()
    formatted_entries = _format_entries()
    _write_output_file('new.csv', formatted_entries)
