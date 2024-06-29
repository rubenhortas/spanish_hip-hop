#!/usr/bin/env python3
import difflib
import signal
from collections import defaultdict

from tqdm import tqdm

from tools.config.config import CSV_FILE, CsvPosition, CSV_DELIMITER
from tools.crosscutting.strings import DONE, DUPLICATES, NO_DUPLICATES_FOUND, LOOKING_FOR_DUPLICATES_IN, SIMILARS
from tools.helpers.file_helpers import write_file, read_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen
from tools.utils.string_utils import remove_punctuation_symbols

_OUTPUT_FILE = f"{CSV_FILE[:-4]}-{DUPLICATES.lower()}.txt"
_MATCH_THRESHOLD = 0.9  # Seems a reasonable threshold


class Line:
    hash = ''
    info = ''
    used = False

    def __init__(self, csv_line: list):
        self._set_hash(csv_line)
        self._set_info(csv_line)

    def _set_hash(self, csv_line: list) -> None:
        string_ = f"{csv_line[CsvPosition.ARTIST.value]}{csv_line[CsvPosition.TITLE.value]}"
        string_ = string_.replace(' ', '')
        self.hash = remove_punctuation_symbols(string_).lower()

    def _set_info(self, csv_line: list) -> None:
        self.info = f"'{csv_line[CsvPosition.ID.value]}{CSV_DELIMITER}{csv_line[CsvPosition.ARTIST.value]}{CSV_DELIMITER}{csv_line[CsvPosition.TITLE.value]}{CSV_DELIMITER}...'"


def _get_duplicates(csv_lines: list) -> (list, list):
    duplicates = defaultdict(list)
    similars = defaultdict(list)
    lines = []

    for csv_line in csv_lines:
        lines.append(Line(csv_line))

    lines_num = len(lines)
    sequence_matcher = difflib.SequenceMatcher(None)

    for i in tqdm(range(lines_num)):
        current_line = lines[i]
        sequence_matcher.set_seq1(current_line.hash)

        for j in range(i + 1, lines_num):
            comparing_line = lines[j]

            if not comparing_line.used:
                sequence_matcher.set_seq2(comparing_line.hash)
                match_ratio = sequence_matcher.ratio()

                if match_ratio > _MATCH_THRESHOLD:
                    comparing_line.used = True

                    if match_ratio == 1:
                        duplicates[current_line.info].append(comparing_line.info)
                    else:
                        similars[current_line.info].append(comparing_line.info)

    duplicates = dict(sorted(duplicates.items()))
    similars = dict(sorted(similars.items()))

    return [*duplicates.items()], [*similars.items()]


def _write_output_file(duplicates: list, similars: list) -> None:
    if duplicates or similars:
        result = []

        if duplicates:
            result.append(f"{DUPLICATES}:\n\n")

            for duplicate in duplicates:
                line = f"* {duplicate[0]}:"

                for duplicate_ in duplicate[1]:
                    line = f"{line} {duplicate_},"

                result.append(f"{line[:-1]}\n")

            result.append('\n')

        if similars:
            result.append(f"* {SIMILARS}:\n\n")

            for similar in similars:
                line = f"{similar[0]}:"

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
    duplicates, similars = _get_duplicates(lines)

    _write_output_file(duplicates, similars)
