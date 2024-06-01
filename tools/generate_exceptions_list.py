#!/usr/bin/env python3
import signal

from tools.exceptions import EXCEPTIONS
from tools.libraries.file_helpers import write_file
from tools.libraries.os_helpers import handle_sigint

_OUTPUT_FILE = 'exceptions.py'


def _get_exceptions(exceptions: list) -> list:
    new_exceptions = []

    for exception in sorted(exceptions):
        if exception not in new_exceptions:
            new_exception = exception.replace("'", "\\'")
            new_exceptions.append(f"\t'{new_exception},'\n")

    return new_exceptions


def _write_output_file(exceptions: list):
    new_exceptions = ['# Words that will be *not* capitalized\n', 'EXCEPTIONS = [\n']
    new_exceptions.extend(exceptions)
    new_exceptions.append(']\n')
    write_file(_OUTPUT_FILE, new_exceptions)


if __name__ == '__main__':
    """
    Generates the file exceptions.py with the exceptions list alphabetically ordered without duplicates.
    """
    signal.signal(signal.SIGINT, handle_sigint)
    print(f"Generating new {_OUTPUT_FILE}...")

    new_exceptions = _get_exceptions(EXCEPTIONS)
    _write_output_file(new_exceptions)

    print('Done')
