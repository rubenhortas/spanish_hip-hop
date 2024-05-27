#!/usr/bin/env python3

from Exception import EXCEPTIONS

OUTPUT_FILE = 'exceptions_dictionary.txt'

if __name__ == '__main__':
    """
    Generates the file exceptions_dictionary.txt with the exceptions dictionary alphabetically ordered without duplicates.
    """
    try:
        unique_keys = []
        result = ['EXCEPTIONS = {']

        for key in EXCEPTIONS:
            if key not in unique_keys:
                unique_keys.append(key)

        for key in sorted(unique_keys, key=str.lower):
            key_ = key.replace("'", "\\'")
            value = EXCEPTIONS[key].replace("'", "\\'")
            result.append(f"\t'{key_}': '{value}',\n")

        result.append('}')

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
