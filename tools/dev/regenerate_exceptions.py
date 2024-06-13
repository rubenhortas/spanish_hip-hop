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
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"{GENERATING_NEW} '{_OUTPUT_FILE}'...")

    new_exceptions = _get_exceptions(EXCEPTIONS)

    backup(_OUTPUT_FILE)
    _write_output_file(new_exceptions)

    print(DONE)
