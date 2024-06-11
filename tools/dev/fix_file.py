#!/usr/bin/env python3

import os
import signal
from collections import Counter

from tools.libraries.config import CSV_FILE, CSV_SEPARATOR, SEPARATOR_NUMBER, CsvPosition
from tools.libraries.file_helpers import read_file, write_file
from tools.libraries.os_helpers import handle_sigint, clear_screen

_OUTPUT_FILE = f"{CSV_FILE[:-4]} - arreglado.csv"
_ERROR_FILE = f"{CSV_FILE[:-4]} - errores.csv"
_FOREIGN_ARTISTS = ['Ace Hood', 'Aqeel', 'Aqueel', 'Asap Mob', 'G Jazz', 'Gavlyn', 'Gee Falcone', 'Jim Jones',
                    'Kafu Banton', 'Kev Brown',
                    'Kidz In The Hall', 'Random Axe', 'Red Pill', 'Rick Ross', 'Schoolboy Q', 'Sean Combs',
                    'Snak The Ripper', 'Stan Forebee',
                    'Stat Quo', 'Statik Selektah', 'Step Brothers', 'Strange Fruit Project', 'Street Bucks',
                    'String Theory',
                    'Strong Arm Steady', 'TNGHT', 'Tenacity', 'Terrace Martin', 'Tragedy Khadafi', 'Vinnie Paz',
                    'Wadada Sound System', 'Wale',
                    'Wiz Khalifa', 'Young Jeezy']
_DESCONOCIDOS = ['desconocido', '[desconocido]', 'intérprete desconocido']


def _fix(lines: list) -> (list, list):
    fixed_lines = []
    errors = []

    for line in lines:
        if Counter(line)[CSV_SEPARATOR] == SEPARATOR_NUMBER:
            values = line.split(CSV_SEPARATOR)

            if values[CsvPosition.ARTIST.value] not in _FOREIGN_ARTISTS:
                if values[CsvPosition.PRESERVER.value] == '-' or values[CsvPosition.PRESERVER.value] == '':
                    fixed_values = []

                    for value in values:
                        value_ = value

                        if value_:
                            if value_[0] == '"' and value_[-1] == '"':
                                value_ = value_[1:-1]

                            if value_.lower() in _DESCONOCIDOS:
                                value_ = ''

                        fixed_values.append(value_)

                    fixed_lines.append(CSV_SEPARATOR.join(fixed_values))
        else:
            errors.append(line)

    return fixed_lines, errors


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Fixing {CSV_FILE}...")

    lines = read_file(os.path.join(os.path.abspath('..'), CSV_FILE))
    header = lines[0].replace('"', '')
    fixed_lines, errors = _fix(lines[1:])

    fixed_lines.insert(0, header)
    write_file(os.path.join(os.path.abspath(''), _OUTPUT_FILE), fixed_lines)

    if errors:
        write_file(os.path.join(os.path.abspath(''), _ERROR_FILE), errors)

    print('Done')
