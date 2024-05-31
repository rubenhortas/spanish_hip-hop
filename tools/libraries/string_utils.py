from tools.exceptions import EXCEPTIONS


def replace_exceptions(string: str) -> str:
    string_ = string
    words = string.split()

    for word in words:
        if word.lower() in EXCEPTIONS:
            string_ = string_.replace(word, EXCEPTIONS[word.lower()])

    return string_
