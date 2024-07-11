from tools.utils.string_utils import convert_to_python_string


def create_python_dictionary(name: str, dictionary: dict) -> list:
    """
    Creates a string that represents a python dictionary from a python dictionary value type.
    @param name: 'foo_dict'
    @param dictionary: 'bar_dict = { 'bob': 'Bob', 'alice': 'Alice' }
    @return:
        'foo_dict = {\n
            \t'bob': 'Bob',\n
            \t'alice': 'Alice'\n
        }\n'
    """
    lst = [f"{name.upper()} = " + '{\n']

    for key, value in dictionary.items():
        key_ = convert_to_python_string(key)

        if isinstance(value, str):
            value_ = convert_to_python_string(value)
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
