#!/usr/bin/env python3

from collections import Counter

from tools.libraries.config import CSV_SEPARATOR, SEPARATOR_NUMBER


def has_correct_number_separators(line: str):
    return Counter(line)[CSV_SEPARATOR] == SEPARATOR_NUMBER
