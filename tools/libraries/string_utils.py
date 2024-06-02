import re

from tools.exceptions import EXCEPTIONS

_VOLUME_RE = re.compile(r'((?P<label>(vol)(\?|(ume)n?)?([. ]{0,2})\??)'
                        r'(?P<num>\w*(\.?\d*)?))'
                        , re.IGNORECASE)


def replace_exceptions(string: str) -> str:
    string_ = string
    words = string.split()

    for word in words:
        if word.lower() in EXCEPTIONS:
            string_ = string_.replace(word, EXCEPTIONS[word.lower()])

    return string_


def replace_volumes(string: str) -> str:
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
