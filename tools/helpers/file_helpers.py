import csv
import datetime
import shutil
from functools import wraps
from typing import Callable

from config.config import CSV_DELIMITER
from crosscutting.strings import NO_SUCH_FILE_OR_DIRECTORY, PERMISSION_DENIED


def _do_file_operation(func: Callable) -> Callable:
    @wraps(func)
    def _do_file_operation_wrapper(file: str, lines: list = None) -> list | None:
        try:
            if 'read' in func.__name__:
                return func(file)
            else:
                if lines:
                    return func(file, lines)
        except FileNotFoundError as file_not_found_error:
            print(f"'{file_not_found_error.filename}' {NO_SUCH_FILE_OR_DIRECTORY}")
            exit(-1)
        except PermissionError:
            print(f"{PERMISSION_DENIED}: '{file}'")
            exit(-1)
        except OSError as os_error:
            print(f"'{file}' OSError: {os_error}")
            exit(-1)

    return _do_file_operation_wrapper


@_do_file_operation
def read_csv_file(file: str) -> list:
    with open(file, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=CSV_DELIMITER, quotechar='"', quoting=csv.QUOTE_ALL)
        return list(csv_reader)


@_do_file_operation
def write_csv_file(file: str, rows: list) -> None:
    with open(file, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=CSV_DELIMITER, quotechar='"', quoting=csv.QUOTE_ALL)

        for row in rows:
            csv_writer.writerow(row)


@_do_file_operation
def read_file(file: str) -> list:
    with open(file, 'r', encoding='utf-8') as f:
        return f.readlines()


@_do_file_operation
def write_file(file: str, lines: list) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        f.writelines(lines)


@_do_file_operation
def backup(file: str) -> None:
    """
    Backups a file.
    @param file: 'foo.bar'
    @return: 'foo_20241201240001.bar'
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    shutil.copy(file, f"{file}_{timestamp}.bkp")
