from typing import overload

from tools.utils.string_utils import convert_to_python_string


@overload
def create_python_list(name: str, values: list) -> list:
    ...


@overload
def create_python_list(name: str, dictionary: dict) -> list:
    ...


def create_python_list(name: str, values: list | dict) -> list:
    if isinstance(values, list):
        return _create_python_list_from_list(name, values)
    elif isinstance(values, dict):
        return _create_python_list_from_dictionary(name, values)


def _create_python_list_from_list(name: str, values: list) -> list:
    lst = [f"{name.upper()} = [\n"]

    for value in values:
        lst.append(f"\t'{convert_to_python_string(value)}',\n")

    lst.append(']\n')

    return lst


def _create_python_list_from_dictionary(name: str, dictionary: dict) -> list:
    lst = [f"{name.upper()} = " + '{\n']

    for key, value in dictionary.items():
        key_ = convert_to_python_string(key)

        if isinstance(value, str):
            value_ = convert_to_python_string(dictionary[value])
            lst.append(f"\t'{key_}': '{value_}',\n")
        elif isinstance(value, tuple):
            value_ = convert_to_python_string(value[0])
            comment = value[1]

            if comment == '':
                lst.append(f"\t'{key_}': '{value_}',\n")
            else:
                lst.append(f"\t'{key_}': '{value_}',  # {comment}\n")

    lst.append('}\n')

    return lst
