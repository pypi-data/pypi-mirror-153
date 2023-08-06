from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'NDim': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::DataRange',
        'method_name': 'NDim',
        'return_type': 'unsigned int',
    },
    'Size': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::DataRange',
        'method_name': 'Size',
        'return_type': 'unsigned int',
    },
    'IsSet': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::DataRange',
        'method_name': 'IsSet',
        'return_type': 'bool',
    },
    'IsInside': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'ROOT::Fit::DataRange',
        'method_name': 'IsInside',
        'return_type': 'bool',
    },
}


T = TypeVar('T')


def _add_method_metadata(s: ObjectStream[T], a: ast.Call) -> Tuple[ObjectStream[T], ast.Call]:
    '''Add metadata for a collection to the func_adl stream if we know about it
    '''
    assert isinstance(a.func, ast.Attribute)
    if a.func.attr in _method_map:
        s_update = s.MetaData(_method_map[a.func.attr])
        return s_update, a
    else:
        return s, a


@func_adl_callback(_add_method_metadata)
class DataRange:
    "A class"

    def NDim(self) -> int:
        "A method"
        ...

    def Size(self, icoord: int) -> int:
        "A method"
        ...

    def IsSet(self) -> bool:
        "A method"
        ...

    def IsInside(self, x: float, icoord: int) -> bool:
        "A method"
        ...
