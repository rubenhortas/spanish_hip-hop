def create_dictionary(name: str, values: list, keys_in_lower: bool = False) -> list:
    lst = [f"{name.upper()} = " + '{\n']

    for value in values:
        key = value.lower if keys_in_lower else value
        lst.append(f"\t'{key}': '{value}',\n")

    lst.append('}\n')

    return lst
