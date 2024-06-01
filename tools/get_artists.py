#!/usr/bin/env python3
from tools.libraries.config import CSV_FILE, CSV_SEPARATOR
from tools.libraries.file_helpers import read_file, write_file

_OUTPUT_FILE = 'artists.txt'

if __name__ == '__main__':
    lines = read_file(CSV_FILE)[1:]
    artists = set()

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        artists.add(line_[0].strip().lower())

    artists_ = [f"\t'{artist.lower()}':'{artist.upper()}',\n" for artist in artists]
    write_file(_OUTPUT_FILE, sorted(artists_))
