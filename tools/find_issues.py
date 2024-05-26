#!/usr/bin/env python3

from collections import Counter

if __name__ == '__main__':
    try:
        CSV_FILE = 'lista trabajos hip-hop español.csv'
        # CSV_FILE = 'lista trabajos hip-hop español - formateado.csv'

        extra_commas = []
        parentheses_issues = []

        with open(CSV_FILE, 'r') as f:
            lines = f.readlines()
        # Commas
        # Parentheses

        for line in lines:
            line_counter = Counter(line)

            if line_counter[','] > 3:
                extra_commas.append(line.strip())

            if line_counter['('] != line_counter[')']:
                parentheses_issues.append(line.strip())

        if extra_commas or parentheses_issues:
            if extra_commas:
                print('Lines with extra commas:\n')

                for line in extra_commas:
                    print(line)

                print()

            if parentheses_issues:
                print('Lines with parentheses issues:\n')

                for line in parentheses_issues:
                    print(line)

                print()
        else:
            print('No se encontraron problemas')
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{CSV_FILE}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{CSV_FILE}' OSError: {os_error}")
        exit(-1)
