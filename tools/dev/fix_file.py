#!/usr/bin/env python3
import os
import signal
from collections import Counter

from tools.config.config import CSV_FILE, CSV_SEPARATOR, SEPARATOR_NUMBER, CsvPosition
from tools.crosscutting.strings import FIXING, DONE, ERRORS, FIXED
from tools.helpers.file_helpers import read_file, write_file
from tools.helpers.os_helpers import handle_sigint, clear_screen

_INPUT_FILE = os.path.join(os.path.abspath('..'), CSV_FILE)
_OUTPUT_FILE = os.path.join(os.path.abspath('..'), f"{CSV_FILE[:-4]}-{FIXED.lower()}.csv")
_ERROR_FILE = os.path.join(os.path.abspath('..'), f"{CSV_FILE[:-4]}-{ERRORS.lower()}.csv")
_FOREIGN_ARTISTS = ['Ace Hood', 'Ali G indahouse', 'Aqeel', 'Aqueel', 'Asap Mob', 'G Jazz', 'Gavlyn', 'Gee Falcone',
                    'Jim Jones', 'Kafu Banton', 'Kev Brown', 'Kidz In The Hall', 'Random Axe', 'Red Pill', 'Rick Ross',
                    'Schoolboy Q', 'Sean Combs', 'Snak The Ripper', 'Stan Forebee', 'Stat Quo', 'Statik Selektah',
                    'Step Brothers', 'Strange Fruit Project', 'Street Bucks', 'String Theory', 'Strong Arm Steady',
                    'TNGHT', 'Tenacity', 'Terrace Martin', 'Tragedy Khadafi', 'Vinnie Paz', 'Wadada Sound System',
                    'Wale', 'Wiz Khalifa', 'Young Jeezy']
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
    print(f"{FIXING} '{CSV_FILE}'...")

    lines = read_file(_INPUT_FILE)
    header = lines[0].replace('"', '')

    fixed_lines, errors = _fix(lines[1:])

    if fixed_lines:
        fixed_lines.insert(0, header)
        write_file(_OUTPUT_FILE, fixed_lines)

    write_file(_ERROR_FILE, errors)

    print(DONE)
