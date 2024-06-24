import re
import string
from collections import Counter
from typing import Pattern

_REGEX_VOLUMES = re.compile(r'((?P<label>(vol)(\?|(ume)n?)?([. ]{0,2})\??\b)(?P<num>\w*(\.?\d*)?))', re.IGNORECASE)
_REGEX_PARENTHESES = re.compile(r'(?P<text>(\(.+\))|(\(.+|\S+\)))')
_REGEX_SQUARE_BRACKETS = re.compile(r'(?P<text>(\[.+])|(\[.+|\S+]))')
_REGEX_QUOTES = re.compile(r'(?P<text>((".+)|(\S+")))')
_REGEX_ACRONYMS = re.compile(r'^([a-z][.-])+[a-z]?$', re.IGNORECASE)


def fix_volumes(string: str) -> str:
    match = re.search(_REGEX_VOLUMES, string)

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


def has_mismatched_square_brackets(string: str) -> bool:
    return _has_mismatched(string, '[', ']')


def has_mismatched_parentheses(string: str) -> bool:
    return _has_mismatched(string, '(', ')')


def has_mismatched_quotes(string: str) -> bool:
    return Counter(string)['"'] % 2 != 0


def fix_mismatched_square_brackets(string: str) -> str:
    return _fix_mismatched(string, '[', ']', _REGEX_SQUARE_BRACKETS)


def fix_mismatched_parentheses(string: str) -> str:
    return _fix_mismatched(string, '(', ')', _REGEX_PARENTHESES)


def fix_mismatched_quotes(string: str) -> str:
    match = re.search(_REGEX_QUOTES, string)

    if match:
        match_text = match.group('text')
        text = match_text.replace('"', '')
        return string.replace(match_text, f"\"{text}\"")

    return string


def convert_to_python_string(string: str) -> str:
    return string.replace("'", "\\'")


def remove_punctuation_symbols(string_: str, punctuation_symbols: list = None) -> str:
    clean_string = string_

    if not punctuation_symbols:
        punctuation_symbols = string.punctuation

    for symbol in punctuation_symbols:
        clean_string = clean_string.replace(symbol, '')

    return clean_string


def replace_word(word: str, string: str) -> str:
    match = re.search(rf"\b{word}\b", string, re.IGNORECASE)

    if match:
        match_text = match.group(0)
        return string.replace(match_text, word)

    return string


def is_acronym(string: str) -> bool:
    match = re.search(_REGEX_ACRONYMS, string)

    if match:
        return True

    return False


def _has_mismatched(string: str, left_char: str, right_char: str) -> bool:
    string_counter = Counter(string)
    return string_counter[left_char] != string_counter[right_char]


def _fix_mismatched(string: str, left_char: str, right_char: str, regex: Pattern[str]) -> str:
    match = re.search(regex, string)

    if match:
        match_text = match.group('text')
        text_counter = Counter(match_text)

        if text_counter[left_char] != text_counter[right_char]:
            text = match_text.replace(left_char, '').replace(right_char, '')
            return string.replace(match_text, f"{left_char}{text}{right_char}")

    return string
