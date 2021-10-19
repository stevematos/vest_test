import re


def split_symbol_and_number(string):
    match = re.search(r'([\D]+)([\d,/.]+)', string)
    items_split = match.groups()
    return items_split


def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')


# print(get_change(24, 30))


def average(lst):
    return sum(lst) / len(lst)
