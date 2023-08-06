import collections


def value_mapper(a_dict, b_dict):
    """
    a_dict = {
        'key1': 'a_value1',
        'key2': 'a_value2'
    }

    b_dict = {
        'key1': 'b_value1',
        'key2': 'b_value2'
    }

    >>> value_mapper(a_dict, b_dict)
    {
        'a_value1': 'b_value1',
        'a_value2': 'b_value2'
    }
    """

    return {a_value: b_dict.get(a_key) for a_key, a_value in a_dict.items()}


def isiter(arg):
    return isinstance(arg, collections.Iterable) and not isinstance(arg, str)
