from tools.utils.string_utils import convert_to_python_string


def create_python_list(lst_name: str, values: list) -> list:
    lst = [f"{lst_name.upper()} = [\n"]

    for value in values:
        lst.append(f"\t'{convert_to_python_string(value)}',\n")

    lst.append(']\n')

    return lst


def create_python_dictionary(name: str, values: list) -> list:
    lst = [f"{name.upper()} = " + '{\n']

    for value in values:
        lst.append(f"\t'{convert_to_python_string(value.lower())}': '{convert_to_python_string(value)}',\n")

    lst.append('}\n')

    return lst
