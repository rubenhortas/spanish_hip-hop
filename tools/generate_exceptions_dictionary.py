#!/usr/bin/env python3

from tools.Exception import EXCEPTIONS

OUTPUT_FILE = 'Exception.py'


def _get_keys(dictionary: dict):
    keys = set()
    entries = []

    for key in dictionary:
        keys.add(key)

    for key in sorted(list(keys), key=str.lower):
        key_ = key.replace("'", "\\'")
        value = dictionary[key].replace("'", "\\'")
        entries.append(f"\t'{key_}': '{value}',\n")

    return entries


if __name__ == '__main__':
    """
    Generates the file exceptions_dictionary.txt with the exceptions dictionary alphabetically ordered without duplicates.
    """
    try:
        result = ['# Words that will be *not* capitalized\n', 'EXCEPTIONS = {\n']
        keys = _get_keys(EXCEPTIONS)
        result.extend(keys)
        result.append('}\n')

        with open(OUTPUT_FILE, 'w') as f:
            f.writelines(result)
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{OUTPUT_FILE}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{OUTPUT_FILE}' OSError: {os_error}")
        exit(-1)
