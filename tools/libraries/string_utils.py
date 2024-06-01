import re

from tools.exceptions import EXCEPTIONS

_VOLUME_RE = re.compile(r'((?P<label>(vol)(\?|(ume)n?)?([. ]{0,2})\??0?)'
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
        return f"Vol. {match.group('num').upper()}"

    return string
