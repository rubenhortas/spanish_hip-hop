#!/usr/bin/env python3
import os
import signal
from types import FrameType

CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_SEPARATOR = ','


def _handle_sigint(signal: int, frame: FrameType) -> None:
    print('\rStopped')
    exit(0)


def _clear_screen() -> None:
    if 'nt' in os.name:
        os.system('cls')
    elif 'posix' in os.name:
        os.system('clear')


def _capitalize(line: str) -> str:
    fields = line.split(CSV_SEPARATOR)

    # TODO: Exceptions in fields 0 and 1
    return f"{fields[0].title()}{CSV_SEPARATOR}{fields[1].capitalize()}{CSV_SEPARATOR}{fields[2]}{CSV_SEPARATOR}{fields[3]}"


def _capitalize_file() -> list:
    try:
        with open(CSV_FILE, 'r') as f:
            return [_capitalize(line) for line in f.readlines()]
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{CSV_FILE}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{CSV_FILE}' OSError: {os_error}")
        exit(-1)


def _write_output_file(file: str, lines: list) -> None:
    try:
        with open(file, 'w') as f:
            f.writelines(lines)
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{file}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{file}' OSError: {os_error}")
        exit(-1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handle_sigint)
    _clear_screen()
    capitalized_lines = _capitalize_file()
    # TODO: Sort capitalized lines before write the output file
    _write_output_file('new.csv', capitalized_lines)
