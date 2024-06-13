import re
import string
from collections import Counter
from typing import Pattern

from tools.config.exceptions import EXCEPTIONS
from tools.config.config import CSV_SEPARATOR, SEPARATOR_NUMBER

_VOLUME_RE = re.compile(r'((?P<label>(vol)(\?|(ume)n?)?([. ]{0,2})\??\b)(?P<num>\w*(\.?\d*)?))', re.IGNORECASE)
_PARENTHESES_REGEX = re.compile(r'(?P<text>(\(.*\))|(\([\w .-?]+)|[\w.-?]+\))')
_SQUARE_BRACKETS_REGEX = re.compile(r'(?P<text>(\[.*])|(\[[\w .-?]+)|[\w.-?]+])')


def replace_exceptions(s: str) -> str:
    string_ = s
    words = s.split()

    for word in words:
        if word.lower() in EXCEPTIONS:
            string_ = string_.replace(word, EXCEPTIONS[word.lower()])

    return string_


def fix_volumes(s: str) -> str:
    match = re.search(_VOLUME_RE, s)

    if match:
        match_text = match.group(0)
        vol_label = match.group('label').capitalize()
        vol_label = vol_label.replace(' ', '')
        vol_label = vol_label.replace('?', '')
        vol_label = vol_label.capitalize()

        if vol_label == 'Vol':
            vol_label = 'Vol.'

        vol_num = match.group('num').upper()
        result = s.replace(match_text, f"{vol_label} {vol_num}")

        return result

    return s


def has_correct_number_separators(line: str) -> bool:
    return Counter(line)[CSV_SEPARATOR] == SEPARATOR_NUMBER


def fix_mismatched_square_brackets(s: str) -> str:
    return _fix_mismatched(s, '[', ']', _SQUARE_BRACKETS_REGEX)


def fix_mismatched_parentheses(s: str) -> str:
    return _fix_mismatched(s, '(', ')', _PARENTHESES_REGEX)


def convert_to_python_string(s: str) -> str:
    return s.replace("'", "\\'")


def remove_puntuation_symbols(s: str) -> str:
    s_ = s

    for symbol in string.punctuation:
        s_ = s_.replace(symbol, '')

    return s


def _fix_mismatched(s: str, left_char: str, right_char: str, regex: Pattern[str]) -> str:
    match = re.search(regex, s)

    if match:
        match_text = match.group('text')
        text_counter = Counter(match_text)

        if text_counter[left_char] != text_counter[right_char]:
            text = match_text.replace(left_char, '').replace(right_char, '')
            return s.replace(match_text, f"{left_char}{text}{right_char}")

    return s
