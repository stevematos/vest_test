import re


def split_symbol_and_number(string):
    match = re.search(r'([\D]+)([\d,/.]+)', string)
    items_split = match.groups()
    return items_split
