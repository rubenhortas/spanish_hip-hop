#!/usr/bin/env python3

from collections import Counter

CSV_FILE = 'lista trabajos hip-hop español.csv'
CSV_SEPARATOR = ','

if __name__ == '__main__':
    try:
        extra_separators = []
        parentheses_issues = []

        with open(CSV_FILE, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line_counter = Counter(line)

            if line_counter[CSV_SEPARATOR] > 3:
                extra_separators.append(line.strip())

            if line_counter['('] != line_counter[')']:
                parentheses_issues.append(line.strip())

        if extra_separators or parentheses_issues:
            if extra_separators:
                print('Lines with extra separators:\n')

                for line in extra_separators:
                    print(line)

                print()

            if parentheses_issues:
                print('Lines with parentheses issues:\n')

                for line in parentheses_issues:
                    print(line)
        else:
            print('No issues found.')
    except FileNotFoundError as file_not_found_error:
        print(f"'{file_not_found_error.filename}' no such file or directory")
        exit(-1)
    except PermissionError:
        print(f"Permission denied: '{CSV_FILE}'")
        exit(-1)
    except OSError as os_error:
        print(f"'{CSV_FILE}' OSError: {os_error}")
        exit(-1)
