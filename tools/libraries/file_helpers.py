def read_file(file: str) -> list:
    try:
        with open(file, 'r') as f:
            return f.readlines()
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{file}'")
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
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{file}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{file}' OSError: {os_error}")
        exit(-1)
