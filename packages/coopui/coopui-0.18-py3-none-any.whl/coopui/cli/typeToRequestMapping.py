import uuid
from typing import List, Dict
from coopui.cli.CliAtomicUserInteraction import CliAtomicUserInteraction as ui
from datetime import date, datetime
from inspect import signature
from enum import Enum

def _tupleize_a_func(func):
    return (func, [x for x in signature(func).parameters])

CLI_TYPE_TO_REQUEST_MAPPING = {
    int: _tupleize_a_func(ui.request_int),
    str: _tupleize_a_func(ui.request_string),
    datetime: _tupleize_a_func(ui.request_datetime),
    date: _tupleize_a_func(ui.request_date),
    float: _tupleize_a_func(ui.request_float),
    uuid.UUID: _tupleize_a_func(ui.request_guid),
    List: _tupleize_a_func(ui.request_from_list),
    Dict: _tupleize_a_func(ui.request_from_dict),
    bool: _tupleize_a_func(ui.request_bool),
    Enum: _tupleize_a_func(ui.request_enum),
}

if __name__ == "__main__":
    [print(x) for x in CLI_TYPE_TO_REQUEST_MAPPING.items()]