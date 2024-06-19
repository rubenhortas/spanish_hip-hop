#!/usr/bin/env python3
import os
import signal

from tools.config.exceptions import EXCEPTIONS
from tools.crosscutting.strings import GENERATING_NEW, DONE
from tools.helpers.file_helpers import write_file, backup
from tools.helpers.os_helpers import handle_sigint

_OUTPUT_FILE = os.path.join(os.path.abspath(''), 'config', 'exceptions.py')


def regenerate_exceptions_dictionary() -> None:
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    exceptions = _get_exceptions(EXCEPTIONS)

    backup(_OUTPUT_FILE)
    _write_output_file(exceptions)


def _get_exceptions(dictionary: dict) -> list:
    keys = set()
    new_exceptions = []

    for key in dictionary:
        keys.add(key)

    for key in keys:
        key_ = key.replace("'", "\\'").lower()
        value = dictionary[key].replace("'", "\\'")
        new_exceptions.append(f"\t'{key_}': '{value}',\n")

    return sorted(new_exceptions)


def _write_output_file(values: list) -> None:
    if values:
        exceptions = ['EXCEPTIONS = {\n']
        exceptions.extend(values)
        exceptions.append('}\n')
        write_file(_OUTPUT_FILE, exceptions)


if __name__ == '__main__':
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
            - Exceptions will *not* apply to artist names.
    """
    signal.signal(signal.SIGINT, handle_sigint)

    regenerate_exceptions_dictionary()

    print(DONE)
