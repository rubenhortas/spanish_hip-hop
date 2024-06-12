import datetime
import shutil


def read_file(file: str) -> list:
    try:
        with open(file, 'r') as f:
            return f.readlines()
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no se encuentra el fichero o el directorio")
        exit(-1)
    except PermissionError:
        print(f"Permiso denegado: '{file}'")
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
        print(f"'{file_not_found_error.filename}' no se encuentra el fichero o el directorio")
        exit(-1)
    except PermissionError:
        print(f"Permiso denegado: '{file}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{file}' OSError: {os_error}")
        exit(-1)


def backup(file: str) -> None:
    try:
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        shutil.copy(file, f"{file}_{timestamp}.bkp")
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no se encuentra el fichero o el directorio")
        exit(-1)
    except PermissionError:
        print(f"Permiso denegado: '{file}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{file}' OSError: {os_error}")
        exit(-1)
