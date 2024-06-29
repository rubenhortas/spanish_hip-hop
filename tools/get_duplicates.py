#!/usr/bin/env python3
import difflib
import signal

from tqdm import tqdm

from tools.config.config import CSV_FILE, CsvPosition, CSV_DELIMITER
from tools.crosscutting.strings import DONE, DUPLICATES, NO_DUPLICATES_FOUND, LOOKING_FOR_DUPLICATES_IN, SIMILARS
from tools.helpers.file_helpers import write_file, read_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen
from tools.utils.string_utils import remove_punctuation_symbols

_OUTPUT_FILE = f"{CSV_FILE[:-4]}-{DUPLICATES.lower()}.txt"
_MATCH_THRESHOLD = 0.9  # Seems a reasonable threshold


class Line:
    def __init__(self, csv_line):
        self.id = csv_line[CsvPosition.ID.value]
        self.artist = csv_line[CsvPosition.ARTIST.value]
        self.title = csv_line[CsvPosition.TITLE.value]
        self.hash = self._get_string_hash()
        self.is_duplicate = False
        self.duplicates = []
        self.similar = []

    def __str__(self):
        return f"{self.id}{CSV_DELIMITER}{self.artist}{CSV_DELIMITER}{self.title}..."

    def __eq__(self, other):
        return (self.id == other.id
                and self.artist == other.artist
                and self.title == other.title
                and self.hash == other.hash
                and all(a == b for a, b in zip(self.duplicates, other.duplicates))
                and all(a == b for a, b in zip(self.similar, other.similar)))

    def has_duplicates(self):
        return len(self.duplicates) > 0

    def has_similar(self):
        return len(self.similar) > 0

    def _get_string_hash(self):
        value = f"{self.artist}{self.title}".lower()
        value = value.replace(' ', '')
        value = remove_punctuation_symbols(value)

        return value


def _get_duplicates(csv_lines: list) -> list:
    lines = []
    duplicates = []

    for line in csv_lines:
        lines.append(Line(line))

    lines_num = len(lines)
    sequence_matcher = difflib.SequenceMatcher(None)

    for i in tqdm(range(lines_num)):
        current_line = lines[i]
        sequence_matcher.set_seq1(current_line.hash)

        for j in range(i + 1, lines_num):
            comparing_line = lines[j]

            if not comparing_line.is_duplicate:
                sequence_matcher.set_seq2(comparing_line.hash)
                match_ratio = sequence_matcher.ratio()

                if match_ratio > _MATCH_THRESHOLD:
                    comparing_line.is_duplicate = True

                    if match_ratio == 1:
                        current_line.duplicates.append(comparing_line)
                    else:
                        current_line.similar.append(comparing_line)

        if current_line.has_duplicates() or current_line.has_similar():
            duplicates.append(current_line)

    return duplicates


def _write_output_file(lines: list) -> None:
    if lines:
        output_lines = []

        for line in lines:
            output_lines.append(f"{line}\n:")

            if line.has_duplicates():
                output_lines.append(f"\t{DUPLICATES}\n:")

                for duplicate in line.duplicates:
                    output_lines.append(f"\t - {duplicate}\n")

                output_lines.append('')

            if line.has_similar():
                output_lines.append(f"\t{SIMILARS}\n:")

                for similar in line.similar:
                    output_lines.append(f"\t - {similar}\n")

                output_lines.append('')

            output_lines.append('')

        write_file(_OUTPUT_FILE, output_lines)
        print(f"\n{DONE}")
    else:
        print(f"{NO_DUPLICATES_FOUND}")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{LOOKING_FOR_DUPLICATES_IN} '{CSV_FILE}'...")

    lines = read_csv_file(CSV_FILE)[1:]
    duplicates = _get_duplicates(lines)

    _write_output_file(duplicates)
