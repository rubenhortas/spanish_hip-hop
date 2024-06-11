#!/usr/bin/env python3
import signal
from collections import Counter

from tools.libraries.config import CSV_SEPARATOR, CSV_FILE, SEPARATOR_NUMBER
from tools.libraries.file_helpers import read_file, write_file
from tools.libraries.os_helpers import handle_sigint, clear_screen

_INCORRECT_SEPARATORS = 'errores - separadores incorrectos.txt'
_MISMATCHED_PARENTHESES_FILE = 'errores - parentesis.txt'
_MISMATCHED_SQUARE_BRACKETS_FILE = 'errores - corchetes.txt'


def _get_issues(lines) -> (list, list, list):
    incorrect_separators = []
    mismatched_parentheses = []
    mismatched_square_brackets = []

    for line in lines:
        line_counter = Counter(line)

        if not _has_correct_number_separators(line_counter):
            incorrect_separators.append(line)

        if _has_mismatched_symbols(line, line_counter, '(', ')'):
            mismatched_parentheses.append(line)

        if _has_mismatched_symbols(line, line_counter, '[', ']'):
            mismatched_square_brackets.append(line)

    return incorrect_separators, mismatched_parentheses, mismatched_square_brackets


def _has_correct_number_separators(line_counter: Counter):
    return line_counter[CSV_SEPARATOR] == SEPARATOR_NUMBER


def _has_mismatched_symbols(line: str, line_counter: Counter, left_symbol: str, right_symbol: str) -> bool:
    def has_mismatched_symbols(counter: Counter) -> bool:
        if counter[left_symbol] != counter[right_symbol]:
            return True

        return False

    if has_mismatched_symbols(line_counter):
        return True
    else:
        values = line.split(CSV_SEPARATOR)

        for value in values:
            if has_mismatched_symbols(Counter(value)):
                return True

    return False


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_sigint)
    clear_screen()
    print(f"Buscando líneas con problemas en '{CSV_FILE}'...")

    lines = read_file(CSV_FILE)[1:]
    incorrect_separators, mismatched_parentheses, mismatched_square_brackets = _get_issues(lines)

    if incorrect_separators or mismatched_parentheses or mismatched_square_brackets:
        write_file(_INCORRECT_SEPARATORS, incorrect_separators)
        write_file(_MISMATCHED_PARENTHESES_FILE, mismatched_parentheses)
        write_file(_MISMATCHED_SQUARE_BRACKETS_FILE, mismatched_square_brackets)
        print('Hecho')
    else:
        print('No se han encontrado problemas')
