#!/usr/bin/env python3
import signal

from tools.libraries.exceptions import EXCEPTIONS
from tools.libraries.file_helpers import write_file
from tools.libraries.os_helpers import handle_sigint

_OUTPUT_FILE = '../libraries/exceptions.py'


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
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"Generando nuevo '{_OUTPUT_FILE}'...")

    new_exceptions = _get_exceptions(EXCEPTIONS)
    _write_output_file(new_exceptions)

    print('Hecho')
