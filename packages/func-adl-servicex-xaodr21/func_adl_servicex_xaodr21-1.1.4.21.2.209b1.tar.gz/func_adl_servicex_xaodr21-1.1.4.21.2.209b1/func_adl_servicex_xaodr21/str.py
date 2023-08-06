from __future__ import annotations
import ast
from typing import Tuple, TypeVar, Iterable
from func_adl import ObjectStream, func_adl_callback, func_adl_parameterized_call
import func_adl_servicex_xaodr21

_method_map = {
    'empty': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'string',
        'method_name': 'empty',
        'return_type': 'bool',
    },
    'append': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'string',
        'method_name': 'append',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'string',
    },
    'assign': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'string',
        'method_name': 'assign',
        'return_type_element': '__gnu_cxx::__normal_iterator<char*,string>',
        'return_type_collection': 'string',
    },
    'compare': {
        'metadata_type': 'add_method_type_info',
        'type_string': 'string',
        'method_name': 'compare',
        'return_type': 'int',
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
class str:
    "A class"

    def empty(self) -> bool:
        "A method"
        ...

    def append(self, __str: str) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def assign(self, __str: str) -> func_adl_servicex_xaodr21.str.str:
        "A method"
        ...

    def compare(self, __str: str) -> int:
        "A method"
        ...
