#!/usr/bin/env python3

import os
import signal

from tools.libraries.config import CSV_FILE, CSV_SEPARATOR
from tools.libraries.file_helpers import read_file, write_file
from tools.libraries.os_helpers import handle_sigint, clear_screen

_OUTPUT_FILE = f"{CSV_FILE[:-4]} - fixed.csv"
_FOREIGN_ARTISTS = ['Ace Hood', 'Aqeel', 'Aqueel', 'Asap Mob', 'G Jazz', 'Gavlyn', 'Gee Falcone', 'Jim Jones', 'Kafu Banton', 'Kev Brown',
                    'Kidz In The Hall', 'Random Axe', 'Red Pill', 'Rick Ross', 'Schoolboy Q', 'Sean Combs', 'Snak The Ripper', 'Stan Forebee',
                    'Stat Quo', 'Statik Selektah', 'Step Brothers', 'Strange Fruit Project', 'Street Bucks', 'String Theory',
                    'Strong Arm Steady', 'TNGHT', 'Tenacity', 'Terrace Martin', 'Tragedy Khadafi', 'Vinnie Paz', 'Wadada Sound System', 'Wale',
                    'Wiz Khalifa', 'Young Jeezy']
_DESCONOCIDOS = ['desconocido', '[desconocido]', 'intérprete desconocido']


def _remove_foreign_artists(lines: list) -> list:
    print('Removing foreign artists...')
    lines_ = []

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)

        if line_[1] not in _FOREIGN_ARTISTS:
            lines_.append(line)

    return lines


def _remove_quotation_marks(lines: list) -> list:
    print('Removing quotation marks...')
    fixed_lines = []

    for line in lines:
        fixed_line = line.replace('"', '')
        fixed_lines.append(fixed_line)

    return fixed_lines


def _add_dashes(lines: list) -> list:
    print('Adding dashes...')
    fixed_lines = []

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        new_line = ','.join([field if field else '-' for field in line_])
        fixed_lines.append(new_line)

    return fixed_lines


def _delete_desconocidos(lines: list) -> list:
    print('Deleting "desconocido[s]"')
    fixed_lines = []

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        new_line = ','.join([field if field.lower() not in _DESCONOCIDOS else '-' for field in line_])
        fixed_lines.append(new_line)

    return fixed_lines


def _fix(lines: list) -> list:
    fixed_lines = _remove_quotation_marks(lines)
    fixed_lines = _remove_foreign_artists(fixed_lines)
    fixed_lines = _add_dashes(fixed_lines)
    fixed_lines = _delete_desconocidos(fixed_lines)

    return fixed_lines


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Fixing {CSV_FILE}...")
    lines = read_file(os.path.join(os.path.abspath(''), CSV_FILE))
    fixed_lines = _fix(lines)
    write_file(os.path.join(os.path.abspath(''), _OUTPUT_FILE), fixed_lines)
    print('Done')
