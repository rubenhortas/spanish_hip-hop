def create_list(lst_name: str, values: list) -> list:
    lst = [f"{lst_name.upper()} = [\n"]

    for value in values:
        lst.append(f"\t'{value}',\n")

    lst.append(']\n')

    return lst
