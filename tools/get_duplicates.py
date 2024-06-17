#!/usr/bin/env python3
import difflib
import signal

from tools.config.config import CSV_FILE, CsvPosition, CSV_DELIMITER
from tools.crosscutting.strings import DONE, DUPLICATES, POSSIBLE_DUPLICATES, NO_DUPLICATES_FOUND, \
    LOOKING_FOR_DUPLICATES_IN
from tools.helpers.file_helpers import write_file, read_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen
from tools.utils.string_utils import remove_punctuation_symbols

_OUTPUT_FILE = f"{CSV_FILE[:-4]}-{DUPLICATES.lower()}.txt"
_MATCH_THRESHOLD = 0.9  # Seems a reasonable threshold


def _get_duplicates(lines: list) -> (list, list):
    lines_ = _normalize_lines(lines)
    lines_num = len(lines_)
    duplicates = []
    possible_duplicates = []

    for i in range(lines_num):
        print(f"\r{i + 1}/{lines_num}", end='')

        for j in range(i + 1, lines_num):
            match_ratio = difflib.SequenceMatcher(None, lines_[i][1], lines_[j][1]).ratio()

            if match_ratio > _MATCH_THRESHOLD:
                duplicate = f"{lines_[i][0].strip()}  -> {lines_[j][0]}"

                if match_ratio == 1:
                    duplicates.append(duplicate)
                else:
                    possible_duplicates.append(duplicate)

                break

    return duplicates, possible_duplicates


def _normalize_lines(lines: list) -> list:
    normalized_lines = []

    for line in lines:
        line_resume_info = f"{line[CsvPosition.ID.value]}{CSV_DELIMITER}{line[CsvPosition.ARTIST.value]}{CSV_DELIMITER}{line[CsvPosition.TITLE.value]}..."
        line_value = _normalize(line[CsvPosition.ARTIST.value], line[CsvPosition.TITLE.value])
        line_info = (line_resume_info, line_value)
        normalized_lines.append(line_info)

    return normalized_lines


def _normalize(artist: str, title: str) -> str:
    value = f"{artist}{title}"
    value = value.replace(' ', '')
    value = remove_punctuation_symbols(value)

    return value


def _write_output_file(duplicates: list, possible_duplicates: list) -> None:
    if duplicates or possible_duplicates:
        issues = []

        if duplicates:
            issues.append(f"{DUPLICATES}:\n\n")

            for duplicate in duplicates:
                issues.append(f"{duplicate}\n")

            issues.append('\n')

        if possible_duplicates:
            issues.append(f"{POSSIBLE_DUPLICATES}:\n\n")

            for possible_duplicate in possible_duplicates:
                issues.append(f"{possible_duplicate}\n")

            issues.append('\n')

        write_file(_OUTPUT_FILE, issues)
        print(f"\n{DONE}")
    else:
        print(f"{NO_DUPLICATES_FOUND}")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{LOOKING_FOR_DUPLICATES_IN} '{CSV_FILE}'...")

    lines = read_csv_file(CSV_FILE)[1:]
    duplicates, possible_duplicates = _get_duplicates(lines)

    _write_output_file(duplicates, possible_duplicates)
