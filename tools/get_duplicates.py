#!/usr/bin/env python3

import difflib
import os
import signal
import string
from types import FrameType

CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_SEPARATOR = ','
MATCH_THRESHOLD = 0.9  # Seems a reasonable threshold


def _handle_sigint(signal: int, frame: FrameType) -> None:
    print('\rStopped')
    exit(0)


def _clear_screen():
    if 'nt' in os.name:
        os.system('cls')
    elif 'posix' in os.name:
        os.system('clear')


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


def _get_duplicates(lines: list) -> (list, list):
    duplicates = []
    possible_duplicates = []
    range_num_lines = len(lines) - 1

    for i in range(range_num_lines):
        print(f"\r{i}/{range_num_lines}", end='')
        for j in range(i + 1, range_num_lines):
            line1 = _normalize(lines[i])
            line2 = _normalize(lines[j])
            match_ratio = difflib.SequenceMatcher(None, line1, line2).ratio()

            if match_ratio > MATCH_THRESHOLD:
                duplicate = f"{lines[i]}  -> {lines[j]}"

                if match_ratio == 1:
                    duplicates.append(duplicate)
                else:
                    possible_duplicates.append(duplicate)

    return duplicates, possible_duplicates


def _normalize(line: list) -> str:
    line_ = line.split(CSV_SEPARATOR)
    artist = line_[0]
    title = line_[1]

    result = f"{artist}{title}".lower()

    for symbol in string.punctuation:
        result.replace(symbol, '')

    return result


def _print_list(name: str, lines: list):
    print(name)

    for line in lines:
        print(line, end='')

    print()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handle_sigint)
    _clear_screen()
    print(f"Looking for duplicates in {CSV_FILE}")
    lines = _read_file()
    duplicates, possible_duplicates = _get_duplicates(lines)

    if duplicates or possible_duplicates:
        if duplicates:
            _print_list('Duplicates', duplicates)

        if possible_duplicates:
            _print_list('Possible duplicates', possible_duplicates)

    else:
        print('No duplicates found.')

