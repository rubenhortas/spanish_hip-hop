#!/usr/bin/env python3
import os
import signal

from tools.config.exceptions import EXCEPTIONS
from tools.crosscutting.strings import GENERATING_NEW, DONE
from tools.helpers.file_helpers import write_file, backup
from tools.helpers.os_helpers import handle_sigint

_OUTPUT_FILE = os.path.join(os.path.abspath(''), 'config', 'exceptions.py')


def _get_exceptions(dictionary: dict) -> list:
    keys = set()
    new_exceptions = set()

    for key in dictionary:
        keys.add(key)

    for key in keys:
        key_ = key.replace("'", "\\'").lower()
        value = dictionary[key].replace("'", "\\'")
        new_exceptions.add(f"\t'{key_}': '{value}',\n")

    return sorted(list(new_exceptions))


def _write_output_file(keys: list) -> None:
    if keys:
        exceptions = ['EXCEPTIONS = {\n']
        exceptions.extend(keys)
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
        * 'value': The value to be formatted to (both for album titles and artist names).
            - Setting a format exception is used to preserve uppercase, lowercase, special words, etc., 
              for example: 'f0o BaR the album'.
            - Exceptions will also apply to artist names, for example: 'f0o BaR,fOo BaR the album,...'
    """
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    new_exceptions = _get_exceptions(EXCEPTIONS)

    backup(_OUTPUT_FILE)
    _write_output_file(new_exceptions)

    print(DONE)