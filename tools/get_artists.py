#!/usr/bin/env python3
from tools.libraries.config import CSV_FILE, CSV_SEPARATOR
from tools.libraries.file_helpers import read_file, write_file
from tools.libraries.string_utils import replace_exceptions

_OUTPUT_FILE = 'artists.txt'

if __name__ == '__main__':
    lines = read_file(CSV_FILE)[1:]
    artists = set()

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        if ' & ' not in line_[0] and ' y ' not in line_[0] and '-N-' not in line_[0] and ' vs ' not in line_[0].lower():
            artists.add(line_[0].strip().lower())

    artists_ = [f"\t'{replace_exceptions(artist.title())}':'{artist.upper()}',\n" for artist in artists]
    write_file(_OUTPUT_FILE, sorted(artists_))
