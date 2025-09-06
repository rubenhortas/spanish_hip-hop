#!/usr/bin/env python3
import os
import signal

from config.config import CSV_FILE, CsvPosition
from config.exceptions import EXCEPTIONS
from crosscutting.strings import GENERATING_NEW, DONE
from helpers.file_helpers import write_file, backup, read_csv_file
from helpers.os_helpers import handle_sigint
from utils.list_utils import create_python_dictionary

_OUTPUT_FILE = os.path.join(os.path.abspath(''), 'config', 'exceptions.py')


def regenerate_exceptions_dictionary() -> None:
    """
    Removes duplicates from the 'EXCEPTIONS' exception dictionary (file /config/exceptions.py)
    and sorts the dictionary alphabetically.

    Dictionary format: 'key': 'value',
        EXCEPTIONS = {
            'foo': 'fOo',
            'bar': 'BaR',
        }

        * 'key': The lowercase word.
        * 'value': The value to which the word be transformed in the titles.
            - Setting a format exception is used to preserve uppercase, lowercase, special words, etc.,
              for example: 'f0o BaR the album'.
            - Exceptions will *not* be applied to artist names.
    """
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    exceptions = _get_exceptions()

    backup(_OUTPUT_FILE)
    _write_output_file(exceptions)


def _get_exceptions() -> dict:
    new_exceptions = {}
    title_words = _get_title_words()

    for key in EXCEPTIONS:
        if key not in new_exceptions and key in title_words:
            new_exceptions[key] = EXCEPTIONS[key]

    return dict(sorted(new_exceptions.items()))


def _get_title_words() -> set:
    title_words = set()
    lines = read_csv_file(CSV_FILE)

    if lines:
        for line in lines:
            title = line[CsvPosition.TITLE.value].lower().split()

            for word in title:
                title_words.add(word)

    return title_words


def _write_output_file(exceptions: dict) -> None:
    exceptions_ = create_python_dictionary('EXCEPTIONS', exceptions)
    write_file(_OUTPUT_FILE, exceptions_)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)

    regenerate_exceptions_dictionary()

    print(DONE)
