from tools.exceptions import EXCEPTIONS


def capitalize_first_letter(string: str):
    words = string.split()
    first_word = words[0]

    if first_word not in EXCEPTIONS:
        return string[0].upper() + string[1:]

    return string
