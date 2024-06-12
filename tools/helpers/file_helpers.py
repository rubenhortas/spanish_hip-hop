import datetime
import shutil

from tools.crosscutting.strings import NO_SUCH_FILE_OR_DIRECTORY, PERMISSION_DENIED


def read_file(file: str) -> list:
    try:
        with open(file, 'r') as f:
            return f.readlines()
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' {NO_SUCH_FILE_OR_DIRECTORY}")
        exit(-1)
    except PermissionError:
        print(f"{PERMISSION_DENIED}: '{file}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{file}' OSError: {os_error}")
        exit(-1)


def write_file(file: str, lines: list) -> None:
    try:
        if lines:
            with open(file, 'w') as f:
                f.writelines(lines)
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' {NO_SUCH_FILE_OR_DIRECTORY}")
        exit(-1)
    except PermissionError:
        print(f"{PERMISSION_DENIED}: '{file}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{file}' OSError: {os_error}")
        exit(-1)


def backup(file: str) -> None:
    try:
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        shutil.copy(file, f"{file}_{timestamp}.bkp")
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' {NO_SUCH_FILE_OR_DIRECTORY}")
        exit(-1)
    except PermissionError:
        print(f"{PERMISSION_DENIED}: '{file}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{file}' OSError: {os_error}")
        exit(-1)
