from tools.utils.string_utils import convert_to_python_string


def create_python_list(lst_name: str, values: list) -> list:
    lst = [f"{lst_name.upper()} = [\n"]

    for value in values:
        lst.append(f"\t'{convert_to_python_string(value)}',\n")

    lst.append(']\n')

    return lst


def create_python_dictionary(name: str, dictionary: dict) -> list:
    lst = [f"{name.upper()} = " + '{\n']

    for key in dictionary:
        lst.append(f"\t'{convert_to_python_string(key)}': '{convert_to_python_string(dictionary[key])}',\n")

    lst.append('}\n')

    return lst
