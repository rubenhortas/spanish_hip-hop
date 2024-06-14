import re
import string
from collections import Counter
from typing import Pattern

from tools.config.exceptions import EXCEPTIONS
from tools.config.config import CSV_SEPARATOR, SEPARATOR_NUMBER

_VOLUME_RE = re.compile(r'((?P<label>(vol)(\?|(ume)n?)?([. ]{0,2})\??\b)(?P<num>\w*(\.?\d*)?))', re.IGNORECASE)
_PARENTHESES_REGEX = re.compile(r'(?P<text>(\(.*\))|(\([\w .-?]+)|[\w.-?]+\))')
_SQUARE_BRACKETS_REGEX = re.compile(r'(?P<text>(\[.*])|(\[[\w .-?]+)|[\w.-?]+])')


def replace_exceptions(string: str) -> str:
    s_ = string
    words = string.split()

    for word in words:
        key = word.lower()

        if key in EXCEPTIONS:
            s_ = s_.replace(word, EXCEPTIONS[key])

    return s_


def fix_volumes(string: str) -> str:
    match = re.search(_VOLUME_RE, string)

    if match:
        match_text = match.group(0)
        vol_label = match.group('label').capitalize()
        vol_label = vol_label.replace(' ', '')
        vol_label = vol_label.replace('?', '')
        vol_label = vol_label.capitalize()

        if vol_label == 'Vol':
            vol_label = 'Vol.'

        vol_num = match.group('num').upper()
        result = string.replace(match_text, f"{vol_label} {vol_num}")

        return result

    return string


def has_correct_number_separators(line: str) -> bool:
    return Counter(line)[CSV_SEPARATOR] == SEPARATOR_NUMBER


def fix_mismatched_square_brackets(string: str) -> str:
    return _fix_mismatched(string, '[', ']', _SQUARE_BRACKETS_REGEX)


def fix_mismatched_parentheses(string: str) -> str:
    return _fix_mismatched(string, '(', ')', _PARENTHESES_REGEX)


def convert_to_python_string(string: str) -> str:
    return string.replace("'", "\\'")


def remove_punctuation_symbols(string_: str) -> str:
    clean_string = string_

    for symbol in string.punctuation:
        clean_string = clean_string.replace(symbol, '')

    return clean_string


def _fix_mismatched(string: str, left_char: str, right_char: str, regex: Pattern[str]) -> str:
    match = re.search(regex, string)

    if match:
        match_text = match.group('text')
        text_counter = Counter(match_text)

        if text_counter[left_char] != text_counter[right_char]:
            text = match_text.replace(left_char, '').replace(right_char, '')
            return string.replace(match_text, f"{left_char}{text}{right_char}")

    return string
