#!/usr/bin/env python3

"""
Gets duplicates (and possible duplicates) entries of the CSV file.

Output:
    - CSV file with duplicates and possible duplicates (if any).
"""
import difflib
import multiprocessing
import signal
from collections import defaultdict

from config.config import CSV_FILE, CsvPosition, CSV_DELIMITER
from crosscutting.strings import DONE, DUPLICATES, NO_DUPLICATES_FOUND, LOOKING_FOR_DUPLICATES_IN, SIMILARS
from helpers.file_helpers import write_file, read_csv_file
from helpers.os_helpers import handle_sigint, clear_screen
from utils.string_utils import delete_punctuation_symbols

_OUTPUT_FILE = f"{CSV_FILE[:-4]}-{DUPLICATES.lower()}.txt"
_MATCH_THRESHOLD = 0.9  # Seems a reasonable threshold


class Line:
    hash = ''
    summary_info = ''

    def __init__(self, csv_line: list):
        self._set_hash(csv_line)
        self._set_info(csv_line)

    def __lt__(self, other):
        return self.hash < other.hash

    def __gt__(self, other):
        return self.hash > other.hash

    def __eq__(self, other):
        return self.hash == other.hash

    def _set_hash(self, csv_line: list) -> None:
        string_ = f"{csv_line[CsvPosition.ARTIST.value]}{csv_line[CsvPosition.TITLE.value]}"
        string_ = string_.replace(' ', '')
        self.hash = delete_punctuation_symbols(string_).lower()

    def _set_info(self, csv_line: list) -> None:
        self.summary_info = f"'{csv_line[CsvPosition.ID.value]}{CSV_DELIMITER}{csv_line[CsvPosition.ARTIST.value]}{CSV_DELIMITER}{csv_line[CsvPosition.TITLE.value]}{CSV_DELIMITER}...'"


def _get_duplicates(csv_lines: list) -> (list, list):
    lines = []
    lines_dict = defaultdict(list)

    for csv_line in csv_lines:
        lines.append(Line(csv_line))

    lines.sort()

    for line in lines:
        lines_dict[line.hash[0]].append(line)

    duplicates = []
    similar = []

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        for key in lines_dict:
            if len(lines_dict[key]) > 1:
                result = pool.map(_compare, [lines_dict[key]])

                if result[0][0]:
                    duplicates.extend(result[0][0])

                if result[0][1]:
                    similar.extend(result[0][1])

    return duplicates, similar


def _compare(lines: list) -> (list, list):
    duplicates = defaultdict(list)
    similar = defaultdict(list)
    lines_num = len(lines)
    sequence_matcher = difflib.SequenceMatcher(None)

    for i in range(lines_num):
        current_line = lines[i]
        sequence_matcher.set_seq1(current_line.hash)

        for j in range(i + 1, lines_num):
            comparing_line = lines[j]
            sequence_matcher.set_seq2(comparing_line.hash)
            match_ratio = sequence_matcher.ratio()

            if match_ratio > _MATCH_THRESHOLD:
                if match_ratio == 1:
                    duplicates[current_line.summary_info].append(comparing_line.summary_info)
                else:
                    similar[current_line.summary_info].append(comparing_line.summary_info)

    duplicates = dict(sorted(duplicates.items()))
    similar = dict(sorted(similar.items()))

    return [*duplicates.items()], [*similar.items()]


def _write_output_file(duplicates: list, similar: list) -> None:
    if duplicates or similar:
        result = []

        if duplicates:
            result.append(f"{DUPLICATES}:\n\n")

            for duplicate in duplicates:
                line = f"* {duplicate[0]}:"

                for duplicate_ in duplicate[1]:
                    line = f"{line} {duplicate_},"

                result.append(f"{line[:-1]}\n")

            result.append('\n')

        if similar:
            result.append(f"{SIMILARS}:\n\n")

            for similar in similar:
                line = f"* {similar[0]}:"

                for similar_ in similar[1]:
                    line = f"{line} {similar_},"

                result.append(f"{line[:-1]}\n")

        write_file(_OUTPUT_FILE, result)
        print(f"\n{DONE}")
    else:
        print(f"{NO_DUPLICATES_FOUND}")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{LOOKING_FOR_DUPLICATES_IN} '{CSV_FILE}'...")

    lines = read_csv_file(CSV_FILE)[1:]
    duplicates, similar = _get_duplicates(lines)

    _write_output_file(duplicates, similar)
