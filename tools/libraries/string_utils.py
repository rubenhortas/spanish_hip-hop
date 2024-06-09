import re
from collections import Counter
from typing import Pattern

from tools.exceptions import EXCEPTIONS
from tools.libraries.config import CSV_SEPARATOR, SEPARATOR_NUMBER

_VOLUME_RE = re.compile(r'((?P<label>(vol)(\?|(ume)n?)?([. ]{0,2})\??)(?P<num>\w*(\.?\d*)?))', re.IGNORECASE)
_PARENTHESES_REGEX = re.compile(r'(?P<text>(\(.*\))|(\([\w .-?]+)|[\w .-?]+\))')
_SQUARE_BRACKETS_REGEX = re.compile(r'(?P<text>(\[.*])|(\[[\w .-?]+)|[\w .-?]+])')


def _fix_mismatched(string: str, left_char: str, right_char: str, regex: Pattern[str]) -> str:
    match = re.search(regex, string)

    if match:
        match_text = match.group('text')
        text_counter = Counter(match_text)

        if text_counter[left_char] != text_counter[right_char]:
            stript_text = match_text.replace(left_char, '').replace(right_char, '')
            return string.replace(match_text, f"{left_char}{stript_text}{right_char}")

    return string


def replace_exceptions(string: str) -> str:
    string_ = string
    words = string.split()

    for word in words:
        if word.lower() in EXCEPTIONS:
            string_ = string_.replace(word, EXCEPTIONS[word.lower()])

    return string_


def fix_volumes(string: str) -> str:
    match = re.search(_VOLUME_RE, string)

    if match:
        match_ = match.group(0)
        new_label = match.group('label').capitalize()
        new_label = new_label.replace(' ', '')
        new_label = new_label.replace('?', '')
        new_label = new_label.capitalize()

        if new_label == 'Vol':
            new_label = 'Vol.'

        new_num = match.group('num').upper()

        result = string.replace(match_, f"{new_label} {new_num}")

        return result

    return string


def has_correct_number_separators(line: str) -> bool:
    return Counter(line)[CSV_SEPARATOR] == SEPARATOR_NUMBER


def fix_mismatched_square_brackets(string: str) -> str:
    return _fix_mismatched(string, '[', ']', _SQUARE_BRACKETS_REGEX)


def fix_mismatched_parentheses(string: str) -> str:
    return _fix_mismatched(string, '(', ')', _PARENTHESES_REGEX)
