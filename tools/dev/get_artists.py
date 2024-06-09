#!/usr/bin/env python3
import os

from tools.libraries.config import CSV_FILE, CSV_SEPARATOR
from tools.libraries.file_helpers import read_file, write_file

# _OUTPUT_FILE = f"{os.path.join(os.getcwd(), 'dev', 'artists.txt')}"
_OUTPUT_FILE = 'check - artistas.txt'

if __name__ == '__main__':
    lines = read_file(os.path.join(os.path.abspath('..'), CSV_FILE))[1:]
    artists = set()

    for line in lines:
        line_ = line.split(CSV_SEPARATOR)
        artists.add(line_[1].strip())

    artists_ = [f"'{artist}'\n" for artist in artists]

    write_file(_OUTPUT_FILE, sorted(artists_))
