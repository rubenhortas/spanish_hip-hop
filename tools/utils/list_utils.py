from tools.utils.string_utils import convert_to_python_string


def create_python_list(name: str, dictionary: dict) -> list:
    lst = [f"{name.upper()} = " + '{\n']

    for key, value in dictionary.items():
        key_ = convert_to_python_string(key)

        if isinstance(value, str):
            value_ = convert_to_python_string(dictionary[value])
            lst.append(f"    '{key_}': '{value_}',\n")
        elif isinstance(value, tuple):
            value_ = convert_to_python_string(value[0])
            comment = value[1]

            if comment == '':
                lst.append(f"    '{key_}': '{value_}',\n")
            else:
                lst.append(f"    '{key_}': '{value_}',  # {comment}\n")

    lst.append('}\n')

    return lst
