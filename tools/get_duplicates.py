#!/usr/bin/env python3

import difflib
import os
import signal
import string
from types import FrameType

CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_SEPARATOR = ','
OUTPUT_FILE = 'duplicados.txt'
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
    normalized_lines = []
    duplicates = []
    possible_duplicates = []

    for line in lines:
        normalized_lines.append((line, _normalize(line)))

    num_lines = len(normalized_lines)

    for i in range(num_lines):
        print(f"\r{i + 1}/{num_lines}", end='')

        for j in range(i + 1, num_lines):
            match_ratio = difflib.SequenceMatcher(None, normalized_lines[i][1], normalized_lines[j][1]).ratio()

            if match_ratio > MATCH_THRESHOLD:
                duplicate = f"{normalized_lines[i][0].strip()}  -> {normalized_lines[j][0]}"

                if match_ratio == 1:
                    duplicates.append(duplicate)
                else:
                    possible_duplicates.append(duplicate)

                break

    return duplicates, possible_duplicates


def _normalize(line: str) -> str:
    line_ = line.split(CSV_SEPARATOR)
    artist = line_[0]
    title = line_[1]

    result = f"{artist}{title}".lower().replace(' ', '')

    for symbol in string.punctuation:
        result = result.replace(symbol, '')

    return result


def _write_output_file(lines: list) -> None:
    try:
        with open(OUTPUT_FILE, 'w') as f:
            f.writelines(lines)
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{OUTPUT_FILE}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{OUTPUT_FILE}' OSError: {os_error}")
        exit(-1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handle_sigint)
    _clear_screen()
    print(f"Looking for duplicates in {CSV_FILE}")
    lines = _read_file()[1:]
    duplicates, possible_duplicates = _get_duplicates(lines)

    if duplicates or possible_duplicates:
        issues = []

        if duplicates:
            issues.append('Duplicates:\n\n')
            issues.extend(duplicates)
            issues.append('\n')

        if possible_duplicates:
            issues.append('Possible duplicates:\n\n')
            issues.extend(possible_duplicates)

        _write_output_file(issues)
        print('\nDone')
    else:
        print('No duplicates found.')
