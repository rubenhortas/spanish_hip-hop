#!/usr/bin/env python3
import os
import signal

from tools.config.config import CSV_SEPARATOR, CSV_FILE, CsvPosition
from tools.crosscutting.strings import GENERATING_NEW, DONE
from tools.helpers.file_helpers import read_file, backup, write_file
from tools.utils.list_utils import create_python_list, create_python_dictionary
from tools.helpers.os_helpers import handle_sigint

_INPUT_FILE = os.path.join(os.path.abspath(''), CSV_FILE)
_OUTPUT_FILE = f"{os.path.join(os.path.abspath(''), 'config', 'artists.py')}"


def _get_artists(lines: list) -> (list, list):
    artists_ = set()
    separators_ = set()

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        line_value = line_[CsvPosition.ARTIST.value].strip()
        line_value = line_value.replace('"', '')
        line_value = line_value.replace('(', '').replace(')', '')
        line_value = line_value.replace('[', '').replace(']', '')

        if not line_value.isnumeric():
            artists_.add(line_value)

        words = line_value.split()

        for word in words:
            if len(word) == 1 and (word.lower() == 'y' or not word.isalnum()):
                separators_.add(word)
            elif word.isalnum() and not word.isnumeric():
                artists_.add(word)

    return sorted(list(artists_)), sorted(list(separators_))


def _write_output_file(artists: list, separators: list) -> None:
    separators = create_python_list('SEPARATORS', separators)
    art = create_python_dictionary('ARTISTS', artists)

    result = []
    result.extend(separators)
    result.append('\n')
    result.extend(art)

    write_file(_OUTPUT_FILE, result)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    lines = read_file(_INPUT_FILE)[1:]
    artists, separators = _get_artists(lines)

    backup(_OUTPUT_FILE)
    _write_output_file(artists, separators)

    print(DONE)
