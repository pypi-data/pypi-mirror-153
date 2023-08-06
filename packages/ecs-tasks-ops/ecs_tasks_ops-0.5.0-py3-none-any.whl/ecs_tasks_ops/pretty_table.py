"""Module to create beautiful tables from dicts."""
from tabulate import tabulate


def tabulate_list_json(
    data=(), fields_from=None, fields_to=None, empty_msg="No data to show"
) -> str:
    """Generate a table with information from a list of json."""
    if not data:
        return empty_msg

    keys = list(data[0].keys())
    if fields_from and fields_to:
        keys = keys[fields_from:fields_to]
    elif fields_from:
        keys = keys[fields_from:]
    elif fields_to:
        keys = keys[:fields_to]
    return tabulate_list_json_keys(data=data, keys=keys, empty_msg=empty_msg)


def tabulate_list_json_keys(data=(), keys=(), empty_msg="No data to show"):
    """Generate a table from a list of json where you can specify keys to show."""
    if not data:
        return empty_msg

    headers = {k: k for k in keys}
    return tabulate(
        [{k: v for k, v in c.items() if k in headers} for c in data], headers=headers
    )
