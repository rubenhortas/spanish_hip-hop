#!/usr/bin/env python3

import difflib
import signal
import string

from tools.libraries.config import CSV_FILE, CSV_SEPARATOR
from tools.libraries.file_helpers import read_file, write_file
from tools.libraries.os_helpers import handle_sigint, clear_screen

_OUTPUT_FILE = 'duplicados.txt'
_MATCH_THRESHOLD = 0.9  # Seems a reasonable threshold


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

            if match_ratio > _MATCH_THRESHOLD:
                duplicate = f"{normalized_lines[i][0].strip()}  -> {normalized_lines[j][0]}"

                if match_ratio == 1:
                    duplicates.append(duplicate)
                else:
                    possible_duplicates.append(duplicate)

                break

    return duplicates, possible_duplicates


def _normalize(line: str) -> str:
    line_ = line.split(CSV_SEPARATOR)
    artist = line_[1]
    title = line_[2]

    result = f"{artist}{title}".lower().replace(' ', '')

    for symbol in string.punctuation:
        result = result.replace(symbol, '')

    return result


def _write_output_file(duplicates: list, possible_duplicates: list) -> None:
    issues = []

    if duplicates:
        issues.append('Duplicates:\n\n')
        issues.extend(duplicates)
        issues.append('\n')

    if possible_duplicates:
        issues.append('Possible duplicates:\n\n')
        issues.extend(possible_duplicates)
        issues.append('\n')

    write_file(_OUTPUT_FILE, issues)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Looking for duplicates in {CSV_FILE}")

    lines = read_file(CSV_FILE)[1:]
    duplicates, possible_duplicates = _get_duplicates(lines)

    if duplicates or possible_duplicates:
        _write_output_file(duplicates, possible_duplicates)
        print('Done')
    else:
        print('No duplicates found.')
