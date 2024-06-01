#!/usr/bin/env python3
import signal

from tools.exceptions import EXCEPTIONS
from tools.libraries.file_helpers import write_file
from tools.libraries.os_helpers import handle_sigint

_OUTPUT_FILE = 'exceptions.py'


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


def _write_output_file(keys):
    exceptions = ['# Words that will be *not* capitalized\n', 'EXCEPTIONS = {\n']
    exceptions.extend(keys)
    exceptions.append('}\n')
    write_file(_OUTPUT_FILE, exceptions)


if __name__ == '__main__':
    """
    Generates the file exceptions.py with the exceptions dictionary alphabetically ordered without duplicates.
    """
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"Generating new {_OUTPUT_FILE}...")

    new_exceptions = _get_exceptions(EXCEPTIONS)
    _write_output_file(new_exceptions)

    print('Done')
