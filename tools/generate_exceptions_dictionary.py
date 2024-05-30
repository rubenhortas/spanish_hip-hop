#!/usr/bin/env python3
import signal

from tools.exceptions import EXCEPTIONS
from tools.libraries.file_helpers import write_file
from tools.libraries.os_helpers import handle_sigint

OUTPUT_FILE = 'exceptions.py'


def _get_exceptions(dictionary: dict):
    keys = set()
    entries = []

    for key in dictionary:
        keys.add(key)

    for key in sorted(list(keys), key=str.lower):
        key_ = key.replace("'", "\\'").lower()
        value = dictionary[key].replace("'", "\\'")
        entries.append(f"\t'{key_}': '{value}',\n")

    return entries


if __name__ == '__main__':
    """
    Generates the file exceptions.py with the exceptions dictionary alphabetically ordered without duplicates.
    """
    signal.signal(signal.SIGINT, handle_sigint)
    exceptions = ['# Words that will be *not* capitalized\n', 'EXCEPTIONS = {\n']
    keys = _get_exceptions(EXCEPTIONS)
    exceptions.extend(keys)
    exceptions.append('}\n')
    write_file(OUTPUT_FILE, exceptions)
