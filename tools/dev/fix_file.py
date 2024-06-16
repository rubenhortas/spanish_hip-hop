#!/usr/bin/env python3
import os
import signal

from tools.config.config import CSV_FILE, CsvPosition
from tools.crosscutting.strings import FIXING, DONE, ERRORS, FIXED
from tools.helpers.file_helpers import read_csv_file, write_csv_file
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


def _fix(lines: list, num_fields: int) -> (list, list):
    errors = []

    for line in lines:
        if len(line) == num_fields:
            if line[CsvPosition.ARTIST.value] not in _FOREIGN_ARTISTS:
                if line[CsvPosition.PRESERVER.value] == '' or line[CsvPosition.PRESERVER.value] == '-':
                    value_index = 0

                    for value in line:
                        if value:
                            if value == '-':
                                line[value_index] = ''

                            if value.lower() in _DESCONOCIDOS:
                                line[value_index] = ''

                        value_index += 1
        else:
            errors.append(line)
            lines.remove(line)

    return lines, errors


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{FIXING} '{CSV_FILE}'...")

    lines = read_csv_file(_INPUT_FILE)

    if lines:
        csv_header = lines[0]
        fixed_lines, errors = _fix(lines[1:], len(csv_header))

        if fixed_lines:
            fixed_lines.insert(0, csv_header)
            write_csv_file(_OUTPUT_FILE, fixed_lines)

        if errors:
            errors.insert(0, csv_header)
            write_csv_file(_ERROR_FILE, errors)

    print(DONE)
