#!/usr/bin/env python3

import os
import signal

from tools.libraries.config import CSV_FILE, CSV_SEPARATOR
from tools.libraries.file_helpers import read_file, write_file
from tools.libraries.os_helpers import handle_sigint, clear_screen

_OUTPUT_FILE = f"{CSV_FILE[:-4]} - fixed.csv"

_DESCONOCIDOS = ['desconocido', '[desconocido]', 'intérprete desconocido']


def _remove_quotation_marks(lines: list) -> list:
    fixed_lines = []

    for line in lines:
        fixed_line = line.replace('"', '')
        fixed_lines.append(fixed_line)

    return fixed_lines


def _add_dashes(lines: list) -> list:
    fixed_lines = []

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        new_line = ','.join([field if field else '-' for field in line_])
        fixed_lines.append(new_line)

    return fixed_lines


def _delete_desconocidos(lines: list) -> list:
    fixed_lines = []

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        new_line = ','.join([field if field.lower() not in _DESCONOCIDOS else '-' for field in line_])
        fixed_lines.append(new_line)

    return fixed_lines


def _fix(lines: list) -> list:
    fixed_lines = _remove_quotation_marks(lines)
    fixed_lines = _add_dashes(fixed_lines)
    fixed_lines = _delete_desconocidos(fixed_lines)

    return fixed_lines


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Fixing {CSV_FILE}...")
    lines = read_file(os.path.join(os.path.abspath('..'), CSV_FILE))
    fixed_lines = _fix(lines)
    write_file(os.path.join(os.path.abspath('..'), _OUTPUT_FILE), fixed_lines)
    print('Done')
