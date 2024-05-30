#!/usr/bin/env python3

import signal

from tools.libraries.config import CSV_FILE, CSV_HEADER, CSV_SEPARATOR
from tools.libraries.file_helper import write_output_file, read_file
from tools.libraries.os_helper import handle_sigint, clear_screen
from tools.libraries.album import Album

CSV_OUTPUT_FILE = f"{CSV_FILE[:-4]} - formateado.csv"


def _format_entries() -> list:
    original_entries = [line.strip() for line in read_file(CSV_FILE)][1:]
    formatted_entries = []
    entry_num = 1
    entries_num = len(original_entries)

    for entry in original_entries:
        print(f"\r{entry_num}/{entries_num}", end='')

        try:
            entry_ = entry.split(CSV_SEPARATOR)
            album = Album(entry_[0], entry_[1], entry_[2], entry_[3])  # artist, title, date, format
            formatted_entries.append(album.list())

            # Debug
            # if entry_[0] != album.artist or entry_[1] != album.title:
            #     print(f": '{entry_[0]},{entry_[1]}' -> '{album.artist},{album.title}'")
        except IndexError:
            print(f"'{entry}: bad format")

        entry_num += 1

    print()

    sorted_formatted_entries = sorted(formatted_entries, key=lambda entry: (entry[0], entry[2], entry[1]))
    result = [f"{CSV_HEADER}\n"]
    result.extend([f"{CSV_SEPARATOR.join(e)}\n" for e in sorted_formatted_entries])

    return result


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Generating {CSV_OUTPUT_FILE}")
    formatted_entries = _format_entries()
    write_output_file(CSV_OUTPUT_FILE, formatted_entries)
    print('Done')
