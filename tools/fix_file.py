#!/usr/bin/env python3
import os
import signal

from tools.config.config import CSV_FILE, CsvPosition, CSV_HEADER
from tools.crosscutting.strings import FIXING, DONE, FIXED, WRONG_FIELDS_NUMBER, FOREIGN_ARTISTS
from tools.helpers.file_helpers import read_csv_file, write_csv_file
from tools.helpers.os_helpers import handle_sigint, clear_screen

_INPUT_FILE = os.path.join(os.path.abspath(''), CSV_FILE)
_OUTPUT_FILE = os.path.join(os.path.abspath(''), f"{CSV_FILE[:-4]}-{FIXED.lower()}.csv")
_WRONG_FIELD_NUMBERS_FILE = os.path.join(os.path.abspath(''), f"{CSV_FILE[:-4]}-{WRONG_FIELDS_NUMBER.lower()}.csv")
_FOREIGN_ARTISTS_FILE = os.path.join(os.path.abspath(''), f"{CSV_FILE[:-4]}-{FOREIGN_ARTISTS.lower()}.csv")
_FOREIGN_ARTISTS = ['Ace Hood', 'Ali G indahouse', 'Aqeel', 'Aqueel', 'Asap Mob', 'G Jazz', 'Gavlyn', 'Gee Falcone',
                    'Jim Jones', 'Kafu Banton', 'Kev Brown', 'Kidz In The Hall', 'Random Axe', 'Red Pill', 'Rick Ross',
                    'Schoolboy Q', 'Sean Combs', 'Snak The Ripper', 'Stan Forebee', 'Stat Quo', 'Statik Selektah',
                    'Step Brothers', 'Strange Fruit Project', 'Street Bucks', 'String Theory', 'Strong Arm Steady',
                    'TNGHT', 'Tenacity', 'Terrace Martin', 'Tragedy Khadafi', 'Vinnie Paz', 'Wadada Sound System',
                    'Wale', 'Wiz Khalifa', 'Young Jeezy', 'Chamillionaire']
_UNKNOWN = ['desconocido', '[desconocido]', 'intérprete desconocido', '-']


def _fix(lines: list, fields_num: int) -> (list, list):
    lines_ = []
    wrong_fields_number = []
    foreign_artists = []

    for line in lines:
        if len(line) == fields_num:
            if line[CsvPosition.ARTIST.value] not in _FOREIGN_ARTISTS:
                if line[CsvPosition.PRESERVER.value] == '' or line[CsvPosition.PRESERVER.value] == '-':
                    line_ = line.replace('  ', ' ')
                    value_index = 0

                    for value in line_:
                        if value:
                            if value.lower() in _UNKNOWN:
                                line_[value_index] = ''

                        value_index += 1

                lines_.append(line)
            else:
                foreign_artists.append(line)
        else:
            wrong_fields_number.append(line)

    return lines_, wrong_fields_number, foreign_artists


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"{FIXING} '{CSV_FILE}'...")

    lines = read_csv_file(_INPUT_FILE)

    if lines:
        lines_, wrong_fields_number, foreign_artists = _fix(lines[1:], len(CSV_HEADER))

        if lines_:
            lines_.insert(0, CSV_HEADER)
            write_csv_file(_OUTPUT_FILE, lines_)

        if wrong_fields_number:
            wrong_fields_number.insert(0, CSV_HEADER)
            write_csv_file(_WRONG_FIELD_NUMBERS_FILE, wrong_fields_number)

        if foreign_artists:
            foreign_artists.insert(0, CSV_HEADER)
            write_csv_file(_FOREIGN_ARTISTS_FILE, foreign_artists)

    print(DONE)
