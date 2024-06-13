#!/usr/bin/env python3
import difflib
import signal

from tools.config.config import CSV_FILE
from tools.crosscutting.strings import DONE, DUPLICATES, POSSIBLE_DUPLICATES, NO_DUPLICATES_FOUND, \
    LOOKING_FOR_DUPLICATES_IN
from tools.domain.album import Album
from tools.helpers.file_helpers import read_file, write_file
from tools.helpers.os_helpers import handle_sigint, clear_screen
from tools.utils.string_utils import remove_punctuation_symbols

_OUTPUT_FILE = f"{CSV_FILE[:-4]}-{DUPLICATES.lower()}.txt"
_MATCH_THRESHOLD = 0.9  # Seems a reasonable threshold


def _get_duplicates(lines: list) -> (list, list):
    normalized_lines = [_normalize(line) for line in lines]
    num_lines = len(normalized_lines)
    duplicates = []
    possible_duplicates = []

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
    album = Album(line)
    result = f"{album.artist}{album.title}".lower()
    result = result.replace(' ', '')
    result = remove_punctuation_symbols(result)

    return result


def _write_output_file(duplicates: list, possible_duplicates: list) -> None:
    if duplicates or possible_duplicates:
        issues = []

        if duplicates:
            issues.append(f"{DUPLICATES}:\n\n")
            issues.extend(duplicates)
            issues.append('\n')

        if possible_duplicates:
            issues.append(f"{POSSIBLE_DUPLICATES}:\n\n")
            issues.extend(possible_duplicates)
            issues.append('\n')

        write_file(_OUTPUT_FILE, issues)
        print(DONE)
    else:
        print(NO_DUPLICATES_FOUND)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{LOOKING_FOR_DUPLICATES_IN} '{CSV_FILE}'...")

    lines = read_file(CSV_FILE)[1:]
    duplicates, possible_duplicates = _get_duplicates(lines)

    _write_output_file(duplicates, possible_duplicates)
